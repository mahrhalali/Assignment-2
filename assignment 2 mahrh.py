from datetime import datetime

class User:
    """Represents any user of the system."""
    def __init__(self, user_id, name, contact_info):
        self._user_id = user_id
        self._name = name
        self._contact_info = contact_info

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_contact_info(self):
        return self._contact_info

    def set_contact_info(self, info):
        self._contact_info = info

class LoyaltyRewards:
    """Manages loyalty rewards for guests."""
    def __init__(self, guest):
        self._guest = guest
        self._points = 0

    def add_points(self, points):
        self._points += points

class Guest(User):
    """Handles guest-specific information and actions."""
    def __init__(self, guest_id, name, contact_info, loyalty_status):
        super().__init__(guest_id, name, contact_info)
        self._loyalty_status = loyalty_status
        self._bookings = []
        self._feedbacks = []
        self._service_requests = []
        self._loyalty_rewards = LoyaltyRewards(self)

    def get_loyalty_status(self):
        return self._loyalty_status

    def set_loyalty_status(self, status):
        self._loyalty_status = status

    def add_booking(self, booking):
        self._bookings.append(booking)

    def add_feedback(self, feedback):
        self._feedbacks.append(feedback)

    def add_service_request(self, request):
        self._service_requests.append(request)

class Room:
    """Manages room details."""
    def __init__(self, room_number, room_type, price_per_night):
        self._room_number = room_number
        self._room_type = room_type
        self._price_per_night = price_per_night
        self._availability_status = True

    def is_available(self):
        return self._availability_status

    def set_availability(self, status):
        self._availability_status = status

class Booking:
    """Manages the booking process."""
    def __init__(self, booking_id, guest, room, check_in, check_out):
        self._booking_id = booking_id
        self._guest = guest
        self._room = room
        self._check_in = check_in
        self._check_out = check_out
        self._invoice = None

    def create_invoice(self, invoice_id, charges, payment_id, payment_method):
        self._invoice = Invoice(invoice_id, charges, payment_id, payment_method)

    def get_invoice(self):
        return self._invoice

class Invoice:
    """Handles invoicing and payments."""
    def __init__(self, invoice_id, charges, payment_id, payment_method):
        self._invoice_id = invoice_id
        self._charges = charges
        self._total_amount = sum(charges.values())
        self._payment = Payment(payment_id, self._total_amount, payment_method)

    def get_total_amount(self):
        return self._total_amount

    def get_payment(self):
        return self._payment

class Payment:
    """Processes payments for bookings."""
    def __init__(self, payment_id, amount, payment_method):
        self._payment_id = payment_id
        self._amount = amount
        self._payment_method = payment_method
        self._is_paid = False

    def process_payment(self):
        self._is_paid = True

    def is_paid(self):
        return self._is_paid

class ServiceRequest:
    """Tracks service requests from guests."""
    def __init__(self, request_id, guest, service_type):
        self._request_id = request_id
        self._guest = guest
        self._service_type = service_type
        self._status = "Pending"

    def set_status(self, status):
        self._status = status

class Feedback:
    """Collects and stores feedback from guests."""
    def __init__(self, feedback_id, guest, rating, comments):
        self._feedback_id = feedback_id
        self._guest = guest
        self._rating = rating
        self._comments = comments

# List of available rooms
rooms = [
    Room("101", "Single", 150),
    Room("102", "Double", 250),
    Room("103", "Suite", 400)
]

def show_available_rooms(room_list):
    """Displays available rooms."""
    print("\n--- Available Rooms ---")
    for room in room_list:
        if room.is_available():
            print("Room Number:", room._room_number, "| Type:", room._room_type, "| Price per night:", room._price_per_night)

def valid_date_range(check_in, check_out):
    """Validates that the check-out date is after the check-in date."""
    fmt = "%Y-%m-%d"
    checkin_date = datetime.strptime(check_in, fmt)
    checkout_date = datetime.strptime(check_out, fmt)
    if checkout_date <= checkin_date:
        raise ValueError("Check-out date must be after check-in date.")
    return True

if __name__ == "__main__":
    try:
        guest_name = input("Enter guest name: ")
        guest_contact = input("Enter guest phone number: ")
        loyalty_status = input("Enter loyalty status (Gold/Silver/None): ").capitalize()
        if loyalty_status not in ["Gold", "Silver", "None"]:
            raise ValueError("Loyalty status must be 'Gold', 'Silver', or 'None'.")

        guest = Guest(1, guest_name, guest_contact, loyalty_status)
        show_available_rooms(rooms)
        selected_room_number = input("Enter desired room number: ")
        selected_room = next((r for r in rooms if r._room_number == selected_room_number and r.is_available()), None)
        if not selected_room:
            raise ValueError("Selected room is unavailable or invalid.")

        check_in = input("Enter check-in date (YYYY-MM-DD): ")
        check_out = input("Enter check-out date (YYYY-MM-DD): ")
        if valid_date_range(check_in, check_out):
            num_days = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days

            booking = Booking(1, guest, selected_room, check_in, check_out)
            guest.add_booking(booking)
            selected_room.set_availability(False)

            service_type = input("Request a service (Housekeeping/Transportation/None): ")
            service_request = ServiceRequest(1, guest, service_type)
            guest.add_service_request(service_request)
            service_charge = 0 if service_type == "None" else 50

            charges = {"Room Charges": selected_room._price_per_night * num_days, "Service": service_charge}
            booking.create_invoice(1, charges, 1, "Credit Card")

            invoice = booking.get_invoice()
            payment = invoice.get_payment()
            payment.process_payment()

            rating = int(input("Rate your stay (1-5): "))
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5.")

            comments = input("Enter feedback comments: ")
            feedback = Feedback(1, guest, rating, comments)
            guest.add_feedback(feedback)

            print("--- Booking Summary ---")
            print("Guest Name:", guest.get_name())
            print("Room Number:", selected_room._room_number)
            print("Check-in Date:", booking._check_in)
            print("Check-out Date:", booking._check_out)
            print("Number of nights:", num_days)
            print("Invoice ID:", invoice._invoice_id)
            print("Total Invoice Amount:", invoice.get_total_amount())
            print("Payment Method:", payment._payment_method)
            print("Payment Status:", "Paid" if payment.is_paid() else "Not Paid")
            print("Service Charges:", charges["Service"])

            print("--- Service Request ---")
            print("Service Requested:", service_request._service_type)
            print("Request Status:", service_request._status)

            print("--- Guest Feedback ---")
            print("Rating:", feedback._rating)
            print("Comments:", feedback._comments)

    except ValueError as ve:
        print("Input error:", ve)
    except Exception as e:
        print("An unexpected error occurred:", e)
