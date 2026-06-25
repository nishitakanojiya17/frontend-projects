"""
RAG (Retrieval-Augmented Generation) utilities for Campus Mitra AI.

Pipeline:
  1. extract_text()   — pull text from PDF / DOCX / PPTX
  2. chunk_text()     — split into ~500-char chunks
  3. index_note()     — save chunks to NoteChunk table
  4. retrieve()       — keyword-based search across chunks
  5. ask_gemini()     — call Google Gemini API with retrieved context
"""

import re
import os
import requests
from decouple import config


# ── 1. Text Extraction ────────────────────────────────────────────────────────

def extract_text_from_file(file_field) -> str:
    """Extract plain text from a Note's FileField (PDF / DOCX / PPTX)."""
    path = file_field.path
    ext  = os.path.splitext(path)[1].lower()

    try:
        if ext == '.pdf':
            return _extract_pdf(path)
        elif ext in ('.doc', '.docx'):
            return _extract_docx(path)
        elif ext in ('.ppt', '.pptx'):
            return _extract_pptx(path)
        else:
            return ''
    except Exception as e:
        print(f'[RAG] Text extraction failed for {path}: {e}')
        return ''


def _extract_pdf(path: str) -> str:
    try:
        import PyPDF2
        text = []
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text.append(t)
        return '\n'.join(text)
    except ImportError:
        # Fallback: try pdfminer if installed
        try:
            from pdfminer.high_level import extract_text
            return extract_text(path)
        except Exception:
            return ''


def _extract_docx(path: str) -> str:
    try:
        from docx import Document
        doc   = Document(path)
        paras = [p.text for p in doc.paragraphs if p.text.strip()]
        return '\n'.join(paras)
    except ImportError:
        return ''


def _extract_pptx(path: str) -> str:
    try:
        from pptx import Presentation
        prs   = Presentation(path)
        lines = []
        for slide in prs.slides:
            for shape in slide.shapes:
                try:
                    if hasattr(shape, 'text') and shape.text and shape.text.strip():
                        lines.append(shape.text.strip())
                except Exception:
                    continue
        return '\n'.join(lines)
    except ImportError:
        return ''
    except Exception as e:
        print(f'[RAG] PPTX error: {e}')
        return ''


# ── 2. Chunking ───────────────────────────────────────────────────────────────

def chunk_text(text: str, size: int = 600, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks of ~size chars."""
    text   = re.sub(r'\s+', ' ', text).strip()
    chunks = []
    start  = 0
    while start < len(text):
        end = min(start + size, len(text))
        # Try to cut at a sentence boundary
        if end < len(text):
            for sep in ['. ', '.\n', '! ', '? ', '\n']:
                idx = text.rfind(sep, start, end)
                if idx != -1:
                    end = idx + len(sep)
                    break
        chunks.append(text[start:end].strip())
        start = end - overlap
    return [c for c in chunks if len(c) > 30]


# ── 3. Index note → NoteChunk table ──────────────────────────────────────────

def index_note(note) -> int:
    """Extract text from note file and save chunks. Returns chunk count."""
    from .models import NoteChunk

    # Clear old chunks
    NoteChunk.objects.filter(note=note).delete()

    text = extract_text_from_file(note.file)
    if not text.strip():
        return 0

    chunks = chunk_text(text)
    objs   = [
        NoteChunk(note=note, chunk_text=chunk, chunk_index=i)
        for i, chunk in enumerate(chunks)
    ]
    NoteChunk.objects.bulk_create(objs)
    return len(objs)


# ── 4. Retrieve relevant chunks ───────────────────────────────────────────────

def retrieve_chunks(query: str, notes_qs, top_k: int = 4) -> list[dict]:
    """
    Keyword-based retrieval from NoteChunk table.
    Returns top_k most relevant chunks with metadata.
    """
    from .models import NoteChunk
    from django.db.models import Q

    # Normalise query — extract meaningful keywords
    stop_words = {'the','a','an','is','are','was','were','what','how','why',
                  'when','where','explain','describe','tell','me','about','please',
                  'can','you','i','my','and','or','in','of','to','do','does'}
    words = [w.lower() for w in re.findall(r'\b\w+\b', query) if w.lower() not in stop_words and len(w) >= 2]

    if not words:
        # No keywords — return most recent chunks
        chunks_qs = NoteChunk.objects.filter(note__in=notes_qs).order_by('-note__uploaded_at')[:top_k]
        return [{'text': c.chunk_text, 'note': c.note.title, 'subject': c.note.subject.name} for c in chunks_qs]

    # Build OR filter across all keywords
    q_filter = Q()
    for word in words:
        q_filter |= Q(chunk_text__icontains=word)

    chunks_qs = NoteChunk.objects.filter(
        note__in=notes_qs
    ).filter(q_filter).select_related('note__subject')

    # Score chunks by keyword hit count
    scored = []
    for chunk in chunks_qs:
        text_lower = chunk.chunk_text.lower()
        score = sum(text_lower.count(w) for w in words)
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:top_k]

    return [
        {
            'text':    c.chunk_text,
            'note':    c.note.title,
            'subject': c.note.subject.name,
            'score':   score,
        }
        for score, c in top
    ]


# ── 5. Gemini API call ────────────────────────────────────────────────────────

GEMINI_API_KEY = config('GEMINI_API_KEY', default='')
GEMINI_URL     = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent'


def ask_gemini(question: str, context_chunks: list[dict], user_name: str = '', role: str = 'student') -> str:
    """
    Send question + retrieved context to Gemini and return the answer.
    Falls back to a structured answer if API key not set.
    """
    if not GEMINI_API_KEY:
        return _fallback_answer(question, context_chunks, user_name)

    # Build context string
    context_parts = []
    for i, c in enumerate(context_chunks, 1):
        context_parts.append(f"[Source {i}: {c['note']} — {c['subject']}]\n{c['text']}")
    context_str = '\n\n'.join(context_parts)

    role_hint = "You are helping a student understand their study material." if role == 'student' else "You are helping a faculty member reference their teaching material."

    prompt = f"""{role_hint}
The user is asking: "{question}"

Here are relevant excerpts from their uploaded study notes:

{context_str}

Instructions:
- Answer the question clearly and concisely using the provided context.
- If the context doesn't fully answer the question, say so and answer from general knowledge.
- Use simple language suitable for engineering students.
- Format with bullet points or numbered steps where helpful.
- Keep the answer under 300 words.
- Address the student by name if provided: {user_name or 'Student'}.
"""

    try:
        res = requests.post(
            f'{GEMINI_URL}?key={GEMINI_API_KEY}',
            json={
                'contents': [{'parts': [{'text': prompt}]}],
                'generationConfig': {'maxOutputTokens': 400, 'temperature': 0.3}
            },
            timeout=15
        )
        if res.status_code == 200:
            data = res.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f'[Gemini] Error {res.status_code}: {res.text[:200]}')
            return _fallback_answer(question, context_chunks, user_name)
    except Exception as e:
        print(f'[Gemini] Exception: {e}')
        return _fallback_answer(question, context_chunks, user_name)


def _fallback_answer(question: str, chunks: list, name: str = '') -> str:
    """Concise structured answer when Gemini is unavailable — shows key content from notes."""
    if not chunks:
        return f"📚 I couldn't find content about **'{question}'** in your uploaded notes.\n\nTry asking about topics your faculty has uploaded — check the **Study Materials** section."

    # Find the best chunk (highest score)
    best = chunks[0]
    text = best['text']

    # Extract the most relevant sentence(s) containing the query keywords
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    query_words = [w.lower() for w in re.findall(r'\b\w{3,}\b', question)]
    scored_sentences = []
    for s in sentences:
        s_lower = s.lower()
        score = sum(1 for w in query_words if w in s_lower)
        if score > 0 and len(s.strip()) > 20:
            scored_sentences.append((score, s.strip()))
    scored_sentences.sort(reverse=True)

    lines = [f"📖 **From {best['note']} ({best['subject']}):**\n"]

    if scored_sentences:
        # Show top 3 most relevant sentences
        shown = [s for _, s in scored_sentences[:3]]
        lines.append('\n'.join(shown))
    else:
        # Show first 300 chars of best chunk
        snippet = text[:300].strip()
        if len(text) > 300:
            snippet += '…'
        lines.append(snippet)

    # If more chunks found, show brief mentions
    if len(chunks) > 1:
        lines.append(f"\n📌 Also found in: {', '.join(c['note'] for c in chunks[1:3])}")

    lines.append(f"\n💡 *Add `GEMINI_API_KEY` in `.env` for full AI explanations.*")
    return '\n'.join(lines)
