from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import Note, Event, Tag
from .forms import NoteForm
import json
import copy
import requests
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def join(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'join.html', {'form': form})

@login_required
def my_notes(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_notes.html', {'notes': notes})

@login_required
def view_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    return render(request, 'view_note.html', {'note': note})

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user

            event_title = request.POST.get("event_text", "").strip()
            if event_title:
                event, _ = Event.objects.get_or_create(title=event_title, user=request.user)
                note.event = event
            else:
                note.event = None
            
            note.save()

            note.tags.clear() 
            tag_names = [t.strip() for t in request.POST.get("tags_text", "").split(",") if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                note.tags.add(tag)

            messages.success(request, "Note updated successfully.")
            return redirect('my_notes')
    else:
        form = NoteForm(instance=note, initial={
            'event_text': note.event.title if note.event else '',
            'tags_text': ", ".join(tag.name for tag in note.tags.all())
        })
    return render(request, 'edit_note.html', {'form': form, 'note': note})

@require_POST
@login_required
def save_transcript(request):
    print("DEBUG: save_transcript view triggered")
    title = request.POST.get('title', '').strip()
    event_title = request.POST.get('event', '').strip()
    tags_text = request.POST.get('tags', '').strip()
    transcript_text = request.POST.get('transcript_text', '').strip()

    if not title or not transcript_text:
        messages.error(request, "Title and Transcript cannot be empty.")
        return redirect('home')

    event_instance = None
    if event_title:
        event_instance, _ = Event.objects.get_or_create(user=request.user, title=event_title)

    note = Note.objects.create(
        user=request.user,
        title=title,
        transcript_text=transcript_text,
        event=event_instance
    )

    tag_names = [tag_name.strip() for tag_name in tags_text.split(',') if tag_name.strip()]
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        note.tags.add(tag)

    messages.success(request, "Transcript saved successfully.")
    return redirect('my_notes')

@require_POST
@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    messages.success(request, "Note deleted successfully.")
    return redirect('my_notes')

# def server_info(request):
#     try:
#         server_geodata_response = requests.get('https://ipwhois.app/json/')
#         server_geodata_response.raise_for_status()
#         server_geodata = server_geodata_response.json()
#     except requests.exceptions.RequestException as e:
#         server_geodata = {"error": f"Could not retrieve geolocation data: {str(e)}"}
#     except json.JSONDecodeError:
#         server_geodata = {"error": "Could not decode geolocation JSON response."}

#     settings_dump = {}
#     for attr in dir(settings):
#         if attr.isupper(): 
#             try:
#                 json.dumps(getattr(settings, attr)) 
#                 settings_dump[attr] = getattr(settings, attr)
#             except TypeError:
#                 settings_dump[attr] = str(getattr(settings, attr))

#     response_content = f"Server Geolocation Data:\n{json.dumps(server_geodata, indent=2)}\n\nDjango Settings (Uppercase):\n{json.dumps(settings_dump, indent=2, default=str)}"
    
#     return HttpResponse(response_content, content_type="text/plain")

def server_info(request):
    server_geodata = requests.get('https://ipwhois.app/json/').json()
    settings_dump = settings.__dict__
    return HttpResponse("{}{}".format(server_geodata, settings_dump))