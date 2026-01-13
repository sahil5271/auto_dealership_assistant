# Installation and Usage Guide

## 🎯 Complete Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- OpenAI API key (free trial available at https://platform.openai.com)
- (Optional) Microphone for voice interaction
- (Optional) Docker for containerized deployment

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
# Using HTTPS
git clone https://github.com/yourusername/auto_dealership_assistant.git
cd auto_dealership_assistant

# Or using SSH
git clone git@github.com:yourusername/auto_dealership_assistant.git
cd auto_dealership_assistant
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
# Upgrade pip first (recommended)
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

#### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# On Linux/macOS:
nano .env
# or
vi .env

# On Windows:
notepad .env
```

Edit the `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
VOICE_PROVIDER=local
```

### Step 5: Verify Installation

```bash
# Test Python and imports
python -c "from src.orchestrator import DealershipAssistant; print('✓ Installation successful!')"
```

## 🚀 Running the Application

### Option 1: Text-Based Conversation (Easiest)
```bash
# Start the assistant in text mode
python main.py

# You should see:
# =====================================================
#    🚗 AUTO DEALERSHIP VOICE ASSISTANT 🎤
# =====================================================
# [Assistant]: Hello! Welcome to Premium Auto Dealership...
# [You]: (type your message here)
```

**Example Conversation:**
```
[Assistant]: Hello! Welcome to Premium Auto Dealership...
[You]: I'm looking for a sedan
[Assistant]: Great! We have the Elegance 2024, which is an excellent sedan...
[You]: What features does it have?
[Assistant]: The Elegance 2024 includes advanced safety features...
[You]: I want to book a test drive for tomorrow at 2 PM
[Assistant]: Perfect! I'll help you book a test drive...
[You]: My name is John Doe and my phone is 555-0123
[Assistant]: ✓ Test drive booked successfully! Booking ID: TD-1705154400...
[You]: quit
[Assistant]: Thank you for visiting Premium Auto Dealership!
```

### Option 2: Voice Interaction (Requires Microphone)
```bash
# Start with voice support
python main.py --voice --voice-provider local

# The assistant will speak to you and listen for your voice responses
```

**Voice Providers:**
- `local` (Default, uses free Google API - requires internet)
- `openai` (Uses OpenAI Whisper - requires OPENAI_API_KEY)
- `azure` (Uses Azure Speech Services - requires Azure credentials)
- `google` (Uses Google Cloud - requires service account)

### Option 3: REST API Server
```bash
# Start the API server
python main.py --api

# Output:
# ============================================================
# Starting Auto Dealership Assistant API Server
# ============================================================
# 📡 API Server running at http://localhost:8000
# 📖 Swagger Docs at http://localhost:8000/docs
# 🎯 ReDoc at http://localhost:8000/redoc
```

Then open in your browser:
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Option 4: Run Tests
```bash
# Run all tests
python main.py --test

# Output:
# ╔════════════════════════════════════════════════════════╗
# ║     AUTO DEALERSHIP ASSISTANT - TEST SUITE            ║
# ╚════════════════════════════════════════════════════════╝
# 
# ============================================================
# TEST: Knowledge Base
# ============================================================
# ...
```

## 📡 Using the REST API

### Start the API Server
```bash
python main.py --api
```

### Making API Requests

#### 1. Chat with the Assistant
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want to book a test drive for an SUV"
  }'
```

**Response:**
```json
{
  "response": "Great! We have several excellent SUVs available...",
  "timestamp": "2024-01-13T10:30:00"
}
```

#### 2. List Available Cars
```bash
curl http://localhost:8000/api/v1/cars
```

**Response:**
```json
[
  {
    "id": "sedan_001",
    "brand": "LuxuryAuto",
    "model": "Elegance 2024",
    "type": "Sedan",
    "price_range": "$35,000 - $42,000",
    "features": ["Advanced safety", "Touchscreen"],
    "fuel_type": "Hybrid",
    "availability": true
  },
  ...
]
```

#### 3. Get Car Details
```bash
curl http://localhost:8000/api/v1/cars/sedan_001
```

#### 4. Search for Cars
```bash
curl -X POST http://localhost:8000/api/v1/cars/search \
  -H "Content-Type: application/json" \
  -d '{
    "car_type": "SUV",
    "budget_min": 40000,
    "budget_max": 60000
  }'
```

#### 5. Book a Test Drive
```bash
curl -X POST http://localhost:8000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Doe",
    "customer_phone": "+1-555-0123",
    "customer_email": "jane@example.com",
    "car_id": "suv_001",
    "preferred_date": "2024-01-20",
    "preferred_time": "14:00"
  }'
```

**Response:**
```json
{
  "booking_id": "TD-1705154400",
  "customer_name": "Jane Doe",
  "car_model": "RuggAuto Explorer Pro",
  "preferred_date": "2024-01-20",
  "preferred_time": "14:00",
  "booking_status": "confirmed",
  "message": "Test drive booked successfully!"
}
```

#### 6. Check Your Booking
```bash
# List all bookings
curl http://localhost:8000/api/v1/bookings

# Get specific booking
curl http://localhost:8000/api/v1/bookings/TD-1705154400
```

#### 7. Get Dealership Info
```bash
curl http://localhost:8000/api/v1/dealership
```

## 🌐 Using the Web Interface

### Access Swagger UI
1. Start API server: `python main.py --api`
2. Open browser: http://localhost:8000/docs
3. Click "Try it out" on any endpoint
4. Fill in parameters
5. Click "Execute"

### Access ReDoc
1. Open browser: http://localhost:8000/redoc
2. Browse through all available endpoints

## 🔧 Command Line Options

### Basic Syntax
```bash
python main.py [OPTIONS]
```

### Options
```
--help                 Show help message
--voice               Enable voice interaction
--voice-provider      Choose voice provider (openai, azure, google, local)
--api                 Start REST API server
--test                Run test suite
--inventory PATH      Path to car inventory JSON
--model MODEL         LLM model (gpt-4, gpt-3.5-turbo)
--port PORT           API server port (default: 8000)
```

### Examples
```bash
# Text mode (default)
python main.py

# Voice mode
python main.py --voice

# Voice with OpenAI provider
python main.py --voice --voice-provider openai

# API server on custom port
python main.py --api --port 8001

# Use GPT-3.5-turbo for faster responses
python main.py --model gpt-3.5-turbo

# Custom inventory file
python main.py --inventory /path/to/custom_inventory.json

# Run tests
python main.py --test
```

## 🐳 Using Docker

### Build Docker Image
```bash
# Build the image
docker build -t auto-dealership-assistant:latest .

# Verify build
docker images | grep auto-dealership
```

### Run with Docker
```bash
# Run in text mode
docker run -e OPENAI_API_KEY=your_key \
  auto-dealership-assistant:latest

# Run API server
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  auto-dealership-assistant:latest python main.py --api

# Run with volume mount
docker run -v $(pwd)/data:/app/data \
  -e OPENAI_API_KEY=your_key \
  auto-dealership-assistant:latest
```

### Use Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

## 🔐 Environment Configuration

### Required Variables
```env
# OpenAI API Key (required)
OPENAI_API_KEY=sk-your-key-here
```

### Optional Variables
```env
# Model Configuration
MODEL_NAME=gpt-4                    # or gpt-3.5-turbo
TEMPERATURE=0.7                     # 0-1, higher = more creative

# Voice Settings
USE_VOICE=true
VOICE_PROVIDER=local               # openai, azure, google, or local

# Azure Settings (if using Azure)
AZURE_SPEECH_KEY=your-azure-key
AZURE_SPEECH_REGION=eastus

# Google Cloud (if using Google)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# API Server Settings
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# Database
DATABASE_URL=sqlite:///./test_drives.db
```

## 📚 Documentation Guide

| Document | Purpose |
|----------|---------|
| **README.md** | Complete feature overview and reference |
| **QUICKSTART.md** | 5-minute quick start guide |
| **DEPLOYMENT.md** | Cloud and production deployment |
| **API_DOCUMENTATION.md** | Complete API reference with examples |
| **ARCHITECTURE.md** | System architecture and design patterns |
| **PROJECT_SUMMARY.md** | Project overview and deliverables |
| **This Guide** | Installation and usage instructions |

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
**Solution:**
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not provided"
**Solution:**
1. Create/edit `.env` file
2. Add: `OPENAI_API_KEY=sk-your-actual-key`
3. Save and restart

### "Microphone not detected"
**Solution:**
```bash
# Check if microphone works
python -m speech_recognition

# Use text mode instead
python main.py  # (without --voice flag)
```

### "Port 8000 already in use"
**Solution:**
```bash
# Use different port
python main.py --api --port 8001

# Or kill process using port 8000
lsof -i :8000  # Find process
kill -9 <PID>  # Kill process
```

### "Rate limit exceeded"
**Solution:**
- Wait a few minutes before making more requests
- Use GPT-3.5-turbo instead of GPT-4 (cheaper/faster)
- Implement local caching for repeated queries

### "Connection timeout"
**Solution:**
- Check internet connection
- Verify API key is correct
- Check OpenAI API status at https://status.openai.com

## 📊 Performance Tips

1. **Faster Responses**
   ```bash
   python main.py --model gpt-3.5-turbo
   ```

2. **Offline Voice**
   ```bash
   python main.py --voice --voice-provider local
   ```

3. **Production Deployment**
   - Use `--api` mode for API server
   - Use load balancer for multiple instances
   - Implement Redis caching for responses

## 🎯 Common Workflows

### Workflow 1: Quick Test Drive Booking
```bash
# 1. Start in text mode
python main.py

# 2. Say/Type:
I want to book a test drive for a sedan tomorrow at 11 AM

# 3. Follow prompts to complete booking
```

### Workflow 2: Using REST API
```bash
# 1. Start API server
python main.py --api

# 2. In another terminal, list cars
curl http://localhost:8000/api/v1/cars

# 3. Book a test drive
curl -X POST http://localhost:8000/api/v1/bookings ...

# 4. Check bookings
curl http://localhost:8000/api/v1/bookings
```

### Workflow 3: Running Tests
```bash
# Run all tests
python main.py --test

# Run specific test
python tests/test_assistant.py
```

## 🚀 Next Steps

1. **Customize Inventory**: Edit `data/car_inventory.json` with your vehicle fleet
2. **Configure Voice**: Set up voice provider in `.env`
3. **Deploy**: Follow `DEPLOYMENT.md` for production setup
4. **Integrate**: Use REST API in your applications
5. **Monitor**: Set up logging and monitoring in production

## 📞 Support

- **Installation Issues**: Check prerequisites and dependencies
- **API Issues**: See `API_DOCUMENTATION.md`
- **Voice Issues**: Check microphone and voice provider configuration
- **Feature Questions**: See `README.md` and `ARCHITECTURE.md`

---

**You're ready to go! Start with `python main.py` and enjoy! 🚗**
