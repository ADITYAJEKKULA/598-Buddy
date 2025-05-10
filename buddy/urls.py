from django.urls import path
from . import views, api_views
from django.contrib.auth import views as auth_views
from buddy import views as buddy_views

urlpatterns = [

    path('', views.home, name='home'),

    path('join/', views.join, name='join'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('about/', views.about, name='about'),

    path('my-notes/', views.my_notes, name='my_notes'),

    path('notes/view/<int:note_id>/', views.view_note, name='view_note'),

    path('notes/edit/<int:note_id>/', views.edit_note, name='edit_note'),

    # New URL pattern for deleting notes
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),

    path('save-transcript/', views.save_transcript, name='save_transcript'),

    # API endpoint for transcription
    path('api/transcribe/', api_views.transcribe_audio, name='transcribe_audio'),

    # Redundant API URL - you can remove one of these if they are the same
    # path("api/transcribe/", api_views.transcribe_audio, name="whisper_transcribe"),
    # path('server_info/', views.server_info, name='server_info'),

    path('server_info/', views.server_info),

    path('events/', views.notes_by_event, name='notes_by_event'),

    path('notes/download/<int:note_id>/', views.download_note, name='download_note'),


]