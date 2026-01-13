"""
Multi-agent orchestrator for auto dealership voice assistant.
Coordinates between Conversation, Knowledge, and Booking agents.
"""

import os
from typing import Optional, Dict, Any
import asyncio
from dotenv import load_dotenv

from src.agents import (
    ConversationAgent,
    KnowledgeAgent,
    BookingAgent,
    DealershipTools,
    KnowledgeBase,
)
from src.voice_utils import (
    get_stt_provider,
    get_tts_provider,
    SpeechToText,
    TextToSpeech,
)

# Load environment variables
load_dotenv()


class DealershipAssistant:
    """Main orchestrator for the auto dealership voice assistant."""

    def __init__(
        self,
        use_voice: bool = False,
        voice_provider: str = "local",
        inventory_path: str = "data/car_inventory.json",
        model_name: str = "gpt-4",
    ):
        """
        Initialize the dealership assistant.

        Args:
            use_voice: Enable voice interaction
            voice_provider: Voice provider to use ('openai', 'azure', 'google', 'local')
            inventory_path: Path to car inventory JSON file
            model_name: LLM model name to use
        """
        self.use_voice = use_voice
        self.voice_provider = voice_provider
        self.model_name = model_name
        
        # Initialize knowledge base
        self.knowledge_base = KnowledgeBase(inventory_path)
        
        # Initialize tools
        self.tools = DealershipTools(self.knowledge_base).get_tools()
        
        # Initialize agents
        self.conversation_agent = ConversationAgent(self.tools, model_name)
        self.knowledge_agent = KnowledgeAgent(self.knowledge_base)
        self.booking_agent = BookingAgent(self.knowledge_base)
        
        # Initialize voice components if enabled
        self.stt: Optional[SpeechToText] = None
        self.tts: Optional[TextToSpeech] = None
        
        if self.use_voice:
            try:
                self.stt = get_stt_provider(provider=voice_provider)
                self.tts = get_tts_provider(provider=voice_provider)
                print("✓ Voice components initialized successfully")
            except Exception as e:
                print(f"⚠ Warning: Could not initialize voice components: {e}")
                self.use_voice = False

    def process_text(self, user_input: str) -> str:
        """
        Process text input and return response from conversation agent.

        Args:
            user_input: User's text input

        Returns:
            Agent's response
        """
        return self.conversation_agent.process_input(user_input)

    async def process_text_async(self, user_input: str) -> str:
        """Async version of process_text."""
        return await asyncio.to_thread(self.process_text, user_input)

    async def listen(self) -> Optional[str]:
        """
        Listen for voice input and convert to text.

        Returns:
            Transcribed text or None if no speech detected
        """
        if not self.stt:
            return None
        return await self.stt.listen_async()

    async def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.

        Args:
            text: Text to convert to speech
        """
        if not self.tts:
            print(f"[Output]: {text}")
            return
        await self.tts.speak_async(text)

    async def run_voice_interaction(self) -> None:
        """Run interactive voice-based conversation."""
        if not self.use_voice or not self.stt or not self.tts:
            print("Voice interaction is not enabled. Run with --voice flag.")
            return

        print("\n" + "="*60)
        print("AUTO DEALERSHIP VOICE ASSISTANT")
        print("="*60)
        
        # Greeting
        greeting = (
            "Hello! Welcome to Premium Auto Dealership. I'm here to help you find "
            "the perfect car and book a test drive. What brings you in today?"
        )
        print(f"\n[Assistant]: {greeting}")
        await self.speak(greeting)

        # Main conversation loop
        while True:
            print("\nListening...")
            user_input = await self.listen()

            if not user_input:
                print("Sorry, I didn't catch that. Could you please repeat?")
                await self.speak("Sorry, I didn't catch that. Could you please repeat?")
                continue

            print(f"\n[Customer]: {user_input}")

            # Check for exit commands
            if any(word in user_input.lower() for word in ["bye", "goodbye", "exit", "quit"]):
                farewell = (
                    "Thank you for visiting Premium Auto Dealership! "
                    "We look forward to seeing you soon. Goodbye!"
                )
                print(f"\n[Assistant]: {farewell}")
                await self.speak(farewell)
                break

            # Process input
            response = await self.process_text_async(user_input)
            print(f"\n[Assistant]: {response}")
            await self.speak(response)

    def run_text_interaction(self) -> None:
        """Run interactive text-based conversation."""
        print("\n" + "="*60)
        print("AUTO DEALERSHIP TEXT ASSISTANT")
        print("="*60)
        
        # Greeting
        greeting = (
            "Hello! Welcome to Premium Auto Dealership. I'm here to help you find "
            "the perfect car and book a test drive. What brings you in today? "
            "(Type 'quit' to exit)"
        )
        print(f"\n[Assistant]: {greeting}\n")

        # Main conversation loop
        while True:
            try:
                user_input = input("[You]: ").strip()

                if not user_input:
                    continue

                # Check for exit commands
                if user_input.lower() in ["bye", "goodbye", "exit", "quit"]:
                    farewell = (
                        "Thank you for visiting Premium Auto Dealership! "
                        "We look forward to seeing you soon. Goodbye!"
                    )
                    print(f"\n[Assistant]: {farewell}")
                    break

                # Process input
                response = self.process_text(user_input)
                print(f"\n[Assistant]: {response}\n")

            except KeyboardInterrupt:
                print("\n\nAssistant shutting down...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def get_bookings(self) -> list:
        """Get all bookings made during this session."""
        return self.knowledge_base.bookings

    def display_bookings(self) -> None:
        """Display all bookings made during this session."""
        bookings = self.get_bookings()
        if not bookings:
            print("\nNo bookings made yet.")
            return

        print("\n" + "="*60)
        print("TEST DRIVE BOOKINGS")
        print("="*60)
        for booking in bookings:
            print(f"\nBooking ID: {booking.booking_id}")
            print(f"Customer: {booking.customer_name}")
            print(f"Phone: {booking.customer_phone}")
            print(f"Car: {booking.car_model}")
            print(f"Date: {booking.preferred_date} at {booking.preferred_time}")
            print(f"Duration: {booking.test_drive_duration} minutes")
            print(f"Status: {booking.booking_status}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Auto Dealership Voice Assistant"
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Enable voice interaction (requires microphone)",
    )
    parser.add_argument(
        "--voice-provider",
        default="local",
        choices=["openai", "azure", "google", "local"],
        help="Voice provider to use",
    )
    parser.add_argument(
        "--inventory",
        default="data/car_inventory.json",
        help="Path to car inventory JSON file",
    )
    parser.add_argument(
        "--model",
        default="gpt-4",
        help="LLM model name to use",
    )

    args = parser.parse_args()

    # Initialize assistant
    assistant = DealershipAssistant(
        use_voice=args.voice,
        voice_provider=args.voice_provider,
        inventory_path=args.inventory,
        model_name=args.model,
    )

    # Run interaction
    if args.voice:
        asyncio.run(assistant.run_voice_interaction())
    else:
        assistant.run_text_interaction()

    # Display bookings
    assistant.display_bookings()


if __name__ == "__main__":
    main()
