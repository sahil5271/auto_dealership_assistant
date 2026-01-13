# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API is open. In production, implement:
- API Keys
- OAuth 2.0
- JWT tokens

## Response Format
All responses are JSON:
```json
{
  "status": "success",
  "data": {},
  "timestamp": "2024-01-13T10:30:00"
}
```

## Error Handling
```json
{
  "detail": "Error message here"
}
```

## Endpoints

### Health & Status

#### GET /
Check API status.

**Response:**
```json
{
  "status": "online",
  "service": "Auto Dealership Voice Assistant",
  "version": "1.0.0"
}
```

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-13T10:30:00"
}
```

---

### Chat

#### POST /api/v1/chat
Send a text message to the assistant.

**Request:**
```json
{
  "message": "I want to book a test drive for an SUV",
  "session_id": "session_123"
}
```

**Response:**
```json
{
  "response": "Great! We have several SUVs available...",
  "session_id": "session_123",
  "timestamp": "2024-01-13T10:30:00"
}
```

**Status Codes:**
- 200: Success
- 500: Server error

---

### Voice

#### POST /api/v1/transcribe
Transcribe audio file to text.

**Request:**
- Content-Type: multipart/form-data
- File: audio file (WAV, MP3)

**Response:**
```json
{
  "text": "I want to book a test drive",
  "confidence": 0.95
}
```

#### POST /api/v1/speak
Convert text to speech.

**Request:**
```json
{
  "text": "Your test drive is confirmed",
  "voice": "nova"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Audio generated"
}
```

---

### Cars

#### GET /api/v1/cars
List available cars, optionally filtered by type.

**Query Parameters:**
- `car_type` (optional): Type of car (sedan, SUV, truck, compact, electric)

**Response:**
```json
[
  {
    "id": "sedan_001",
    "brand": "LuxuryAuto",
    "model": "Elegance 2024",
    "year": 2024,
    "type": "Sedan",
    "price_range": "$35,000 - $42,000",
    "features": ["Advanced safety", "Touchscreen"],
    "fuel_type": "Hybrid",
    "availability": true
  }
]
```

#### GET /api/v1/cars/{car_id}
Get detailed information about a specific car.

**Path Parameters:**
- `car_id`: Car ID (e.g., "sedan_001")

**Response:**
```json
{
  "id": "sedan_001",
  "type": "Sedan",
  "model": "Elegance 2024",
  "brand": "LuxuryAuto",
  "year": 2024,
  "color": ["Black", "Silver", "Blue"],
  "price_range": "$35,000 - $42,000",
  "features": [
    "Advanced safety features",
    "Touchscreen infotainment",
    "Lane keeping assist"
  ],
  "fuel_type": "Hybrid",
  "mpg": "45 city / 52 highway",
  "seating_capacity": 5,
  "transmission": "Automatic CVT",
  "engine": "2.5L 4-cylinder hybrid",
  "availability": true,
  "test_drive_duration_minutes": 60
}
```

#### POST /api/v1/cars/search
Search for cars based on criteria.

**Request:**
```json
{
  "car_type": "SUV",
  "brand": "RuggAuto",
  "budget_min": 40000,
  "budget_max": 60000
}
```

**Response:**
```json
[
  {
    "id": "suv_001",
    "brand": "RuggAuto",
    "model": "Explorer Pro",
    "type": "SUV",
    "price_range": "$45,000 - $55,000",
    "features": ["All-wheel drive", "Panoramic roof"],
    "fuel_type": "Gasoline",
    "availability": true
  }
]
```

---

### Bookings

#### POST /api/v1/bookings
Create a new test drive booking.

**Request:**
```json
{
  "customer_name": "John Doe",
  "customer_phone": "+1-555-0123",
  "customer_email": "john@example.com",
  "car_id": "sedan_001",
  "preferred_date": "2024-01-20",
  "preferred_time": "14:00"
}
```

**Response:**
```json
{
  "booking_id": "TD-1705154400",
  "customer_name": "John Doe",
  "car_model": "LuxuryAuto Elegance 2024",
  "preferred_date": "2024-01-20",
  "preferred_time": "14:00",
  "booking_status": "confirmed",
  "message": "Test drive booked successfully! Confirmation will be sent to +1-555-0123"
}
```

**Status Codes:**
- 200: Success
- 400: Invalid data or time not available
- 404: Car not found
- 500: Server error

#### GET /api/v1/bookings
List all bookings made during this session.

**Response:**
```json
{
  "bookings": [
    {
      "booking_id": "TD-1705154400",
      "customer_name": "John Doe",
      "customer_phone": "+1-555-0123",
      "car_model": "LuxuryAuto Elegance 2024",
      "preferred_date": "2024-01-20",
      "preferred_time": "14:00",
      "test_drive_duration": 60,
      "booking_status": "confirmed",
      "booking_timestamp": "2024-01-13T10:30:00"
    }
  ],
  "count": 1
}
```

#### GET /api/v1/bookings/{booking_id}
Get details of a specific booking.

**Path Parameters:**
- `booking_id`: Booking ID (e.g., "TD-1705154400")

**Response:**
```json
{
  "booking_id": "TD-1705154400",
  "customer_name": "John Doe",
  "customer_phone": "+1-555-0123",
  "car_model": "LuxuryAuto Elegance 2024",
  "preferred_date": "2024-01-20",
  "preferred_time": "14:00",
  "test_drive_duration": 60,
  "booking_status": "confirmed",
  "booking_timestamp": "2024-01-13T10:30:00"
}
```

---

### Dealership Info

#### GET /api/v1/dealership
Get dealership information and working hours.

**Response:**
```json
{
  "name": "Premium Auto Dealership",
  "location": "Downtown Motors",
  "contact": "+1-800-PREMIUM-1",
  "email": "bookings@premiumauto.com",
  "working_hours": {
    "monday": "09:00 - 18:00",
    "tuesday": "09:00 - 18:00",
    "wednesday": "09:00 - 18:00",
    "thursday": "09:00 - 18:00",
    "friday": "09:00 - 18:00",
    "saturday": "10:00 - 17:00",
    "sunday": "Closed"
  }
}
```

---

### WebSocket

#### WS /ws/chat/{client_id}
Real-time chat via WebSocket.

**Connect:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/client123');
```

**Send Message:**
```javascript
ws.send(JSON.stringify({
  message: "I want to book a test drive"
}));
```

**Receive Response:**
```javascript
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.response);
  console.log(data.timestamp);
};
```

---

## Rate Limiting

Current limits (can be customized):
- Chat: 100 requests per minute per IP
- Bookings: 10 per minute per IP
- Transcribe: 20 per minute per IP

Response header:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1705154400
```

---

## Pagination

For list endpoints:
```
GET /api/v1/cars?page=1&limit=10
```

Response:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "pages": 10
  }
}
```

---

## Common Use Cases

### 1. Full Booking Flow
```bash
# 1. Get available cars
curl http://localhost:8000/api/v1/cars?car_type=SUV

# 2. Get car details
curl http://localhost:8000/api/v1/cars/suv_001

# 3. Create booking
curl -X POST http://localhost:8000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_phone": "+1-555-0123",
    "car_id": "suv_001",
    "preferred_date": "2024-01-20",
    "preferred_time": "14:00"
  }'

# 4. Verify booking
curl http://localhost:8000/api/v1/bookings
```

### 2. Voice Interaction
```bash
# 1. Transcribe audio
curl -X POST -F "file=@audio.wav" \
  http://localhost:8000/api/v1/transcribe

# 2. Chat with response
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to book a test drive"}'

# 3. Speak response
curl -X POST http://localhost:8000/api/v1/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "Your booking is confirmed!"}'
```

---

## Changelog

### Version 1.0.0
- Initial release
- Multi-agent conversation system
- Test drive booking
- Voice I/O support
- REST API endpoints
- WebSocket support
