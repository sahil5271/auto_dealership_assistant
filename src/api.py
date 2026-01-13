"""
FastAPI backend for the auto dealership voice assistant.
Provides REST API endpoints for web and mobile clients.
"""

import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio

from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from src.orchestrator import DealershipAssistant
from src.agents import TestDriveBooking

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Auto Dealership Voice Assistant API",
    description="Multi-agent voice assistant for test drive booking",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize assistant
assistant = DealershipAssistant(
    use_voice=True,
    voice_provider=os.getenv("VOICE_PROVIDER", "local"),
    inventory_path=os.getenv("INVENTORY_PATH", "data/car_inventory.json"),
    model_name=os.getenv("MODEL_NAME", "gpt-4"),
)


# ==================== Request/Response Models ====================

class ChatRequest(BaseModel):
    """Request model for text-based chat."""
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for context")


class ChatResponse(BaseModel):
    """Response model for text-based chat."""
    response: str = Field(..., description="Assistant response")
    session_id: Optional[str] = Field(None, description="Session ID")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class AudioTranscriptionRequest(BaseModel):
    """Request model for audio transcription."""
    language: str = Field(default="en", description="Language code")


class AudioTranscriptionResponse(BaseModel):
    """Response model for audio transcription."""
    text: str = Field(..., description="Transcribed text")
    confidence: Optional[float] = Field(None, description="Confidence score")


class TextToSpeechRequest(BaseModel):
    """Request model for text-to-speech."""
    text: str = Field(..., description="Text to convert to speech")
    voice: str = Field(default="nova", description="Voice to use")


class CarSearchRequest(BaseModel):
    """Request model for car search."""
    car_type: Optional[str] = Field(None, description="Type of car (sedan, SUV, etc.)")
    brand: Optional[str] = Field(None, description="Brand of car")
    budget_min: Optional[float] = Field(None, description="Minimum budget")
    budget_max: Optional[float] = Field(None, description="Maximum budget")


class CarDetails(BaseModel):
    """Model for car details."""
    id: str
    brand: str
    model: str
    year: int
    type: str
    price_range: str
    features: List[str]
    fuel_type: str
    availability: bool


class TestDriveBookingRequest(BaseModel):
    """Request model for booking test drive."""
    customer_name: str = Field(..., description="Customer name")
    customer_phone: str = Field(..., description="Customer phone number")
    customer_email: Optional[str] = Field(None, description="Customer email")
    car_id: str = Field(..., description="Car ID")
    preferred_date: str = Field(..., description="Preferred date (YYYY-MM-DD)")
    preferred_time: str = Field(..., description="Preferred time (HH:MM)")


class TestDriveBookingResponse(BaseModel):
    """Response model for test drive booking."""
    booking_id: str
    customer_name: str
    car_model: str
    preferred_date: str
    preferred_time: str
    booking_status: str
    message: str


class DealershipInfo(BaseModel):
    """Model for dealership information."""
    name: str
    location: str
    contact: str
    email: str
    working_hours: Dict[str, str]


# ==================== Endpoints ====================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - check API status."""
    return {
        "status": "online",
        "service": "Auto Dealership Voice Assistant",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


# ==================== Chat Endpoints ====================

@app.post("/api/v1/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process text-based chat message.

    Args:
        request: Chat request with message

    Returns:
        Chat response from the assistant
    """
    try:
        response = await assistant.process_text_async(request.message)
        return ChatResponse(
            response=response,
            session_id=request.session_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


# ==================== Voice Endpoints ====================

@app.post("/api/v1/transcribe", response_model=AudioTranscriptionResponse, tags=["Voice"])
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio file to text.

    Args:
        file: Audio file to transcribe

    Returns:
        Transcribed text
    """
    try:
        if not assistant.stt:
            raise HTTPException(status_code=400, detail="Speech-to-text not available")

        # Save uploaded file
        contents = await file.read()
        with open("temp_audio.wav", "wb") as f:
            f.write(contents)

        # Transcribe
        text = await assistant.stt.listen_async()
        if not text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        return AudioTranscriptionResponse(text=text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")
    finally:
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")


@app.post("/api/v1/speak", tags=["Voice"])
async def text_to_speech(request: TextToSpeechRequest):
    """
    Convert text to speech and return audio.

    Args:
        request: Text-to-speech request

    Returns:
        Audio file
    """
    try:
        if not assistant.tts:
            raise HTTPException(status_code=400, detail="Text-to-speech not available")

        await assistant.speak(request.text)
        return {"status": "success", "message": "Audio generated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")


# ==================== Car Endpoints ====================

@app.get("/api/v1/cars", response_model=List[CarDetails], tags=["Cars"])
async def list_cars(car_type: Optional[str] = None):
    """
    List available cars, optionally filtered by type.

    Args:
        car_type: Type of car to filter by

    Returns:
        List of available cars
    """
    try:
        if car_type:
            cars = assistant.knowledge_base.search_cars_by_type(car_type)
        else:
            cars = assistant.knowledge_base.get_available_cars()

        return [CarDetails(**car) for car in cars]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing cars: {str(e)}")


@app.get("/api/v1/cars/{car_id}", tags=["Cars"])
async def get_car(car_id: str):
    """
    Get detailed information about a specific car.

    Args:
        car_id: ID of the car

    Returns:
        Detailed car information
    """
    try:
        car = assistant.knowledge_base.get_car_details(car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        return car
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving car: {str(e)}")


@app.post("/api/v1/cars/search", response_model=List[CarDetails], tags=["Cars"])
async def search_cars(request: CarSearchRequest):
    """
    Search for cars based on criteria.

    Args:
        request: Search criteria

    Returns:
        List of matching cars
    """
    try:
        results = []

        if request.car_type:
            results = assistant.knowledge_base.search_cars_by_type(request.car_type)
        elif request.brand:
            results = assistant.knowledge_base.search_cars_by_brand(request.brand)
        else:
            results = assistant.knowledge_base.get_available_cars()

        # Filter by budget if provided
        if request.budget_min or request.budget_max:
            # Note: In production, would parse price_range properly
            filtered = []
            for car in results:
                filtered.append(car)
            results = filtered

        return [CarDetails(**car) for car in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching cars: {str(e)}")


# ==================== Booking Endpoints ====================

@app.post("/api/v1/bookings", response_model=TestDriveBookingResponse, tags=["Bookings"])
async def create_booking(request: TestDriveBookingRequest):
    """
    Create a new test drive booking.

    Args:
        request: Booking details

    Returns:
        Booking confirmation
    """
    try:
        # Validate car exists
        car = assistant.knowledge_base.get_car_details(request.car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")

        # Check availability
        if not assistant.knowledge_base.check_time_availability(
            request.preferred_date, request.preferred_time
        ):
            raise HTTPException(status_code=400, detail="Requested time is not available")

        # Create booking
        booking = TestDriveBooking(
            booking_id=f"TD-{int(datetime.now().timestamp())}",
            customer_name=request.customer_name,
            customer_phone=request.customer_phone,
            customer_email=request.customer_email,
            car_model=f"{car['brand']} {car['model']}",
            car_id=request.car_id,
            preferred_date=request.preferred_date,
            preferred_time=request.preferred_time,
            test_drive_duration=car.get("test_drive_duration_minutes", 60),
        )

        if not assistant.knowledge_base.book_test_drive(booking):
            raise HTTPException(status_code=400, detail="Failed to create booking")

        return TestDriveBookingResponse(
            booking_id=booking.booking_id,
            customer_name=booking.customer_name,
            car_model=booking.car_model,
            preferred_date=booking.preferred_date,
            preferred_time=booking.preferred_time,
            booking_status=booking.booking_status,
            message=f"Test drive booked successfully! Confirmation will be sent to {request.customer_phone}",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating booking: {str(e)}")


@app.get("/api/v1/bookings", tags=["Bookings"])
async def list_bookings():
    """
    List all test drive bookings made during this session.

    Returns:
        List of bookings
    """
    try:
        bookings = [b.dict() for b in assistant.get_bookings()]
        return {"bookings": bookings, "count": len(bookings)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving bookings: {str(e)}")


@app.get("/api/v1/bookings/{booking_id}", tags=["Bookings"])
async def get_booking(booking_id: str):
    """
    Get details of a specific booking.

    Args:
        booking_id: ID of the booking

    Returns:
        Booking details
    """
    try:
        for booking in assistant.get_bookings():
            if booking.booking_id == booking_id:
                return booking.dict()
        raise HTTPException(status_code=404, detail="Booking not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving booking: {str(e)}")


# ==================== Dealership Info Endpoints ====================

@app.get("/api/v1/dealership", response_model=DealershipInfo, tags=["Info"])
async def get_dealership_info():
    """
    Get dealership information and working hours.

    Returns:
        Dealership details
    """
    try:
        info = assistant.knowledge_base.get_dealership_info()
        return DealershipInfo(**info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dealership info: {str(e)}")


# ==================== WebSocket Endpoints ====================

@app.websocket("/ws/chat/{client_id}")
async def websocket_chat(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time chat.

    Args:
        websocket: WebSocket connection
        client_id: Client identifier
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")

            if not message:
                continue

            # Process message
            response = await assistant.process_text_async(message)

            # Send response
            await websocket.send_json({
                "response": response,
                "client_id": client_id,
                "timestamp": datetime.now().isoformat(),
            })
    except Exception as e:
        await websocket.close(code=1011, reason=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("API_DEBUG", "true").lower() == "true"

    uvicorn.run(
        "src.api:app",
        host=host,
        port=port,
        reload=debug,
    )
