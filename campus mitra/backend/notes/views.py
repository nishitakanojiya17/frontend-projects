from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note
from .forms import NoteUploadForm


@login_required
def notes_list(request):
    """Students see notes for their branch + ALL-branch notes."""
    subject = request.GET.get('subject', '')
    branch  = request.GET.get('branch', '')

    notes = Note.objects.filter(is_active=True)

    # Auto-filter by student's branch
    if request.user.role == 'student':
        profile = getattr(request.user, 'student_profile', None)
        if profile:
            notes = notes.filter(branch__in=[profile.branch, 'ALL'])

    # Manual branch filter (for faculty/admin)
    if branch and request.user.role != 'student':
        notes = notes.filter(branch=branch)

    if subject:
        notes = notes.filter(subject=subject)

    return render(request, 'notes/notes_list.html', {
        'notes': notes,
        'subject_filter': subject,
        'branch_filter': branch,
        'subjects': Note.subject.field.choices,
        'branches': Note.branch.field.choices,
    })


@login_required
def upload_note(request):
    """Faculty only — upload a new note."""
    if request.user.role != 'faculty':
        messages.error(request, 'Only faculty can upload notes.')
        return redirect('notes_list')

    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully.')
            return redirect('notes_list')
    else:
        form = NoteUploadForm()

    return render(request, 'notes/upload_note.html', {'form': form})


@login_required
def delete_note(request, pk):
    """Faculty can delete their own notes."""
    note = get_object_or_404(Note, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        note.is_active = False
        note.save()
        messages.success(request, 'Note removed.')
    return redirect('notes_list')
