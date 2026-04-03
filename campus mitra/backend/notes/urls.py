from django.urls import path
from . import views

urlpatterns = [
    path('notes/',              views.notes_list,   name='notes_list'),
    path('notes/upload/',       views.upload_note,  name='upload_note'),
    path('notes/delete/<int:pk>/', views.delete_note, name='delete_note'),
]
