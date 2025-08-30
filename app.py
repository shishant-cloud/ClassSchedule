# This is our main Flask application file
# It contains all the routes (URLs) and functions for our web app

import os
import logging
from flask import Flask, request, redirect, session, url_for
from data_manager import DataManager

# Set up logging to help with debugging
logging.basicConfig(level=logging.DEBUG)

# Create our Flask app
app = Flask(__name__)

# Set secret key for sessions (used to keep users logged in)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")

# Create our data manager to handle JSON files
data_manager = DataManager()

# Home page - redirects to login
@app.route('/')
def home():
    """
    This is the main page that users see first.
    If they're logged in, send them to their dashboard.
    If not, send them to login page.
    """
    if 'user_id' in session:
        # User is logged in, send them to their dashboard
        user = data_manager.get_user_by_id(session['user_id'])
        if user and user['role'] == 'admin':
            return redirect('/admin_dashboard')
        else:
            return redirect('/student_dashboard')
    else:
        # User is not logged in, send them to login page
        return redirect('/login')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This handles user login.
    GET request shows the login form.
    POST request processes the login.
    """
    if request.method == 'POST':
        # User submitted the login form
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password is correct
        user = data_manager.validate_user(username, password)
        if user:
            # Login successful - save user info in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            # Redirect to appropriate dashboard
            if user['role'] == 'admin':
                return redirect('/admin_dashboard')
            else:
                return redirect('/student_dashboard')
        else:
            # Login failed - show error message
            error = "Invalid username or password"
            return data_manager.read_html_file('templates/login.html').replace('{{error}}', error)
    
    # Show login form (GET request)
    return data_manager.read_html_file('templates/login.html').replace('{{error}}', '')

# Logout
@app.route('/logout')
def logout():
    """
    This logs out the user by clearing their session.
    """
    session.clear()
    return redirect('/login')

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    """
    This shows the admin dashboard.
    Only admins can access this page.
    """
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    
    return data_manager.read_html_file('templates/admin_dashboard.html')

# Student Dashboard
@app.route('/student_dashboard')
def student_dashboard():
    """
    This shows the student dashboard.
    Students and admins can access this page.
    """
    if 'user_id' not in session:
        return redirect('/login')
    
    return data_manager.read_html_file('templates/student_dashboard.html')

# Schedule Management
@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    """
    This handles the class schedule.
    GET request shows the schedule.
    POST request adds a new class (admin only).
    """
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST' and session.get('role') == 'admin':
        # Admin is adding a new class
        class_name = request.form['class_name']
        room = request.form['room']
        time = request.form['time']
        day = request.form['day']
        teacher = request.form['teacher']
        
        # Add the class to our schedule data
        data_manager.add_class(class_name, room, time, day, teacher)
    
    # Get all scheduled classes and show them
    classes = data_manager.get_all_classes()
    html_content = data_manager.read_html_file('templates/schedule.html')
    
    # Build the schedule table
    schedule_rows = ""
    for class_info in classes:
        schedule_rows += f"""
        <tr>
            <td>{class_info['day']}</td>
            <td>{class_info['time']}</td>
            <td>{class_info['class_name']}</td>
            <td>{class_info['room']}</td>
            <td>{class_info['teacher']}</td>
        </tr>
        """
    
    html_content = html_content.replace('{{schedule_rows}}', schedule_rows)
    
    # Show or hide add form based on user role
    if session.get('role') == 'admin':
        html_content = html_content.replace('{{admin_only}}', '')
    else:
        html_content = html_content.replace('{{admin_only}}', 'style="display:none"')
    
    return html_content

# Attendance Management
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    """
    This handles attendance tracking.
    GET request shows attendance records.
    POST request marks attendance (admin only).
    """
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST' and session.get('role') == 'admin':
        # Admin is marking attendance
        student_name = request.form['student_name']
        class_name = request.form['class_name']
        date = request.form['date']
        status = request.form['status']  # present or absent
        
        # Add attendance record
        data_manager.mark_attendance(student_name, class_name, date, status)
    
    # Get all attendance records and show them
    attendance_records = data_manager.get_attendance_records()
    html_content = data_manager.read_html_file('templates/attendance.html')
    
    # Build the attendance table
    attendance_rows = ""
    for record in attendance_records:
        status_class = "text-success" if record['status'] == 'present' else "text-danger"
        attendance_rows += f"""
        <tr>
            <td>{record['date']}</td>
            <td>{record['student_name']}</td>
            <td>{record['class_name']}</td>
            <td><span class="{status_class}">{record['status'].title()}</span></td>
        </tr>
        """
    
    html_content = html_content.replace('{{attendance_rows}}', attendance_rows)
    
    # Show or hide add form based on user role
    if session.get('role') == 'admin':
        html_content = html_content.replace('{{admin_only}}', '')
    else:
        html_content = html_content.replace('{{admin_only}}', 'style="display:none"')
    
    return html_content

# Assignments Management
@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    """
    This handles assignments and links repository.
    GET request shows all assignments.
    POST request adds new assignment (admin only).
    """
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST' and session.get('role') == 'admin':
        # Admin is adding a new assignment
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        link = request.form['link']  # Google Drive or other cloud link
        
        # Add the assignment
        data_manager.add_assignment(title, description, due_date, link)
    
    # Get all assignments and show them
    assignments_list = data_manager.get_all_assignments()
    html_content = data_manager.read_html_file('templates/assignments.html')
    
    # Build the assignments table
    assignment_rows = ""
    for assignment in assignments_list:
        assignment_rows += f"""
        <tr>
            <td>{assignment['title']}</td>
            <td>{assignment['description']}</td>
            <td>{assignment['due_date']}</td>
            <td><a href="{assignment['link']}" target="_blank" class="btn btn-sm btn-outline-primary">Open Link</a></td>
        </tr>
        """
    
    html_content = html_content.replace('{{assignment_rows}}', assignment_rows)
    
    # Show or hide add form based on user role
    if session.get('role') == 'admin':
        html_content = html_content.replace('{{admin_only}}', '')
    else:
        html_content = html_content.replace('{{admin_only}}', 'style="display:none"')
    
    return html_content

# Calendar
@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    """
    This shows important dates and events.
    GET request shows the calendar.
    POST request adds new event (admin only).
    """
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST' and session.get('role') == 'admin':
        # Admin is adding a new event
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        description = request.form['description']
        
        # Add the event
        data_manager.add_event(event_name, event_date, description)
    
    # Get all events and show them
    events = data_manager.get_all_events()
    html_content = data_manager.read_html_file('templates/calendar.html')
    
    # Build the events list
    event_items = ""
    for event in events:
        event_items += f"""
        <div class="card mb-2">
            <div class="card-body">
                <h6 class="card-title">{event['event_name']}</h6>
                <p class="card-text text-muted">Date: {event['event_date']}</p>
                <p class="card-text">{event['description']}</p>
            </div>
        </div>
        """
    
    html_content = html_content.replace('{{event_items}}', event_items)
    
    # Show or hide add form based on user role
    if session.get('role') == 'admin':
        html_content = html_content.replace('{{admin_only}}', '')
    else:
        html_content = html_content.replace('{{admin_only}}', 'style="display:none"')
    
    return html_content
