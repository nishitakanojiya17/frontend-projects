import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmitra.settings')
django.setup()

from core.models import Note, NoteChunk
from core.rag_utils import extract_text_from_file

print(f"Total Notes: {Note.objects.count()}")
for note in Note.objects.all():
    chunks = NoteChunk.objects.filter(note=note).count()
    print(f"Note: {note.title} (ID: {note.id}) - Chunks in DB: {chunks}")
    if chunks == 0:
        print(f"  Attempting text extraction for: {note.file.name}")
        text = extract_text_from_file(note.file)
        print(f"  Extracted text length: {len(text)}")
        if text.strip():
            snippet = text[:200].encode('ascii', errors='ignore').decode('ascii')
            print(f"  Text snippet: {snippet}")
        else:
            print(f"  WARNING: Extracted text is empty!")

print(f"Total NoteChunks in DB: {NoteChunk.objects.count()}")
