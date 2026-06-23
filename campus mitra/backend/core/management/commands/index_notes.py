"""
Management command: python manage.py index_notes

Re-indexes all existing uploaded notes into NoteChunk table for RAG search.
Run this once after adding RAG support to index previously uploaded notes.
"""
from django.core.management.base import BaseCommand
from core.models import Note
from core.rag_utils import index_note


class Command(BaseCommand):
    help = 'Index all uploaded notes for RAG-based AI search'

    def handle(self, *args, **options):
        notes = Note.objects.all()
        self.stdout.write(f'Indexing {notes.count()} notes...\n')
        total_chunks = 0
        for note in notes:
            try:
                count = index_note(note)
                total_chunks += count
                self.stdout.write(f'  ✅ {note.title} ({note.subject.name}) — {count} chunks')
            except Exception as e:
                self.stdout.write(f'  ❌ {note.title} — failed: {e}')
        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Indexed {total_chunks} chunks from {notes.count()} notes.'))
