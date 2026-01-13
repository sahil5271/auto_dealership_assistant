# Quick Start Guide

## 5-Minute Setup

### Step 1: Clone & Setup (2 minutes)
```bash
cd auto_dealership_assistant
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure (1 minute)
```bash
cp .env.example .env
# Edit .env: Replace OPENAI_API_KEY with your actual key
```

### Step 3: Run (2 minutes)

#### Text-Based Mode
```bash
python main.py
```

**Sample Conversation:**
```
[Assistant]: Hello! Welcome to Premium Auto Dealership...
[You]: I want an SUV
[Assistant]: We have several great SUVs available...
[You]: Tell me about the Explorer Pro
[Assistant]: The RuggAuto Explorer Pro is a fantastic choice...
[You]: I'd like to book a test drive for tomorrow at 11 AM
[Assistant]: Perfect! I can help with that...
```

#### Voice Mode (Requires Microphone)
```bash
python main.py --voice --voice-provider local
```

#### API Server
```bash
python main.py --api
# Visit: http://localhost:8000/docs
```

---

## Common Tasks

### Book a Test Drive via CLI
```bash
python main.py
```
Then say/type: "I want to book a test drive for a sedan tomorrow at 2 PM"

### Book via API
```bash
curl -X POST http://localhost:8000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Doe",
    "customer_phone": "+1-555-0123",
    "car_id": "sedan_001",
    "preferred_date": "2024-01-20",
    "preferred_time": "14:00"
  }'
```

### List Available Cars
```bash
curl http://localhost:8000/api/v1/cars
```

### Search for SUVs
```bash
curl "http://localhost:8000/api/v1/cars?car_type=SUV"
```

### Run Tests
```bash
python main.py --test
```

---

## Troubleshooting

### Error: "OpenAI API key not provided"
1. Copy `.env.example` to `.env`
2. Add your OpenAI API key
3. Save and restart

### Error: "Microphone not detected"
1. Check microphone is connected
2. Check permissions: `Settings → Privacy → Microphone`
3. Use text mode instead: `python main.py`

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
```bash
python main.py --api --port 8001
```

---

## Next Steps

1. **Customize**: Edit `data/car_inventory.json` to add your cars
2. **Deploy**: See `DEPLOYMENT.md` for cloud deployment
3. **Extend**: See `API_DOCUMENTATION.md` for API details
4. **Integrate**: Use REST API in your web/mobile app

---

## Help

- 📖 See `README.md` for full documentation
- 📡 See `API_DOCUMENTATION.md` for API details
- 🚀 See `DEPLOYMENT.md` for deployment options
- 🧪 Run `python main.py --test` to run test suite

---

## Example Conversations

### Conversation 1: Simple Booking
```
Assistant: Hello! Welcome to Premium Auto Dealership...
You: Hi, I want to book a test drive
Assistant: Great! What type of vehicle interests you?
You: I'm looking for an SUV
Assistant: We have several excellent SUVs...
You: When can I come in?
You: How about tomorrow at 10 AM?
Assistant: Perfect! Your test drive is booked!
```

### Conversation 2: Detailed Inquiry
```
Assistant: Hello! Welcome to Premium Auto Dealership...
You: Tell me about your electric vehicles
Assistant: We have the FutureRide EV, which is fantastic...
You: What's the range?
Assistant: It has a 350-mile range with fast charging...
You: How much does it cost?
Assistant: The price range is $42,000 to $58,000...
You: I'd like to test drive it this Saturday at 2 PM
Assistant: Your test drive for Saturday is confirmed!
```

---

## API Quick Reference

```bash
# Start API
python main.py --api

# Chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want an SUV"}'

# Book
curl -X POST http://localhost:8000/api/v1/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John",
    "customer_phone": "+1-555-0123",
    "car_id": "suv_001",
    "preferred_date": "2024-01-20",
    "preferred_time": "10:00"
  }'

# List cars
curl http://localhost:8000/api/v1/cars

# Get car details
curl http://localhost:8000/api/v1/cars/sedan_001

# Check booking
curl http://localhost:8000/api/v1/bookings
```

---

## Tips & Tricks

1. **Faster Response**: Use GPT-3.5-turbo instead of GPT-4
   ```bash
   python main.py --model gpt-3.5-turbo
   ```

2. **Better Voice Quality**: Use Azure or OpenAI voice provider
   ```bash
   python main.py --voice --voice-provider openai
   ```

3. **Custom Inventory**: Add cars to `data/car_inventory.json`

4. **API Swagger**: Visit `http://localhost:8000/docs` when running API

5. **WebSocket Chat**: Use `ws://localhost:8000/ws/chat/client123`

---

**You're all set! Enjoy using the Auto Dealership Assistant! 🚗**
