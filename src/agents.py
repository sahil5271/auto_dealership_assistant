"""
Multi-agent system for auto dealership test drive booking.
Implements Conversation Agent, Knowledge Agent, and Booking Agent.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from pathlib import Path
from pydantic import BaseModel, Field
from langchain.tools import tool, Tool
from langchain.agents import Tool as LangchainTool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_openai_functions_agent


# ==================== Data Models ====================

class TestDriveBooking(BaseModel):
    """Data model for test drive bookings."""
    booking_id: str
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = None
    car_model: str
    car_id: str
    preferred_date: str
    preferred_time: str
    test_drive_duration: int
    booking_status: str = "confirmed"
    booking_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class KnowledgeBase:
    """Load and manage car inventory knowledge base."""

    def __init__(self, inventory_path: str = "data/car_inventory.json"):
        self.inventory_path = inventory_path
        self.data = self._load_inventory()
        self.bookings: List[TestDriveBooking] = []

    def _load_inventory(self) -> Dict[str, Any]:
        """Load car inventory from JSON file."""
        try:
            with open(self.inventory_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Inventory file not found: {self.inventory_path}")

    def search_cars_by_type(self, car_type: str) -> List[Dict[str, Any]]:
        """Search cars by type (e.g., 'sedan', 'SUV')."""
        results = []
        for car in self.data.get("inventory", []):
            if car_type.lower() in car.get("type", "").lower():
                results.append(car)
        return results

    def search_cars_by_brand(self, brand: str) -> List[Dict[str, Any]]:
        """Search cars by brand."""
        results = []
        for car in self.data.get("inventory", []):
            if brand.lower() in car.get("brand", "").lower():
                results.append(car)
        return results

    def get_car_details(self, car_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific car."""
        for car in self.data.get("inventory", []):
            if car.get("id") == car_id:
                return car
        return None

    def get_available_cars(self) -> List[Dict[str, Any]]:
        """Get all available cars for test drive."""
        return [car for car in self.data.get("inventory", []) if car.get("availability", False)]

    def get_working_hours(self) -> Dict[str, str]:
        """Get dealership working hours."""
        return self.data.get("working_hours", {})

    def check_time_availability(self, date_str: str, time_str: str) -> bool:
        """Check if a specific date and time is available."""
        try:
            # Simple availability check - in production, would query actual calendar
            requested_date = datetime.fromisoformat(date_str)
            if requested_date.date() < datetime.now().date():
                return False
            
            # Check if within 30 days
            if (requested_date.date() - datetime.now().date()).days > 30:
                return False
            
            return True
        except ValueError:
            return False

    def book_test_drive(self, booking: TestDriveBooking) -> bool:
        """Record a test drive booking."""
        self.bookings.append(booking)
        return True

    def get_dealership_info(self) -> Dict[str, Any]:
        """Get dealership contact and general information."""
        dealership = self.data.get("dealership", {})
        working_hours = self.data.get("working_hours", {})
        return {
            **dealership,
            "working_hours": working_hours,
        }


# ==================== Agent Tools ====================

class DealershipTools:
    """Tools for agents to interact with dealership data."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    @tool
    def search_car_by_type(self, car_type: str) -> str:
        """Search for cars by type (sedan, SUV, truck, compact, electric)."""
        results = self.kb.search_cars_by_type(car_type)
        if not results:
            return f"No cars found of type '{car_type}'"
        
        response = f"Found {len(results)} car(s) of type '{car_type}':\n"
        for car in results:
            response += f"- {car['brand']} {car['model']} ({car['year']}): ${car['price_range']}\n"
        return response

    @tool
    def get_car_details(self, car_id: str) -> str:
        """Get detailed information about a specific car."""
        car = self.kb.get_car_details(car_id)
        if not car:
            return f"Car with ID '{car_id}' not found"
        
        response = f"**{car['brand']} {car['model']} {car['year']}**\n"
        response += f"Type: {car['type']}\n"
        response += f"Price: {car['price_range']}\n"
        response += f"Features: {', '.join(car['features'][:5])}\n"
        response += f"Fuel Type: {car.get('fuel_type', 'N/A')}\n"
        response += f"MPG: {car.get('mpg', 'N/A')}\n"
        response += f"Seating: {car.get('seating_capacity', 'N/A')}\n"
        return response

    @tool
    def list_available_cars(self) -> str:
        """List all available cars for test drive."""
        cars = self.kb.get_available_cars()
        if not cars:
            return "No cars are currently available"
        
        response = "Available cars for test drive:\n"
        for car in cars:
            response += f"- {car['brand']} {car['model']} ({car['year']}) - ${car['price_range']}\n"
        return response

    @tool
    def check_availability(self, date: str, time: str) -> str:
        """Check if a specific date and time is available for test drive."""
        is_available = self.kb.check_time_availability(date, time)
        if is_available:
            return f"Great! {date} at {time} is available for booking."
        return f"Sorry, {date} at {time} is not available. Please choose another time."

    @tool
    def get_dealership_info(self) -> str:
        """Get dealership contact information and working hours."""
        info = self.kb.get_dealership_info()
        response = f"**{info['name']}**\n"
        response += f"Location: {info.get('location', 'N/A')}\n"
        response += f"Contact: {info.get('contact', 'N/A')}\n"
        response += f"Email: {info.get('email', 'N/A')}\n\n"
        response += "Working Hours:\n"
        for day, hours in info.get('working_hours', {}).items():
            response += f"- {day.capitalize()}: {hours}\n"
        return response

    @tool
    def book_test_drive(self, customer_name: str, customer_phone: str, car_id: str, 
                       preferred_date: str, preferred_time: str) -> str:
        """Book a test drive for a customer."""
        car = self.kb.get_car_details(car_id)
        if not car:
            return f"Cannot book: Car with ID '{car_id}' not found"

        if not self.kb.check_time_availability(preferred_date, preferred_time):
            return f"Cannot book: {preferred_date} at {preferred_time} is not available"

        booking = TestDriveBooking(
            booking_id=f"TD-{int(datetime.now().timestamp())}",
            customer_name=customer_name,
            customer_phone=customer_phone,
            car_model=f"{car['brand']} {car['model']}",
            car_id=car_id,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            test_drive_duration=car.get("test_drive_duration_minutes", 60),
        )

        success = self.kb.book_test_drive(booking)
        if success:
            return (
                f"✓ Test drive booked successfully!\n"
                f"Booking ID: {booking.booking_id}\n"
                f"Car: {booking.car_model}\n"
                f"Date: {booking.preferred_date} at {booking.preferred_time}\n"
                f"Duration: {booking.test_drive_duration} minutes\n"
                f"Confirmation sent to {customer_phone}"
            )
        return "Failed to book test drive. Please try again."

    def get_tools(self) -> List[LangchainTool]:
        """Get all tools as LangChain Tool objects."""
        return [
            LangchainTool(
                name="search_car_by_type",
                description="Search for cars by type (sedan, SUV, truck, compact, electric)",
                func=self.search_car_by_type,
            ),
            LangchainTool(
                name="get_car_details",
                description="Get detailed information about a specific car by ID",
                func=self.get_car_details,
            ),
            LangchainTool(
                name="list_available_cars",
                description="List all available cars for test drive",
                func=self.list_available_cars,
            ),
            LangchainTool(
                name="check_availability",
                description="Check if a specific date and time is available for test drive",
                func=self.check_availability,
            ),
            LangchainTool(
                name="get_dealership_info",
                description="Get dealership contact information and working hours",
                func=self.get_dealership_info,
            ),
            LangchainTool(
                name="book_test_drive",
                description="Book a test drive for a customer",
                func=self.book_test_drive,
            ),
        ]


# ==================== Agents ====================

class ConversationAgent:
    """Agent responsible for understanding customer intent and managing dialogue."""

    def __init__(self, tools: List[LangchainTool], model_name: str = "gpt-4"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.tools = tools
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
        self.agent_executor = self._setup_agent()

    def _setup_agent(self) -> AgentExecutor:
        """Set up the agent executor."""
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a friendly and professional auto dealership assistant. Your role is to:
1. Greet customers warmly
2. Understand their intent (e.g., test drive a car)
3. Ask clarifying questions about their preferences
4. Help them find the perfect vehicle
5. Book test drives when requested
6. Provide information about the dealership

Always be polite, helpful, and try to understand the customer's needs. Use the available tools to search for cars, check availability, and book test drives."""
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "human",
                "{input}"
            ),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

        executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
        )
        return executor

    def process_input(self, user_input: str) -> str:
        """Process user input and return agent response."""
        try:
            response = self.agent_executor.invoke({"input": user_input})
            return response.get("output", "I didn't understand that. Can you please rephrase?")
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"


class KnowledgeAgent:
    """Specialized agent for querying car information."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.5,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    def get_car_recommendations(self, preferences: Dict[str, str]) -> List[Dict[str, Any]]:
        """Recommend cars based on customer preferences."""
        car_type = preferences.get("type", "").lower()
        budget = preferences.get("budget", "")
        
        results = self.kb.search_cars_by_type(car_type) if car_type else self.kb.get_available_cars()
        return results[:3]  # Return top 3 recommendations


class BookingAgent:
    """Specialized agent for managing test drive bookings."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    def confirm_booking(self, booking_details: Dict[str, str]) -> bool:
        """Confirm and finalize a booking."""
        required_fields = ["customer_name", "customer_phone", "car_id", "preferred_date", "preferred_time"]
        if not all(field in booking_details for field in required_fields):
            return False
        
        booking = TestDriveBooking(
            booking_id=f"TD-{int(datetime.now().timestamp())}",
            customer_name=booking_details["customer_name"],
            customer_phone=booking_details["customer_phone"],
            car_model=booking_details.get("car_model", ""),
            car_id=booking_details["car_id"],
            preferred_date=booking_details["preferred_date"],
            preferred_time=booking_details["preferred_time"],
            test_drive_duration=booking_details.get("duration", 60),
        )
        
        return self.kb.book_test_drive(booking)

    def get_booking_confirmation(self, booking_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve booking confirmation details."""
        for booking in self.kb.bookings:
            if booking.booking_id == booking_id:
                return booking.dict()
        return None
