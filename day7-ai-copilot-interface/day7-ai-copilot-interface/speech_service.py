"""Helpers for converting recorded microphone audio into text."""

from __future__ import annotations

import tempfile
from pathlib import Path

import speech_recognition as sr


class SpeechToTextError(Exception):
    """Raised when voice input cannot be converted to text."""


def transcribe_audio_file(audio_file) -> str:
    """Convert a Streamlit audio input file into text."""
    suffix = Path(audio_file.name).suffix or ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(audio_file.getvalue())
        temp_path = temp_file.name

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)

        transcript = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError as exc:
        raise SpeechToTextError(
            "I could not understand the recording. Please try again or type the request."
        ) from exc
    except sr.RequestError as exc:
        raise SpeechToTextError(
            "Speech recognition is not available right now. Please check your internet connection or type the request."
        ) from exc
    except Exception as exc:
        raise SpeechToTextError(f"Could not process the audio recording: {exc}") from exc

    return transcript.strip()
