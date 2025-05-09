# buddy/models.py

from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# --- Renamed this class ---
class Note(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notes' # Updated related_name
    )
    # --- Updated related_name ---
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255, blank=True)
    transcript_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # --- Updated related_name ---
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='notes'
    )

    def __str__(self):
        # Consider changing this if 'Note' implies something different now
        return self.title or f"Note created {self.created_at.strftime('%Y-%m-%d')}"