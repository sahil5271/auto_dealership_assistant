#!/usr/bin/env python
"""
Entry point for the Auto Dealership Voice Assistant.
Provides both interactive CLI and API server modes.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from src.orchestrator import DealershipAssistant
import argparse
import asyncio


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Auto Dealership Voice Assistant - Multi-Agent Test Drive Booking System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start text-based conversation
  python main.py

  # Start voice interaction
  python main.py --voice --voice-provider local

  # Start REST API server
  python main.py --api

  # Run tests
  python main.py --test
        """
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
        help="Voice provider to use (default: local)",
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start REST API server instead of CLI",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test suite",
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
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for API server (default: 8000)",
    )

    args = parser.parse_args()

    # Run tests
    if args.test:
        from tests.test_assistant import run_all_tests
        success = run_all_tests()
        sys.exit(0 if success else 1)

    # Start API server
    if args.api:
        import uvicorn
        print("\n" + "="*60)
        print("Starting Auto Dealership Assistant API Server")
        print("="*60)
        print(f"\n📡 API Server running at http://localhost:{args.port}")
        print(f"📖 Swagger Docs at http://localhost:{args.port}/docs")
        print(f"🎯 ReDoc at http://localhost:{args.port}/redoc")
        print("\nPress Ctrl+C to stop the server\n")

        uvicorn.run(
            "src.api:app",
            host="0.0.0.0",
            port=args.port,
            reload=False,
        )
        return

    # Initialize assistant
    print("\n" + "="*70)
    print(" "*15 + "🚗 AUTO DEALERSHIP VOICE ASSISTANT 🎤")
    print(" "*10 + "Multi-Agent Test Drive Booking System v1.0.0")
    print("="*70)

    assistant = DealershipAssistant(
        use_voice=args.voice,
        voice_provider=args.voice_provider,
        inventory_path=args.inventory,
        model_name=args.model,
    )

    # Run interaction
    try:
        if args.voice:
            asyncio.run(assistant.run_voice_interaction())
        else:
            assistant.run_text_interaction()
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using Auto Dealership Assistant!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        # Display bookings
        assistant.display_bookings()


if __name__ == "__main__":
    main()
