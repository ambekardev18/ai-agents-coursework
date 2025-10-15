# @title 📅 Task 5: Booking Agent - Smart Appointment Scheduling
# @markdown Natural language appointment booking system

class BookingStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Appointment:
    def __init__(self, appointment_id: str, user_id: str, service: str, 
                 scheduled_time: datetime, duration: int = 60):
        self.appointment_id = appointment_id
        self.user_id = user_id
        self.service = service
        self.scheduled_time = scheduled_time
        self.duration = duration
        self.status = BookingStatus.PENDING
        self.created_at = datetime.now()
        self.confirmed_at = None
    
    def confirm(self):
        self.status = BookingStatus.CONFIRMED
        self.confirmed_at = datetime.now()
    
    def to_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "user_id": self.user_id,
            "service": self.service,
            "scheduled_time": self.scheduled_time.strftime("%Y-%m-%d %H:%M"),
            "duration": self.duration,
            "status": self.status.value,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "confirmed_at": self.confirmed_at.strftime("%Y-%m-%d %H:%M") if self.confirmed_at else None
        }

class BookingAgent:
    def __init__(self):
        self.appointments = {}
        self.available_slots = self._generate_weekly_slots()
        self.services = {
            "doctor": {"duration": 30, "price": 100, "type": "medical"},
            "dentist": {"duration": 45, "price": 150, "type": "medical"},
            "therapy": {"duration": 60, "price": 120, "type": "wellness"},
            "consultation": {"duration": 30, "price": 80, "type": "professional"},
            "massage": {"duration": 60, "price": 90, "type": "wellness"},
            "checkup": {"duration": 20, "price": 60, "type": "medical"}
        }
        self.users = {}
        self.next_appointment_id = 1
    
    def _generate_weekly_slots(self) -> List[datetime]:
        """Generate available time slots for the next 7 days"""
        slots = []
        start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        for day in range(7):
            current_date = start_date + timedelta(days=day)
            # Skip weekends
            if current_date.weekday() >= 5:
                continue
            
            # Generate slots from 9 AM to 5 PM
            for hour in range(9, 17):
                for minute in [0, 30]:  # Slots at :00 and :30
                    slot_time = current_date.replace(hour=hour, minute=minute)
                    if slot_time > datetime.now() + timedelta(hours=1):  # Only future slots with 1hr buffer
                        slots.append(slot_time)
        
        return sorted(slots)
    
    def parse_booking_intent(self, user_message: str) -> Dict:
        """Advanced intent parsing with natural language understanding"""
        message_lower = user_message.lower()
        
        intent = {
            "service": None,
            "preferred_time": None,
            "date_preference": None,
            "urgency": "normal",
            "certainty": "high",
            "user_sentiment": "neutral"
        }
        
        # Extract service type with fuzzy matching
        for service in self.services.keys():
            if service in message_lower:
                intent["service"] = service
                break
        
        # If no direct service match, try partial matching
        if not intent["service"]:
            for service in self.services.keys():
                if any(word in message_lower for word in service.split()):
                    intent["service"] = service
                    break
        
        # Enhanced time/date parsing
        time_patterns = {
            "morning": "09:00-12:00",
            "afternoon": "12:00-17:00", 
            "evening": "17:00-20:00",
            "lunch": "12:00-13:00"
        }
        
        date_patterns = {
            "tomorrow": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "monday": self._next_weekday(0),
            "tuesday": self._next_weekday(1),
            "wednesday": self._next_weekday(2),
            "thursday": self._next_weekday(3),
            "friday": self._next_weekday(4),
            "next week": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        }
        
        for pattern, time_range in time_patterns.items():
            if pattern in message_lower:
                intent["preferred_time"] = time_range
        
        for pattern, date in date_patterns.items():
            if pattern in message_lower:
                intent["date_preference"] = date
        
        # Extract urgency and sentiment
        urgency_indicators = ['urgent', 'asap', 'emergency', 'quick', 'soon']
        positive_indicators = ['please', 'thank', 'appreciate', 'would like']
        
        if any(word in message_lower for word in urgency_indicators):
            intent["urgency"] = "high"
        if any(word in message_lower for word in positive_indicators):
            intent["user_sentiment"] = "positive"
        
        return intent
    
    def _next_weekday(self, weekday):
        """Get next specific weekday date"""
        today = datetime.now()
        days_ahead = weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return (today + timedelta(days_ahead)).strftime("%Y-%m-%d")
    
    def find_available_slots(self, service: str, date_preference: str = None) -> List[datetime]:
        """Find available slots for a service with preferences"""
        service_info = self.services.get(service)
        if not service_info:
            return []
        
        available = []
        for slot in self.available_slots:
            if not self._is_slot_booked(slot):
                slot_date = slot.strftime("%Y-%m-%d")
                if date_preference:
                    if slot_date == date_preference:
                        available.append(slot)
                else:
                    available.append(slot)
        
        return sorted(available)[:6]  # Return first 6 available slots
    
    def _is_slot_booked(self, slot: datetime) -> bool:
        """Check if a time slot is already booked"""
        for appointment in self.appointments.values():
            if (appointment.scheduled_time == slot and 
                appointment.status != BookingStatus.CANCELLED):
                return True
        return False
    
    def create_appointment(self, user_id: str, service: str, slot: datetime) -> Appointment:
        """Create a new appointment"""
        appointment_id = f"apt_{self.next_appointment_id:04d}"
        self.next_appointment_id += 1
        
        service_duration = self.services[service]["duration"]
        
        appointment = Appointment(
            appointment_id=appointment_id,
            user_id=user_id,
            service=service,
            scheduled_time=slot,
            duration=service_duration
        )
        
        appointment.confirm()
        self.appointments[appointment_id] = appointment
        self._remove_slot(slot)
        
        return appointment
    
    def _remove_slot(self, slot: datetime):
        """Remove slot from available slots"""
        self.available_slots = [s for s in self.available_slots if s != slot]
    
    def process_booking_request(self, user_id: str, user_message: str) -> Dict:
        """Process complete booking request with enhanced responses"""
        print(f"📞 Processing: '{user_message}'")
        
        # Step 1: Parse intent
        intent = self.parse_booking_intent(user_message)
        print(f"   Detected: {intent}")
        
        if not intent["service"]:
            return {
                "status": "clarification_needed",
                "message": "I understand you want to book an appointment. Which service are you interested in?",
                "available_services": list(self.services.keys()),
                "suggestions": ["doctor", "dentist", "therapy", "massage", "consultation"]
            }
        
        # Step 2: Find available slots
        available_slots = self.find_available_slots(
            intent["service"], 
            intent["date_preference"]
        )
        
        if not available_slots:
            return {
                "status": "no_slots", 
                "message": f"Sorry, no available slots found for {intent['service']} appointments.",
                "suggestion": "Please try a different date or service type.",
                "alternative_services": [s for s in self.services.keys() if s != intent["service"]]
            }
        
        # Step 3: Create appointment
        selected_slot = available_slots[0]
        appointment = self.create_appointment(user_id, intent["service"], selected_slot)
        
        # Step 4: Generate enhanced confirmation
        service_price = self.services[intent["service"]]["price"]
        service_type = self.services[intent["service"]]["type"]
        
        return {
            "status": "success",
            "appointment_id": appointment.appointment_id,
            "service": appointment.service,
            "scheduled_time": appointment.scheduled_time.strftime("%A, %B %d, %Y at %H:%M"),
            "duration": f"{appointment.duration} minutes",
            "price": f"${service_price}",
            "service_type": service_type,
            "confirmation_message": f"✅ {intent['service'].title()} Appointment Confirmed!",
            "details": f"📅 {appointment.scheduled_time.strftime('%A, %B %d, %Y')}\n🕒 {appointment.scheduled_time.strftime('%H:%M')} | ⏱️ {appointment.duration}min\n💼 Service: {intent['service'].title()}\n💰 Price: ${service_price}",
            "next_steps": [
                "📧 You will receive a confirmation email",
                "⏰ Reminder sent 24 hours before appointment",
                "📍 Please arrive 10 minutes early",
                "📋 Bring any relevant documents or IDs"
            ],
            "appointment_summary": f"Appointment {appointment.appointment_id} confirmed for {intent['service']} with {user_id}"
        }
    
    def get_booking_stats(self) -> Dict:
        """Get booking system statistics"""
        confirmed_count = sum(1 for apt in self.appointments.values() 
                             if apt.status == BookingStatus.CONFIRMED)
        
        return {
            "total_appointments": len(self.appointments),
            "confirmed_appointments": confirmed_count,
            "available_slots": len(self.available_slots),
            "services_offered": len(self.services),
            "next_available_slot": self.available_slots[0] if self.available_slots else None
        }

# Interactive Widget for Task 5
print("📅 TASK 5: Booking Agent - Smart Appointment Scheduling")
print("Natural language understanding for appointment booking")

booking_input = widgets.Textarea(
    value='I need a dentist appointment tomorrow afternoon',
    placeholder='Describe your appointment needs...',
    description='Request:',
    layout=widgets.Layout(width='80%', height='60px')
)

user_id_input = widgets.Text(
    value='dev ambekar',
    placeholder='Enter user ID...',
    description='User ID:',
    layout=widgets.Layout(width='200px')
)

booking_button = widgets.Button(description="Book Appointment", button_style='primary')
stats_button = widgets.Button(description="Show System Stats", button_style='info')
booking_output = widgets.Output()

def on_booking_click(b):
    with booking_output:
        clear_output()
        agent = BookingAgent()
        result = agent.process_booking_request(user_id_input.value, booking_input.value)
        
        print("📅 BOOKING AGENT RESPONSE")
        print("=" * 50)
        
        if result["status"] == "success":
            print(f"🎉 {result['confirmation_message']}")
            print(f"\n📋 APPOINTMENT DETAILS:")
            print(f"   {result['details']}")
            print(f"\n📝 NEXT STEPS:")
            for step in result["next_steps"]:
                print(f"   • {step}")
            print(f"\n🔢 Appointment ID: {result['appointment_id']}")
            
        elif result["status"] == "clarification_needed":
            print(f"❓ {result['message']}")
            print(f"💡 Available services: {', '.join(result['available_services'])}")
            
        elif result["status"] == "no_slots":
            print(f"😞 {result['message']}")
            print(f"💡 {result['suggestion']}")
            if 'alternative_services' in result:
                print(f"   Try: {', '.join(result['alternative_services'])}")

def on_stats_click(b):
    with booking_output:
        clear_output()
        agent = BookingAgent()
        stats = agent.get_booking_stats()
        
        print("📊 BOOKING SYSTEM STATISTICS")
        print("=" * 40)
        print(f"📈 Total Appointments: {stats['total_appointments']}")
        print(f"✅ Confirmed: {stats['confirmed_appointments']}")
        print(f"🕒 Available Slots: {stats['available_slots']}")
        print(f"🏥 Services Offered: {stats['services_offered']}")
        if stats['next_available_slot']:
            print(f"⏰ Next Available: {stats['next_available_slot'].strftime('%Y-%m-%d %H:%M')}")

booking_button.on_click(on_booking_click)
stats_button.on_click(on_stats_click)

display(widgets.HBox([user_id_input, booking_input]), 
        widgets.HBox([booking_button, stats_button]), 
        booking_output)