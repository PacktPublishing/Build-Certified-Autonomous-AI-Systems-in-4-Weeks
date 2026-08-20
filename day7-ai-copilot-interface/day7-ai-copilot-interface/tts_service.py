"""Optional local text-to-speech helpers with start/stop control."""

from __future__ import annotations

import platform
import shutil
import subprocess
from typing import Optional

MAX_SPOKEN_CHARACTERS = 4000

_speech_process: Optional[subprocess.Popen] = None


def get_tts_command() -> str | None:
    """Return the best local text-to-speech command for this machine."""
    if platform.system() == "Darwin" and shutil.which("say"):
        return "say"

    if shutil.which("espeak"):
        return "espeak"

    return None


def is_tts_available() -> bool:
    """Return True when a supported local text-to-speech command exists."""
    return get_tts_command() is not None


def is_speaking() -> bool:
    """Return True when the app has an active speech process."""
    global _speech_process

    if _speech_process is None:
        return False

    if _speech_process.poll() is None:
        return True

    _speech_process = None
    return False


def stop_speaking() -> str:
    """Stop the current text-to-speech process if one is running."""
    global _speech_process

    stopped = False

    if _speech_process is not None and _speech_process.poll() is None:
        _speech_process.terminate()
        stopped = True

        try:
            _speech_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            _speech_process.kill()

    _speech_process = None

    command = get_tts_command()
    if command in {"say", "espeak"}:
        subprocess.run(["pkill", "-x", command], check=False)
        stopped = True

    if stopped:
        return "Stopped voice playback."

    return "No voice playback was running."


def speak_text(text: str) -> str:
    """Read text aloud using a local text-to-speech command."""
    global _speech_process

    command = get_tts_command()

    if command is None:
        return "No supported local text-to-speech command was found."

    clean_text = text.strip()
    if not clean_text:
        return "There is no text to read aloud."

    stop_speaking()

    spoken_text = clean_text[:MAX_SPOKEN_CHARACTERS]
    _speech_process = subprocess.Popen([command, spoken_text])

    if len(clean_text) > MAX_SPOKEN_CHARACTERS:
        return "Reading the first part of the output aloud."

    return "Reading the output aloud."
