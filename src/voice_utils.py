"""
Voice utilities for Speech-to-Text and Text-to-Speech operations.
Supports multiple providers: OpenAI, Azure, Google Cloud, and local (pyttsx3).
"""

import os
from abc import ABC, abstractmethod
from typing import Optional
import asyncio
from enum import Enum

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    speechsdk = None

try:
    from google.cloud import speech_v1, texttospeech
except ImportError:
    speech_v1 = None
    texttospeech = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

import speech_recognition as sr


class VoiceProvider(str, Enum):
    """Available voice providers."""
    OPENAI = "openai"
    AZURE = "azure"
    GOOGLE = "google"
    LOCAL = "local"


class TextToSpeech(ABC):
    """Abstract base class for TTS implementations."""

    @abstractmethod
    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        pass

    @abstractmethod
    async def speak_async(self, text: str) -> None:
        """Async version of speak."""
        pass


class SpeechToText(ABC):
    """Abstract base class for STT implementations."""

    @abstractmethod
    def listen(self) -> Optional[str]:
        """Listen to audio and convert to text."""
        pass

    @abstractmethod
    async def listen_async(self) -> Optional[str]:
        """Async version of listen."""
        pass


class OpenAITTS(TextToSpeech):
    """OpenAI Text-to-Speech implementation."""

    def __init__(self, api_key: str, voice: str = "nova"):
        if not OpenAI:
            raise ImportError("openai package is required. Install with: pip install openai")
        self.client = OpenAI(api_key=api_key)
        self.voice = voice

    def speak(self, text: str) -> None:
        """Convert text to speech using OpenAI API."""
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=text,
        )
        # Play audio (simplified - in production would save/stream)
        print(f"[TTS Output]: {text}")

    async def speak_async(self, text: str) -> None:
        """Async wrapper for OpenAI TTS."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.speak, text)


class AzureTTS(TextToSpeech):
    """Azure Cognitive Services Text-to-Speech implementation."""

    def __init__(self, api_key: str, region: str):
        if not speechsdk:
            raise ImportError("azure-cognitiveservices-speech is required")
        self.speech_config = speechsdk.SpeechConfig(
            subscription=api_key, region=region
        )
        self.speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

    def speak(self, text: str) -> None:
        """Convert text to speech using Azure."""
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
        synthesizer.speak_text_async(text).get()

    async def speak_async(self, text: str) -> None:
        """Async wrapper for Azure TTS."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.speak, text)


class LocalTTS(TextToSpeech):
    """Local Text-to-Speech implementation using pyttsx3."""

    def __init__(self):
        if not pyttsx3:
            raise ImportError("pyttsx3 is required. Install with: pip install pyttsx3")
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.engine.setProperty("volume", 0.9)

    def speak(self, text: str) -> None:
        """Convert text to speech locally."""
        print(f"[TTS Output]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    async def speak_async(self, text: str) -> None:
        """Async wrapper for local TTS."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.speak, text)


class GoogleSTT(SpeechToText):
    """Google Cloud Speech-to-Text implementation."""

    def __init__(self, credentials_path: str):
        if not speech_v1:
            raise ImportError("google-cloud-speech is required")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = speech_v1.SpeechClient()

    def listen(self) -> Optional[str]:
        """Listen to audio and convert to text using Google."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=10)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return None

    async def listen_async(self) -> Optional[str]:
        """Async wrapper for Google STT."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.listen)


class AzureSTT(SpeechToText):
    """Azure Cognitive Services Speech-to-Text implementation."""

    def __init__(self, api_key: str, region: str):
        if not speechsdk:
            raise ImportError("azure-cognitiveservices-speech is required")
        self.speech_config = speechsdk.SpeechConfig(
            subscription=api_key, region=region
        )

    def listen(self) -> Optional[str]:
        """Listen to audio and convert to text using Azure."""
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config
        )
        result = speech_recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        return None

    async def listen_async(self) -> Optional[str]:
        """Async wrapper for Azure STT."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.listen)


class OpenAISTT(SpeechToText):
    """OpenAI Whisper Speech-to-Text implementation."""

    def __init__(self, api_key: str):
        if not OpenAI:
            raise ImportError("openai package is required")
        self.client = OpenAI(api_key=api_key)

    def listen(self) -> Optional[str]:
        """Listen to audio and convert to text using OpenAI Whisper."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=10)
            except sr.RequestError:
                return None

        # Save audio to temporary file and send to OpenAI
        try:
            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())

            with open("temp_audio.wav", "rb") as f:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1", file=f
                )
            return transcript.text
        except Exception:
            return None
        finally:
            if os.path.exists("temp_audio.wav"):
                os.remove("temp_audio.wav")

    async def listen_async(self) -> Optional[str]:
        """Async wrapper for OpenAI STT."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.listen)


class LocalSTT(SpeechToText):
    """Local Speech-to-Text using Google's free API."""

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self) -> Optional[str]:
        """Listen to audio and convert to text locally."""
        with sr.Microphone() as source:
            try:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=10)
                print("Processing audio...")
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None

    async def listen_async(self) -> Optional[str]:
        """Async wrapper for local STT."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.listen)


def get_tts_provider(
    provider: str = None,
    api_key: str = None,
    azure_region: str = None,
) -> TextToSpeech:
    """Factory function to get TTS provider."""
    provider = provider or os.getenv("VOICE_PROVIDER", "local").lower()

    if provider == VoiceProvider.OPENAI:
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not provided")
        return OpenAITTS(api_key=api_key)
    elif provider == VoiceProvider.AZURE:
        api_key = api_key or os.getenv("AZURE_SPEECH_KEY")
        region = azure_region or os.getenv("AZURE_SPEECH_REGION")
        if not api_key or not region:
            raise ValueError("Azure credentials not provided")
        return AzureTTS(api_key=api_key, region=region)
    elif provider == VoiceProvider.GOOGLE:
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not creds_path:
            raise ValueError("Google credentials path not provided")
        return GoogleSTT(credentials_path=creds_path)
    else:
        return LocalTTS()


def get_stt_provider(
    provider: str = None,
    api_key: str = None,
    azure_region: str = None,
    google_creds_path: str = None,
) -> SpeechToText:
    """Factory function to get STT provider."""
    provider = provider or os.getenv("VOICE_PROVIDER", "local").lower()

    if provider == VoiceProvider.OPENAI:
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not provided")
        return OpenAISTT(api_key=api_key)
    elif provider == VoiceProvider.AZURE:
        api_key = api_key or os.getenv("AZURE_SPEECH_KEY")
        region = azure_region or os.getenv("AZURE_SPEECH_REGION")
        if not api_key or not region:
            raise ValueError("Azure credentials not provided")
        return AzureSTT(api_key=api_key, region=region)
    elif provider == VoiceProvider.GOOGLE:
        creds_path = google_creds_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not creds_path:
            raise ValueError("Google credentials path not provided")
        return GoogleSTT(credentials_path=creds_path)
    else:
        return LocalSTT()
