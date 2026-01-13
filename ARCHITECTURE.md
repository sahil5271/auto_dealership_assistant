# Implementation & Architecture Guide

## System Architecture

### High-Level Overview
```
┌─────────────────┐
│  User Interface │
├─────────────────┤
│  • CLI (Text)   │
│  • CLI (Voice)  │
│  • REST API     │
│  • WebSocket    │
└────────┬────────┘
         │
    ┌────▼─────────────────┐
    │  Orchestrator Layer   │
    │  DealershipAssistant  │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────────────────────┐
    │     Agent Layer (LangChain)            │
    ├────┬──────────────┬──────────────────┤
    │    │              │                  │
    │ Conversation  Knowledge          Booking
    │ Agent         Agent              Agent
    │    │              │                  │
    └────┼──────────────┼──────────────────┘
         │              │                  │
    ┌────▼──────────────▼──────────────────▼──┐
    │           Tools Layer                    │
    │  ├─ search_car_by_type()                 │
    │  ├─ get_car_details()                    │
    │  ├─ list_available_cars()                │
    │  ├─ check_availability()                 │
    │  ├─ get_dealership_info()                │
    │  └─ book_test_drive()                    │
    └────┬──────────────────────────────────┬──┘
         │                                  │
    ┌────▼──────────────┐  ┌──────────────▼────┐
    │  Knowledge Base   │  │  Voice I/O         │
    │  (car_inventory   │  │  ├─ STT (4)        │
    │   .json)          │  │  └─ TTS (4)        │
    └───────────────────┘  └───────────────────┘
```

## Agent Collaboration Flow

### Conversation Flow Diagram
```
Customer Input (Text/Voice)
    │
    ▼
┌─────────────────────────────────┐
│ Conversation Agent              │
│ - Greet customer                │
│ - Understand intent             │
│ - Manage dialogue flow          │
│ - Route to appropriate agent    │
└────┬────────────────────────────┘
     │
     ├─────────────────────────────────────┐
     │                                     │
     ▼                                     ▼
┌──────────────────────┐  ┌──────────────────────┐
│ Knowledge Agent      │  │ Booking Agent        │
│ - Query inventory    │  │ - Check availability │
│ - Provide details    │  │ - Create booking     │
│ - Make             │  │ - Confirm details    │
│   recommendations    │  │                      │
└──────────────┬───────┘  └──────────┬───────────┘
               │                     │
               │                     │
               └─────────┬───────────┘
                         │
                         ▼
                    Response Generation
                         │
                         ▼
              Output (Text or Voice)
```

## Message Flow

### Example: Test Drive Booking
```
Customer: "I want to book a test drive for an SUV tomorrow at 11 AM"
    │
    ▼
Conversation Agent (LLM processes message)
    │
    ├─ Intent: book_test_drive
    ├─ Car Type: SUV
    ├─ Date: tomorrow
    └─ Time: 11 AM
    │
    ▼
Calls: search_car_by_type("SUV")
    │
    ▼
Knowledge Agent (Tool Execution)
    │
    └─ Returns: [Explorer Pro, ...other SUVs]
    │
    ▼
Conversation Agent (Generate Response)
    │
    └─ "We have several SUVs. Let me show you..."
    │
    ▼
Output to Customer
    │
    ▼
Customer: "Tell me about the Explorer Pro"
    │
    ▼
Calls: get_car_details("suv_001")
    │
    ▼
Returns detailed specifications
    │
    ▼
Customer: "Perfect, book it for tomorrow at 11 AM"
    │
    ▼
Calls: book_test_drive(...)
    │
    ├─ Validates date/time
    ├─ Creates booking record
    └─ Returns confirmation
    │
    ▼
"Your test drive is confirmed! Booking ID: TD-..."
```

## Code Flow: Agent Interaction

### Step 1: Initialize System
```python
# src/orchestrator.py
assistant = DealershipAssistant(use_voice=False)

# This initializes:
# 1. KnowledgeBase (loads car_inventory.json)
# 2. DealershipTools (creates 6 tools)
# 3. ConversationAgent (with LLM + tools)
# 4. KnowledgeAgent (for queries)
# 5. BookingAgent (for scheduling)
# 6. Optional: SpeechToText and TextToSpeech
```

### Step 2: Process User Input
```python
# src/orchestrator.py - process_text()
response = assistant.process_text("I want an SUV")

# Internally:
# 1. ConversationAgent receives message
# 2. LLM (GPT-4) processes with system prompt
# 3. Determines tools needed: search_car_by_type()
# 4. Tool execution via DealershipTools
# 5. LLM formats response
# 6. Returns response string
```

### Step 3: Tool Execution
```python
# src/agents.py - DealershipTools
def search_car_by_type(car_type: str) -> str:
    # 1. Query knowledge base
    results = self.kb.search_cars_by_type(car_type)
    
    # 2. Format response
    response = f"Found {len(results)} car(s)..."
    
    # 3. Return to agent
    return response
```

### Step 4: Voice Output (if enabled)
```python
# src/voice_utils.py
tts = get_tts_provider(provider="local")
tts.speak(response)

# Internally:
# 1. Convert text to speech
# 2. Play audio to speaker
```

## Key Design Patterns

### 1. Factory Pattern (Voice Providers)
```python
def get_tts_provider(provider="local"):
    if provider == "openai":
        return OpenAITTS(api_key)
    elif provider == "azure":
        return AzureTTS(api_key, region)
    elif provider == "google":
        return GoogleSTT(credentials_path)
    else:
        return LocalTTS()
```

### 2. Abstract Base Classes (Voice I/O)
```python
class TextToSpeech(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        pass

# Implementations:
class OpenAITTS(TextToSpeech): ...
class AzureTTS(TextToSpeech): ...
class LocalTTS(TextToSpeech): ...
```

### 3. Tool Decorator (LangChain)
```python
@tool
def search_car_by_type(car_type: str) -> str:
    """Search for cars by type."""
    results = self.kb.search_cars_by_type(car_type)
    return formatted_response
```

### 4. Singleton Pattern (KnowledgeBase)
```python
# Single instance shared by all agents
kb = KnowledgeBase("data/car_inventory.json")
tools = DealershipTools(kb)
agent = ConversationAgent(tools)
```

## Extension Points

### Add New Agent
```python
class CustomAgent:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.llm = ChatOpenAI(model="gpt-4")
    
    def process(self, input_data):
        # Custom logic
        return result

# Register in DealershipAssistant
self.custom_agent = CustomAgent(self.knowledge_base)
```

### Add New Tool
```python
@tool
def custom_tool(parameter: str) -> str:
    """Tool description for LLM."""
    # Implementation
    return result

# Add to DealershipTools.get_tools()
tools.append(
    LangchainTool(
        name="custom_tool",
        description="...",
        func=self.custom_tool
    )
)
```

### Add New Voice Provider
```python
class NewVoiceTTS(TextToSpeech):
    def speak(self, text: str) -> None:
        # Implementation using new API
        pass
    
    async def speak_async(self, text: str) -> None:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.speak, text)

# Add to factory
if provider == "new_provider":
    return NewVoiceTTS(api_key)
```

## Data Models

### TestDriveBooking
```python
class TestDriveBooking(BaseModel):
    booking_id: str              # Unique ID (TD-timestamp)
    customer_name: str           # Customer name
    customer_phone: str          # Contact number
    customer_email: Optional[str] # Email
    car_model: str               # e.g., "LuxuryAuto Elegance 2024"
    car_id: str                  # e.g., "sedan_001"
    preferred_date: str          # YYYY-MM-DD
    preferred_time: str          # HH:MM
    test_drive_duration: int     # Minutes
    booking_status: str          # "confirmed", "cancelled", etc.
    booking_timestamp: str       # ISO timestamp
```

## API Response Format

### Standardized Response Structure
```python
# Success Response
{
    "response": "Assistant response text",
    "session_id": "session_123",
    "timestamp": "2024-01-13T10:30:00",
    "status": "success"
}

# Error Response
{
    "detail": "Error message",
    "status_code": 400
}

# List Response
{
    "data": [...],
    "count": 5,
    "timestamp": "2024-01-13T10:30:00"
}
```

## State Management

### Conversation Memory (LangChain)
```python
# ConversationAgent uses ConversationBufferMemory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Stores:
# - User messages
# - Agent responses
# - Tool calls and results
# - Context for next turn
```

### Booking Storage
```python
# KnowledgeBase maintains booking list
class KnowledgeBase:
    def __init__(self):
        self.bookings: List[TestDriveBooking] = []
    
    def book_test_drive(self, booking: TestDriveBooking) -> bool:
        self.bookings.append(booking)
        return True
```

## Error Handling

### Try-Catch Pattern
```python
try:
    response = assistant.process_text(user_input)
except HTTPException:
    raise  # Already formatted
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
```

## Performance Considerations

### Optimization Strategies
1. **Caching**: Use conversation memory to avoid repeated queries
2. **Async**: Use async/await for I/O operations
3. **Streaming**: Stream TTS output for faster response
4. **Model Selection**: Use GPT-3.5-turbo for faster responses (less accurate)

### Scaling
1. **Horizontal**: Run multiple API instances
2. **Vertical**: Increase server resources
3. **Database**: Use PostgreSQL with read replicas
4. **Caching**: Add Redis for session/response caching

## Testing Strategy

### Unit Tests
- Test individual tools
- Test voice providers
- Test data models

### Integration Tests
- Test agent interactions
- Test API endpoints
- Test full booking flow

### End-to-End Tests
- Complete conversation flow
- Voice to booking pipeline
- API to database

## Deployment Architecture

### Single Server
```
User → Load Balancer → API Server + Agent
                         ├─ LLM API
                         ├─ Voice API
                         └─ Database
```

### Distributed
```
Users → Load Balancer → API Servers (n)
            │                 ├─ Agent 1
            │                 ├─ Agent 2
            │                 └─ Agent n
            │
            ├─ LLM API Service
            ├─ Voice API Service
            ├─ Database (Primary + Replicas)
            ├─ Cache (Redis)
            └─ Message Queue (RabbitMQ)
```

## Security Implementation

### API Security
```python
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key
```

### Input Validation
```python
from pydantic import BaseModel, Field, validator

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    
    @validator('message')
    def validate_message(cls, v):
        # Check for injection attacks, profanity, etc.
        return v
```

---

**This guide provides a complete understanding of the system architecture and implementation details for extending and maintaining the Auto Dealership Assistant.**
