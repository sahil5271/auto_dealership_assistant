# 🎤 Multi-Agent Voice Assistant for Auto Dealership Test Drive Booking

A production-ready Python voice assistant for auto dealerships. Customers can book test drives through natural conversation using voice or text. Powered by LangChain, OpenAI, and multiple speech providers.

## ✨ Features

- **Multi-Agent System**: Conversation, Knowledge, and Booking agents working together
- **Voice & Text**: STT (Speech-to-Text) and TTS (Text-to-Speech) support
- **Natural Conversations**: Intent recognition and multi-turn dialogue
- **Test Drive Booking**: Automated scheduling with availability checking
- **Knowledge Base**: Car inventory with sample vehicles
- **REST API**: 15+ endpoints for web/mobile integration
- **WebSocket Support**: Real-time bidirectional communication
- **Multiple Voice Providers**: OpenAI, Azure, Google Cloud, or local
- **Docker Ready**: Containerized deployment included

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8+
- OpenAI API key (get one at https://platform.openai.com/api-keys)

### Setup
```bash
# Clone and setup
git clone https://github.com/sahil5271/auto_dealership_assistant.git
cd auto_dealership_assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Run (Choose One)
```bash
# Text mode (easiest)
python main.py

# Voice mode
python main.py --voice --voice-provider local

# REST API server
python main.py --api
# Visit http://localhost:8000/docs

# Run tests
python main.py --test
```

## 📖 Usage Examples

### Text Conversation
```
$ python main.py

🎉 Welcome to Auto Dealership Voice Assistant!
You: I'm looking for an SUV
Assistant: Great! We have several SUVs available...
You: I'd like to book a test drive for tomorrow
Assistant: Perfect! I can help you with that...
```

### Voice Conversation
```bash
python main.py --voice --voice-provider local
# Speak: "I want to test drive the Elegance sedan"
# Assistant speaks back with options
```

### API Request
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "Show me SUVs"}'
```

## 🏗️ Project Structure

```
├── src/
│   ├── agents.py          # Multi-agent system
│   ├── voice_utils.py     # STT/TTS providers
│   ├── orchestrator.py    # Main coordinator
│   ├── api.py             # FastAPI backend
│   └── __init__.py
├── data/
│   └── car_inventory.json # Knowledge base
├── tests/
│   └── test_assistant.py  # Test suite
├── main.py                # CLI entry point
├── requirements.txt       # Dependencies
├── .env.example           # Config template
├── Dockerfile             # Docker image
├── docker-compose.yml     # Multi-service setup
└── README.md              # This file
```

## 🔧 Configuration

Edit `.env` to configure:

```env
# LLM Configuration
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4              # or gpt-3.5-turbo
TEMPERATURE=0.7

# Voice Configuration
VOICE_PROVIDER=local          # openai, azure, google, local
USE_VOICE=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# Optional: Cloud Providers
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=us-east-1
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

## 📡 REST API

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/chat` | Send message to assistant |
| GET | `/api/v1/cars` | List all available cars |
| GET | `/api/v1/cars/{car_id}` | Get car details |
| POST | `/api/v1/cars/search` | Search cars by type |
| POST | `/api/v1/bookings` | Create test drive booking |
| GET | `/api/v1/bookings` | List all bookings |
| GET | `/api/v1/bookings/{booking_id}` | Get booking details |
| POST | `/api/v1/transcribe` | Convert audio to text |
| POST | `/api/v1/speak` | Convert text to speech |
| WS | `/ws/chat/{client_id}` | WebSocket chat |

### Example: Book a Test Drive
```bash
curl -X POST http://localhost:8000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_phone": "555-1234",
    "customer_email": "john@example.com",
    "car_id": "sedan_001",
    "preferred_date": "2024-01-20",
    "preferred_time": "14:00"
  }'
```

### View API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤖 How It Works

### Agent Architecture
```
User Input (Voice/Text)
    ↓
Conversation Agent
    ├→ Intent Recognition
    ├→ Knowledge Agent (car queries)
    └→ Booking Agent (scheduling)
    ↓
Response Generation
    ↓
Output (Voice/Text/API)
```

## 🎤 Voice Providers

### STT (Speech-to-Text)
- **OpenAI Whisper**: High accuracy, multilingual
- **Azure Speech**: Enterprise-grade
- **Google Cloud**: Cloud-based
- **Local**: SpeechRecognition library (no keys needed)

### TTS (Text-to-Speech)
- **OpenAI**: Natural voices
- **Azure Speech**: Multiple voices
- **Google Cloud**: High quality
- **Local**: pyttsx3 (no internet required)

Change provider:
```bash
python main.py --voice --voice-provider openai
python main.py --voice --voice-provider google
```

## 🐳 Docker Deployment

### Build & Run
```bash
# Build image
docker build -t auto-assistant .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  auto-assistant

# Or use docker-compose
docker-compose up
```

## 🧪 Testing

```bash
python main.py --test
```

Tests include:
- Knowledge base functionality
- Voice utilities
- Conversation agent responses
- Booking system operations
- End-to-end workflow

## 📊 Knowledge Base

Default inventory in `data/car_inventory.json`:
- **LuxuryAuto Elegance** - Sedan, $35k-$42k
- **RuggAuto Explorer Pro** - SUV, $45k-$55k
- **TruckMaster PowerHaul** - Truck, $38k-$52k
- **EcoAuto City Spark** - Compact, $18k-$24k
- **ElectroAuto FutureRide** - EV, $42k-$58k

Edit `car_inventory.json` to customize for your dealership.

## 🔌 Integration

### Python
```python
from src.orchestrator import DealershipAssistant

assistant = DealershipAssistant()
response = assistant.process_text("Show me SUVs under $50k")
print(response)
```

### JavaScript/Web
```javascript
const response = await fetch('http://localhost:8000/api/v1/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({user_id: 'user123', message: 'Book a test drive'})
});
const data = await response.json();
console.log(data.response);
```

## ⚙️ Advanced Usage

### Change LLM Model
```bash
python main.py --model gpt-3.5-turbo
```

### Custom Temperature
Edit `.env`:
```env
TEMPERATURE=0.3  # More deterministic
TEMPERATURE=0.9  # More creative
```

### Add More Vehicles
Edit `data/car_inventory.json` and add to the `inventory` array.

### Add Custom Tools
Edit `src/agents.py` and add functions with `@tool` decorator.

## 🛠️ Troubleshooting

### OpenAI API Key Error
- Check `.env` has `OPENAI_API_KEY`
- Verify key is valid at https://platform.openai.com/api-keys
- Check account has credits

### Microphone Not Working
- Test with `python -m speech_recognition`
- Use `--voice-provider local` if issues persist

### Port 8000 Already in Use
```bash
python main.py --api --port 9000
```

### Module Import Errors
```bash
pip install -r requirements.txt --upgrade
```

## 📈 Performance Tips

- Use GPT-3.5-turbo for faster responses
- Cache inventory in memory (already done)
- Use local voice provider to avoid API latency
- Deploy to same region as users

## 🌐 Scaling

- **Single Server**: Up to ~1000 concurrent users
- **Horizontal**: Use load balancer + multiple instances
- **Database**: Replace in-memory bookings with PostgreSQL
- **Queue**: Use Celery for async operations
- **Monitoring**: Integrate Prometheus + Grafana

## 📚 Learning Path

1. Run `python main.py` (text mode)
2. Try different queries
3. Edit `car_inventory.json` to customize
4. Run `python main.py --api` and explore `/docs`
5. Try `python main.py --voice`
6. Read source code in `src/`

## 💡 Use Cases

- Dealership websites (chat widget)
- Mobile apps (REST API)
- Call centers (voice service)
- Kiosks (standalone terminals)
- Chatbots (Discord, Telegram, WhatsApp)

## 📄 License

MIT License - Feel free to use and modify

## 🙋 Support

- **Issues**: Create GitHub issue
- **API Docs**: Visit `http://localhost:8000/docs`
- **Examples**: See usage examples above

## 🎯 What's Next

- [ ] Multi-language support
- [ ] Email/SMS confirmations
- [ ] Analytics dashboard
- [ ] Admin panel
- [ ] Mobile app
- [ ] Payment integration

---

**Built with ❤️ using Python, LangChain, and OpenAI**

**Repository**: https://github.com/sahil5271/auto_dealership_assistant
