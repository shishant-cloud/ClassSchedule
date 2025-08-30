# DATA MANAGER - This handles all our data storage
# 
# What does this do?
# - Saves information to files (like a simple database)
# - Reads information from files
# - JSON files are just text files that store data in an organized way
# - Think of JSON like a digital filing cabinet with labeled folders

import json
import os
from datetime import datetime

class DataManager:
    """
    This class manages all our data stored in JSON files.
    JSON files are just text files that store data in an organized way.
    Think of them like spreadsheets but in text format.
    """
    
    def __init__(self):
        """
        Initialize the data manager.
        This runs when we create a DataManager object.
        It makes sure all our data folders and files exist.
        """
        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Initialize all our data files
        self.init_users()
        self.init_schedules()
        self.init_attendance()
        self.init_assignments()
        self.init_events()
    
    def read_json_file(self, filename):
        """
        Read data from a JSON file.
        JSON files store data like a Python dictionary or list.
        If the file doesn't exist, return an empty list.
        """
        try:
            with open(filename, 'r') as file:
                # Load the data from the file
                return json.load(file)
        except FileNotFoundError:
            # File doesn't exist, return empty list
            return []
        except json.JSONDecodeError:
            # File is corrupted, return empty list
            return []
    
    def write_json_file(self, filename, data):
        """
        Write data to a JSON file.
        This saves our Python data (lists, dictionaries) to a text file.
        indent=4 makes the file human-readable with nice formatting.
        """
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    
    def read_html_file(self, filename):
        """
        Read an HTML file and return its content.
        This is used because we can't use Jinja templates.
        """
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "<html><body><h1>File not found</h1></body></html>"
    
    def init_users(self):
        """
        Initialize the users data file.
        This creates default admin and student accounts if they don't exist.
        """
        users_file = 'data/users.json'
        users = self.read_json_file(users_file)
        
        if not users:  # If no users exist, create default ones
            default_users = [
                {
                    'id': 1,
                    'username': 'admin',
                    'password': 'admin123',  # In real apps, this should be encrypted
                    'role': 'admin',
                    'name': 'Administrator'
                },
                {
                    'id': 2,
                    'username': 'student1',
                    'password': 'student123',
                    'role': 'student',
                    'name': 'John Doe'
                }
            ]
            self.write_json_file(users_file, default_users)
    
    def init_schedules(self):
        """
        Initialize the schedules data file.
        This creates the file to store class schedules.
        """
        schedules_file = 'data/schedules.json'
        if not os.path.exists(schedules_file):
            self.write_json_file(schedules_file, [])
    
    def init_attendance(self):
        """
        Initialize the attendance data file.
        This creates the file to store attendance records.
        """
        attendance_file = 'data/attendance.json'
        if not os.path.exists(attendance_file):
            self.write_json_file(attendance_file, [])
    
    def init_assignments(self):
        """
        Initialize the assignments data file.
        This creates the file to store assignments and links.
        """
        assignments_file = 'data/assignments.json'
        if not os.path.exists(assignments_file):
            self.write_json_file(assignments_file, [])
    
    def init_events(self):
        """
        Initialize the events data file.
        This creates the file to store calendar events.
        """
        events_file = 'data/events.json'
        if not os.path.exists(events_file):
            self.write_json_file(events_file, [])
    
    def validate_user(self, username, password):
        """
        Check if a user's login is valid.
        Returns the user data if valid, None if invalid.
        """
        users = self.read_json_file('data/users.json')
        for user in users:
            if user['username'] == username and user['password'] == password:
                return user
        return None
    
    def get_user_by_id(self, user_id):
        """
        Find a user by their ID number.
        Returns the user data if found, None if not found.
        """
        users = self.read_json_file('data/users.json')
        for user in users:
            if user['id'] == user_id:
                return user
        return None
    
    def add_class(self, class_name, room, time, day, teacher):
        """
        Add a new class to the schedule.
        This adds a new row to our schedule data.
        """
        schedules = self.read_json_file('data/schedules.json')
        
        # Create a new class entry
        new_class = {
            'id': len(schedules) + 1,  # Simple ID assignment
            'class_name': class_name,
            'room': room,
            'time': time,
            'day': day,
            'teacher': teacher,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to our list and save
        schedules.append(new_class)
        self.write_json_file('data/schedules.json', schedules)
    
    def get_all_classes(self):
        """
        Get all scheduled classes.
        Returns a list of all classes in the schedule.
        """
        return self.read_json_file('data/schedules.json')
    
    def mark_attendance(self, student_name, class_name, date, status):
        """
        Record attendance for a student.
        Status can be 'present' or 'absent'.
        """
        attendance = self.read_json_file('data/attendance.json')
        
        # Create a new attendance record
        new_record = {
            'id': len(attendance) + 1,
            'student_name': student_name,
            'class_name': class_name,
            'date': date,
            'status': status,
            'recorded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to our list and save
        attendance.append(new_record)
        self.write_json_file('data/attendance.json', attendance)
    
    def get_attendance_records(self):
        """
        Get all attendance records.
        Returns a list of all attendance records.
        """
        return self.read_json_file('data/attendance.json')
    
    def add_assignment(self, title, description, due_date, link):
        """
        Add a new assignment to the repository.
        Link can be a Google Drive link or any other cloud storage.
        """
        assignments = self.read_json_file('data/assignments.json')
        
        # Create a new assignment entry
        new_assignment = {
            'id': len(assignments) + 1,
            'title': title,
            'description': description,
            'due_date': due_date,
            'link': link,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to our list and save
        assignments.append(new_assignment)
        self.write_json_file('data/assignments.json', assignments)
    
    def get_all_assignments(self):
        """
        Get all assignments.
        Returns a list of all assignments and their links.
        """
        return self.read_json_file('data/assignments.json')
    
    def add_event(self, event_name, event_date, description):
        """
        Add a new event to the calendar.
        Events are important dates like exams, holidays, etc.
        """
        events = self.read_json_file('data/events.json')
        
        # Create a new event entry
        new_event = {
            'id': len(events) + 1,
            'event_name': event_name,
            'event_date': event_date,
            'description': description,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to our list and save
        events.append(new_event)
        self.write_json_file('data/events.json', events)
    
    def get_all_events(self):
        """
        Get all calendar events.
        Returns a list of all events sorted by date.
        """
        events = self.read_json_file('data/events.json')
        # Sort events by date (most recent first)
        return sorted(events, key=lambda x: x['event_date'], reverse=True)
    
    def change_admin_password(self, user_id, new_password):
        """
        Change admin's password.
        This updates the admin's password in the users file.
        """
        users = self.read_json_file('data/users.json')
        
        # Find the admin user and update password
        for user in users:
            if user['id'] == user_id and user['role'] == 'admin':
                user['password'] = new_password
                break
        
        # Save the updated users list
        self.write_json_file('data/users.json', users)
    
    def username_exists(self, username):
        """
        Check if a username already exists.
        Returns True if username exists, False if it doesn't.
        """
        users = self.read_json_file('data/users.json')
        
        # Check each user to see if username matches
        for user in users:
            if user['username'] == username:
                return True
        return False
    
    def add_student(self, name, username, password):
        """
        Add a new student to the system.
        This creates a new student account.
        """
        users = self.read_json_file('data/users.json')
        
        # Create new student account
        new_student = {
            'id': len(users) + 1,  # Simple ID assignment
            'username': username,
            'password': password,
            'role': 'student',
            'name': name,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to our users list and save
        users.append(new_student)
        self.write_json_file('data/users.json', users)
