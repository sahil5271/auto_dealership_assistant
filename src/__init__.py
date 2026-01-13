"""Auto Dealership Assistant - Multi-Agent Voice System"""

__version__ = "1.0.0"
__author__ = "Auto Dealership Team"

from src.orchestrator import DealershipAssistant
from src.agents import (
    ConversationAgent,
    KnowledgeAgent,
    BookingAgent,
    KnowledgeBase,
    TestDriveBooking,
)
from src.voice_utils import (
    get_stt_provider,
    get_tts_provider,
    VoiceProvider,
)

__all__ = [
    "DealershipAssistant",
    "ConversationAgent",
    "KnowledgeAgent",
    "BookingAgent",
    "KnowledgeBase",
    "TestDriveBooking",
    "get_stt_provider",
    "get_tts_provider",
    "VoiceProvider",
]
