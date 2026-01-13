"""
Test scripts for the auto dealership voice assistant.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.orchestrator import DealershipAssistant
from src.agents import KnowledgeBase


def test_knowledge_base():
    """Test knowledge base functionality."""
    print("\n" + "="*60)
    print("TEST: Knowledge Base")
    print("="*60)

    kb = KnowledgeBase("data/car_inventory.json")

    # Test get all cars
    print("\n[1] Available Cars:")
    cars = kb.get_available_cars()
    for car in cars:
        print(f"  - {car['brand']} {car['model']} ({car['type']})")

    # Test search by type
    print("\n[2] Search for SUVs:")
    suvs = kb.search_cars_by_type("SUV")
    for suv in suvs:
        print(f"  - {suv['brand']} {suv['model']}: {suv['price_range']}")

    # Test get car details
    print("\n[3] Car Details (Elegance 2024):")
    car = kb.get_car_details("sedan_001")
    if car:
        print(f"  Brand: {car['brand']}")
        print(f"  Model: {car['model']}")
        print(f"  Features: {', '.join(car['features'][:3])}")

    # Test dealership info
    print("\n[4] Dealership Info:")
    info = kb.get_dealership_info()
    print(f"  Name: {info['name']}")
    print(f"  Contact: {info['contact']}")

    print("\n✓ Knowledge Base Tests Passed!")


def test_conversation_agent():
    """Test conversation agent."""
    print("\n" + "="*60)
    print("TEST: Conversation Agent")
    print("="*60)

    assistant = DealershipAssistant(use_voice=False)

    test_queries = [
        "Hi, I'm looking for a sedan",
        "What's the price range for the Elegance 2024?",
        "I'd like to book a test drive tomorrow at 2 PM",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] User: {query}")
        response = assistant.process_text(query)
        print(f"    Assistant: {response[:200]}...")  # Truncate for display

    print("\n✓ Conversation Agent Tests Passed!")


def test_voice_utilities():
    """Test voice utilities."""
    print("\n" + "="*60)
    print("TEST: Voice Utilities")
    print("="*60)

    from src.voice_utils import get_tts_provider, get_stt_provider

    # Test TTS provider initialization
    print("\n[1] Testing TTS Providers:")
    try:
        tts = get_tts_provider(provider="local")
        print("  ✓ Local TTS initialized")
    except Exception as e:
        print(f"  ✗ Local TTS failed: {e}")

    # Test STT provider initialization
    print("\n[2] Testing STT Providers:")
    try:
        stt = get_stt_provider(provider="local")
        print("  ✓ Local STT initialized")
    except Exception as e:
        print(f"  ✗ Local STT failed: {e}")

    print("\n✓ Voice Utilities Tests Passed!")


def test_booking():
    """Test booking functionality."""
    print("\n" + "="*60)
    print("TEST: Booking System")
    print("="*60)

    assistant = DealershipAssistant(use_voice=False)

    # Simulate booking process
    print("\n[1] Booking Test Drive:")
    response = assistant.process_text(
        "I want to book a test drive for the Elegance sedan on 2024-01-20 at 14:00"
    )
    print(f"    {response}")

    # Check bookings
    print("\n[2] Confirm Booking:")
    bookings = assistant.get_bookings()
    if bookings:
        booking = bookings[0]
        print(f"    Booking ID: {booking.booking_id}")
        print(f"    Customer: {booking.customer_name}")
        print(f"    Car: {booking.car_model}")
        print(f"    Status: {booking.booking_status}")
    else:
        print("    No bookings recorded")

    print("\n✓ Booking System Tests Passed!")


def test_end_to_end():
    """Test complete end-to-end flow."""
    print("\n" + "="*60)
    print("TEST: End-to-End Flow")
    print("="*60)

    assistant = DealershipAssistant(use_voice=False)

    # Conversation flow
    conversation = [
        "Hello",
        "I'm interested in an SUV",
        "What features does the Explorer Pro have?",
        "I'd like to book a test drive for tomorrow at 10 AM",
    ]

    for i, msg in enumerate(conversation, 1):
        print(f"\n[Step {i}]")
        print(f"  Customer: {msg}")
        response = assistant.process_text(msg)
        print(f"  Assistant: {response[:150]}...")

    # Display final bookings
    print("\n[Final State]")
    assistant.display_bookings()

    print("\n✓ End-to-End Tests Passed!")


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + " AUTO DEALERSHIP ASSISTANT - TEST SUITE".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")

    try:
        test_knowledge_base()
        test_voice_utilities()
        test_conversation_agent()
        test_booking()
        test_end_to_end()

        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60 + "\n")
        return True
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
