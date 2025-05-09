# buddy/api_views.py
import openai
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from io import BytesIO

@csrf_exempt
def transcribe_audio(request):
    if request.method == "POST" and request.FILES.get("audio_file"):
        uploaded_file = request.FILES["audio_file"]

        try:
            # Set up OpenAI client
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

            # Read uploaded audio into memory
            audio_bytes = BytesIO(uploaded_file.read())
            audio_bytes.name = uploaded_file.name  # add filename for OpenAI API

            # Transcribe using Whisper
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=(audio_bytes.name, audio_bytes),  # tuple: (filename, file)
                response_format="text"
            )

            return JsonResponse({"transcription": response})

        except Exception as e:
            print("TRANSCRIPTION ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)