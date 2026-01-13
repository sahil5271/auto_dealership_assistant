# 🚗 Multi-Agent Voice Assistant for Auto Dealership Test Drive Booking

A sophisticated multi-agent voice assistant system that handles test drive bookings for an auto dealership using advanced LLM-based agents and multi-turn conversation management.

## 📋 Features

### ✨ Core Capabilities
- **Multi-Agent Architecture**: Conversation Agent, Knowledge Agent, and Booking Agent working collaboratively
- **Voice Interaction**: Full STT (Speech-to-Text) and TTS (Text-to-Speech) support
- **Natural Language Understanding**: Intent recognition and context-aware responses
- **Test Drive Booking**: Automated scheduling and confirmation
- **Knowledge Base Integration**: Dynamic car inventory management
- **REST API**: Complete API endpoints for integration with web/mobile clients
- **Real-time WebSocket**: Live conversation over WebSocket connections

### 🎯 Multi-Agent System
1. **Conversation Agent**: Manages dialogue flow, intent recognition, and user interaction
2. **Knowledge Agent**: Provides car details, specifications, and availability
3. **Booking Agent**: Handles test drive scheduling and confirmations

## 🛠️ Tech Stack

- **LLM Framework**: LangChain + OpenAI GPT-4
- **Voice APIs**: 
  - Azure Cognitive Services (Speech)
  - Google Cloud Speech-to-Text/Text-to-Speech
  - OpenAI Whisper + TTS
  - Local (pyttsx3 + SpeechRecognition)
- **Backend**: FastAPI + Uvicorn
- **Python**: 3.8+

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- (Optional) Azure Speech API keys
- (Optional) Google Cloud credentials
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/auto_dealership_assistant.git
cd auto_dealership_assistant
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
VOICE_PROVIDER=local  # or: openai, azure, google
```

## 🚀 Quick Start

### Text-Based Interaction
```bash
python -m src.orchestrator
```

**Example:**
```
[Assistant]: Hello! Welcome to Premium Auto Dealership...
[You]: I'm looking for an SUV
[Assistant]: Great! We have several SUVs available...
[You]: I'd like to book a test drive for tomorrow at 11 AM
[Assistant]: Perfect! I can help you book a test drive...
```

### Voice-Based Interaction (Requires Microphone)
```bash
python -m src.orchestrator --voice --voice-provider local
```

**Voice Providers:**
- `local`: Uses free Google Speech API (requires internet)
- `openai`: Uses OpenAI Whisper (requires OPENAI_API_KEY)
- `azure`: Uses Azure Speech Services (requires Azure keys)
- `google`: Uses Google Cloud Speech API (requires credentials file)

### Launch REST API Server
```bash
python -m src.api
```

Server will start at: `http://localhost:8000`

**Swagger Documentation**: `http://localhost:8000/docs`

## 📚 API Endpoints

### Chat
- **POST** `/api/v1/chat` - Send text message to assistant
- **GET** `/ws/chat/{client_id}` - WebSocket for real-time chat

### Cars
- **GET** `/api/v1/cars` - List available cars
- **GET** `/api/v1/cars/{car_id}` - Get car details
- **POST** `/api/v1/cars/search` - Search cars by criteria

### Bookings
- **POST** `/api/v1/bookings` - Create test drive booking
- **GET** `/api/v1/bookings` - List all bookings
- **GET** `/api/v1/bookings/{booking_id}` - Get booking details

### Voice
- **POST** `/api/v1/transcribe` - Transcribe audio to text
- **POST** `/api/v1/speak` - Convert text to speech

### Info
- **GET** `/api/v1/dealership` - Get dealership information
- **GET** `/health` - Health check

## 📖 Usage Examples

### Example 1: Text-Based Chat
```python
from src.orchestrator import DealershipAssistant

assistant = DealershipAssistant(use_voice=False)

# Chat with the assistant
response = assistant.process_text("I want to book a test drive for an SUV")
print(response)

# Get bookings
bookings = assistant.get_bookings()
for booking in bookings:
    print(f"Booking ID: {booking.booking_id}")
    print(f"Car: {booking.car_model}")
    print(f"Date: {booking.preferred_date}")
```

### Example 2: Voice Interaction
```python
import asyncio
from src.orchestrator import DealershipAssistant

async def main():
    assistant = DealershipAssistant(
        use_voice=True,
        voice_provider="local"
    )
    await assistant.run_voice_interaction()

asyncio.run(main())
```

### Example 3: REST API Client
```python
import requests

# Chat endpoint
response = requests.post(
    "http://localhost:8000/api/v1/chat",
    json={"message": "I want to book a test drive"}
)
print(response.json())

# Get available cars
cars = requests.get("http://localhost:8000/api/v1/cars").json()
print(cars)

# Create booking
booking = requests.post(
    "http://localhost:8000/api/v1/bookings",
    json={
        "customer_name": "John Doe",
        "customer_phone": "+1-555-0123",
        "car_id": "sedan_001",
        "preferred_date": "2024-01-20",
        "preferred_time": "14:00"
    }
).json()
print(booking)
```

### Example 4: WebSocket Chat
```javascript
// JavaScript client
const socket = new WebSocket('ws://localhost:8000/ws/chat/client123');

socket.onopen = function() {
    socket.send(JSON.stringify({
        message: "I want to book a test drive"
    }));
};

socket.onmessage = function(event) {
    const response = JSON.parse(event.data);
    console.log("Assistant:", response.response);
};
```

## 📊 Sample Workflow

### Customer Journey
```
1. Customer calls or visits website
   ↓
2. Greeting & Intent Recognition
   "I want to book a test drive for an SUV"
   ↓
3. Knowledge Agent queries inventory
   Lists available SUVs with features
   ↓
4. Customer selects vehicle
   "I like the Explorer Pro"
   ↓
5. Check availability & confirm details
   "Do you want 2024-01-20 at 11 AM?"
   ↓
6. Booking Agent finalizes booking
   Creates confirmation with booking ID
   ↓
7. Send confirmation (SMS/Email)
   "Your test drive is booked!"
```

## 🧪 Testing

Run the test suite:
```bash
python tests/test_assistant.py
```

Tests include:
- Knowledge Base functionality
- Conversation Agent responses
- Voice utilities
- Booking system
- End-to-end workflow

## 📁 Project Structure

```
auto_dealership_assistant/
├── src/
│   ├── __init__.py
│   ├── agents.py              # Multi-agent system
│   ├── voice_utils.py         # STT/TTS utilities
│   ├── orchestrator.py        # Main orchestrator
│   └── api.py                 # FastAPI backend
├── data/
│   └── car_inventory.json     # Car inventory knowledge base
├── tests/
│   └── test_assistant.py      # Test suite
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── README.md                 # This file
└── main.py                   # Entry point
```

## 🔄 Agent Architecture

### Data Flow
```
User Input (Text/Voice)
        ↓
    Conversation Agent
        ↓
   (Intent Recognition)
        ↓
   ├→ Knowledge Agent
   │      ↓
   │  (Query Database)
   │      ↓
   └→ Booking Agent
          ↓
      (Schedule Test Drive)
          ↓
    Generate Response
        ↓
   Output (Text/Voice)
```

## 🎙️ Voice Providers

### Local (Recommended for Testing)
- **STT**: Google Speech API (free, requires internet)
- **TTS**: pyttsx3 (offline)
- No API keys required

### OpenAI
- **STT**: Whisper (excellent accuracy)
- **TTS**: GPT-4 TTS
- Requires: `OPENAI_API_KEY`

### Azure
- **STT**: Azure Cognitive Services Speech-to-Text
- **TTS**: Azure Cognitive Services Text-to-Speech
- Requires: `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`

### Google Cloud
- **STT**: Google Cloud Speech-to-Text
- **TTS**: Google Cloud Text-to-Speech
- Requires: `GOOGLE_APPLICATION_CREDENTIALS` (path to credentials JSON)

## 🔧 Configuration

### Environment Variables
```env
# OpenAI
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4
TEMPERATURE=0.7

# Voice Settings
USE_VOICE=true
VOICE_PROVIDER=local

# Azure (optional)
AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=eastus

# Google Cloud (optional)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# API Server
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# Database
DATABASE_URL=sqlite:///./test_drives.db
```

## 📝 Knowledge Base Format

The knowledge base is stored in `data/car_inventory.json`:
```json
{
  "dealership": {
    "name": "Premium Auto Dealership",
    "location": "Downtown Motors",
    "contact": "+1-800-PREMIUM-1"
  },
  "inventory": [
    {
      "id": "sedan_001",
      "brand": "LuxuryAuto",
      "model": "Elegance 2024",
      "type": "Sedan",
      "price_range": "$35,000 - $42,000",
      "features": [...],
      "availability": true
    }
  ],
  "working_hours": {...}
}
```

## 🤖 Customization

### Add New Car Types
Edit `data/car_inventory.json` and add to the `inventory` array.

### Modify Agent Behavior
Edit prompts in `src/agents.py`:
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom system prompt here"),
    ...
])
```

### Add Custom Tools
Create new tools in `src/agents.py` using the `@tool` decorator:
```python
@tool
def custom_tool(param: str) -> str:
    """Tool description."""
    return "result"
```

## 🐛 Troubleshooting

### Issue: "OpenAI API key not provided"
**Solution**: Set `OPENAI_API_KEY` in `.env` file
```bash
echo "OPENAI_API_KEY=your_key_here" >> .env
```

### Issue: "Could not initialize voice components"
**Solution**: Check voice provider availability
```bash
# Use local provider for testing
python -m src.orchestrator --voice-provider local
```

### Issue: "Microphone not detected"
**Solution**: Verify microphone permissions and drivers
```bash
# Test microphone
python -c "import speech_recognition as sr; sr.Microphone()"
```

### Issue: API port already in use
**Solution**: Change port in `.env`
```bash
echo "API_PORT=8001" >> .env
```

## 📞 API Example: Full Test Drive Booking

```bash
# 1. Start API server
python -m src.api &

# 2. Get available cars
curl http://localhost:8000/api/v1/cars

# 3. Chat about your preference
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want an SUV with good fuel efficiency"}'

# 4. Book a test drive
curl -X POST http://localhost:8000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Doe",
    "customer_phone": "+1-555-0123",
    "car_id": "suv_001",
    "preferred_date": "2024-01-20",
    "preferred_time": "14:00"
  }'

# 5. Check your booking
curl http://localhost:8000/api/v1/bookings
```

## 📈 Performance Tips

1. **Caching**: Results are cached in memory during conversation
2. **Rate Limiting**: Implement rate limits for API endpoints
3. **Async Processing**: Use async endpoints for long operations
4. **Model Selection**: GPT-3.5-turbo is faster than GPT-4 (but less accurate)

## 🔐 Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Rate Limiting**: Implement rate limiting on public APIs
3. **Input Validation**: All inputs are validated
4. **CORS**: Configured to allow necessary origins only
5. **Error Handling**: Sensitive information is not exposed in errors

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include environment details and error logs

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced calendar integration (Google Calendar, Outlook)
- [ ] SMS/Email confirmation system
- [ ] Customer database integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app integration
- [ ] Vehicle comparison feature
- [ ] Financing options integration
- [ ] Extended test drive packages
- [ ] Customer feedback system

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure Speech Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/)

---

**Created with ❤️ for auto dealership innovation**
