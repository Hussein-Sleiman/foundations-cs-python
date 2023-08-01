import datetime  # Importing datetime module for date handling

class TicketingSystem:
    def __init__(self):
        self.special_list = []
        self.load_tickets_from_file()  # O(n)

    def load_tickets_from_file(self):
        try:
            with open('tickets.txt', 'r') as file:
                for line in file:  # O(n)
                    ticket_id, event_id, username, timestamp, priority = line.strip().split(', ')
                    self.special_list.append({
                        'ticket_id': ticket_id,
                        'event_id': event_id,
                        'username': username,
                        'timestamp': datetime.datetime.strptime(timestamp, '%Y%m%d').date(),  # O(1)
                        'priority': int(priority)  # O(1)
                    })
        except FileNotFoundError:
            print("Tickets file not found. Please make sure 'tickets.txt' exists.")  # O(1)

    def save_tickets_to_file(self):
        with open('tickets.txt', 'w') as file:
            for ticket in self.special_list:  # O(n)
                file.write(f"{ticket['ticket_id']}, {ticket['event_id']}, {ticket['username']}, "
                           f"{ticket['timestamp'].strftime('%Y%m%d')}, {ticket['priority']}\n")  # O(1)

    def validate_date(self, date_str):
        try:
            return datetime.datetime.strptime(date_str, '%Y%m%d').date()  # O(1)
        except ValueError:
            return None  # O(1)

    def validate_priority(self, priority_str):
        try:
            priority = int(priority_str)  # O(1)
            if priority < 0:  # O(1)
                raise ValueError
            return priority  # O(1)
        except ValueError:
            return None  # O(1)

    def validate_ticket_id(self, ticket_id):
        return any(ticket['ticket_id'] == ticket_id for ticket in self.special_list)  # O(n)

    def display_user_menu(self):
        while True:
            print("\nUser Menu:")
            print("1. Book a Ticket")
            print("2. Exit")
            choice = input("Enter your choice (1-2): ")  # O(1)

            if choice == '1':
                self.book_ticket()
            elif choice == '2':
                self.save_tickets_to_file()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")  # O(1)

    def display_admin_menu(self):
        attempts = 0  # O(1)
        while attempts < 5:
            username = input("Enter your username: ")  # O(1)
            password = input("Enter your password: ")  # O(1)

            if username.lower() == 'admin' and password == 'admin123123':  # O(1)
                while True:
                    print("\nAdmin Menu:")
                    print("1. Display Statistics")
                    print("2. Book a Ticket")
                    print("3. Display all Tickets")
                    print("4. Change Ticket's Priority")
                    print("5. Disable Ticket")
                    print("6. Run Events")
                    print("7. Exit")
                    choice = input("Enter your choice (1-7): ")  # O(1)

                    if choice == '1':
                        self.display_statistics()
                    elif choice == '2':
                        self.book_ticket()
                    elif choice == '3':
                        self.display_all_tickets()
                    elif choice == '4':
                        self.change_ticket_priority()
                    elif choice == '5':
                        self.disable_ticket()
                    elif choice == '6':
                        self.run_events()
                    elif choice == '7':
                        self.save_tickets_to_file()
                        print("Goodbye!")
                        break
                    else:
                        print("Invalid choice. Please try again.")  # O(1)
                break
            else:
                attempts += 1
                print("Incorrect Username and/or Password. Please try again.")  # O(1)
        else:
            print("Maximum login attempts reached. Exiting the program.")  # O(1)

    def display_statistics(self):
        event_counts = {}  # O(1)
        for ticket in self.special_list:  # O(n)
            event_id = ticket['event_id']  # O(1)
            event_counts[event_id] = event_counts.get(event_id, 0) + 1  # O(1)

        if not event_counts:  # O(1)
            print("No tickets found.")  # O(1)
            return  # O(1)

        max_event_id = max(event_counts, key=event_counts.get)  # O(n)
        print(f"The event ID with the highest number of tickets is: {max_event_id}")  # O(1)

    def book_ticket(self):
        event_id = input("Enter the event ID: ")  # O(1)
        date_str = input("Enter the date of the event (YYYYMMDD): ")  # O(1)
        event_date = self.validate_date(date_str)  # O(1)
        if event_date is None:  # O(1)
            print("Invalid date format. Please use YYYYMMDD.")  # O(1)
            return  # O(1)

        ticket_id = f"tick{len(self.special_list) + 1:03d}"  # O(1)
        username = input("Enter your username: ")  # O(1)
        priority_str = input("Enter the priority: ")  # O(1)
        priority = self.validate_priority(priority_str)  # O(1)
        if priority is None:  # O(1)
            print("Invalid priority. Priority should be a non-negative integer.")  # O(1)
            return  # O(1)

        self.special_list.append({
            'ticket_id': ticket_id,
            'event_id': event_id,
            'username': username,
            'timestamp': event_date,
            'priority': priority
        })  # O(1)

        print("Ticket booked successfully!")  # O(1)

    def display_all_tickets(self):
        today = datetime.date.today()  # O(1)
        all_events = [event for event in self.special_list if event['timestamp'] >= today]  # O(n)
        if not all_events:  # O(1)
            print("No tickets found.")  # O(1)
            return  # O(1)

        print("\nAll Tickets:")
        for event in sorted(all_events, key=lambda x: (x['timestamp'], x['event_id'])):  # O(n log n)
            print(f"Ticket ID: {event['ticket_id']}, Event ID: {event['event_id']}, "
                  f"Date: {event['timestamp'].strftime('%Y-%m-%d')}, Priority: {event['priority']}")  # O(1)

    def change_ticket_priority(self):
        ticket_id = input("Enter the ticket ID to change its priority: ")  # O(1)
        if not self.validate_ticket_id(ticket_id):  # O(n)
            print("Invalid ticket ID.")  # O(1)
            return  # O(1)

        new_priority_str = input("Enter the new priority: ")  # O(1)
        new_priority = self.validate_priority(new_priority_str)  # O(1)
        if new_priority is None:  # O(1)
            print("Invalid priority. Priority should be a non-negative integer.")  # O(1)
            return  # O(1)

        for event in self.special_list:  # O(n)
            if event['ticket_id'] == ticket_id:  # O(1)
                event['priority'] = new_priority  # O(1)
                print("Priority updated successfully!")  # O(1)
                break  # O(1)

    def disable_ticket(self):
        ticket_id = input("Enter the ticket ID to disable: ")  # O(1)
        for event in self.special_list:  # O(n)
            if event['ticket_id'] == ticket_id:  # O(1)
                self.special_list.remove(event)  # O(n)
                print("Ticket disabled successfully!")  # O(1)
                return  # O(1)

        print("Ticket ID not found.")  # O(1)

    def run_events(self):
        today = datetime.date.today()  # O(1)
        today_events = [event for event in self.special_list if event['timestamp'] == today]  # O(n)
        if not today_events:  # O(1)
            print("No events today.")  # O(1)
            return  # O(1)

        print("\nToday's Events:")
        for event in sorted(today_events, key=lambda x: x['priority'], reverse=True):  # O(n log n)
            print(f"Event ID: {event['event_id']}, Priority: {event['priority']}")  # O(1)

        self.special_list = [event for event in self.special_list if event not in today_events]  # O(n)

if __name__ == "__main__":
    ticketing_system = TicketingSystem()
    
    while True:
        print("\nLogin:")
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")  # O(1)
        
        if choice == '1':
            ticketing_system.display_admin_menu()
        elif choice == '2':
            ticketing_system.display_user_menu()
        elif choice == '3':
            print("Goodbye!")  # O(1)
            ticketing_system.save_tickets_to_file()  # O(n)
            break
        else:
            print("Invalid choice. Please try again.")  # O(1)