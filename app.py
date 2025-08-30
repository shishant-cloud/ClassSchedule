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

# Home page - shows login options
@app.route('/')
def home():
    """
    This is the main page that users see first.
    If they're logged in, send them to their dashboard.
    If not, show them login options (admin or student).
    """
    if 'user_id' in session:
        # User is logged in, send them to their dashboard
        user = data_manager.get_user_by_id(session['user_id'])
        if user and user['role'] == 'admin':
            return redirect('/admin_dashboard')
        else:
            return redirect('/student_dashboard')
    else:
        # User is not logged in, show them the main welcome page
        return data_manager.read_html_file('templates/index.html')

# Admin Login
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    """
    This handles admin login specifically.
    Only admin users can login here.
    """
    if request.method == 'POST':
        # Admin submitted the login form
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password is correct
        user = data_manager.validate_user(username, password)
        if user and user['role'] == 'admin':
            # Admin login successful - save user info in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            # Redirect to admin dashboard
            return redirect('/admin_dashboard')
        else:
            # Login failed - show error message
            error = '<div class="alert alert-danger">Invalid admin credentials or not an admin account!</div>'
            return data_manager.read_html_file('templates/admin_login.html').replace('{{error}}', error)
    
    # Show admin login form (GET request)
    return data_manager.read_html_file('templates/admin_login.html').replace('{{error}}', '')

# Student Login
@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    """
    This handles student login specifically.
    Only student users can login here.
    """
    if request.method == 'POST':
        # Student submitted the login form
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists and password is correct
        user = data_manager.validate_user(username, password)
        if user and user['role'] == 'student':
            # Student login successful - save user info in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            # Redirect to student dashboard
            return redirect('/student_dashboard')
        else:
            # Login failed - show error message
            error = '<div class="alert alert-danger">Invalid student credentials or not a student account!</div>'
            return data_manager.read_html_file('templates/student_login.html').replace('{{error}}', error)
    
    # Show student login form (GET request)
    return data_manager.read_html_file('templates/student_login.html').replace('{{error}}', '')

# General Login (kept for compatibility)
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    General login - redirects to home page to choose login type.
    """
    return redirect('/')

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

# Admin Settings - Change Password
@app.route('/admin_settings', methods=['GET', 'POST'])
def admin_settings():
    """
    Admin can change their password here.
    Only admin users can access this page.
    """
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')
    
    message = ""
    if request.method == 'POST':
        # Admin wants to change password
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Check if current password is correct
        admin_user = data_manager.get_user_by_id(session['user_id'])
        if admin_user is None or admin_user['password'] != current_password:
            message = '<div class="alert alert-danger">Current password is wrong!</div>'
        elif new_password != confirm_password:
            message = '<div class="alert alert-danger">New passwords do not match!</div>'
        elif len(new_password) < 6:
            message = '<div class="alert alert-danger">New password must be at least 6 characters!</div>'
        else:
            # Change the password
            data_manager.change_admin_password(session['user_id'], new_password)
            message = '<div class="alert alert-success">Password changed successfully!</div>'
    
    # Show the settings page
    html_content = data_manager.read_html_file('templates/admin_settings.html')
    html_content = html_content.replace('{{message}}', message)
    
    return html_content

# Student Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Students can register here using an invite code.
    This creates a new student account and can be accessed via admin's shared link.
    """
    if request.method == 'POST':
        # Student is trying to register
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        invite_code = request.form['invite_code']
        
        # Validate input fields
        if len(name.strip()) < 2:
            error = '<div class="alert alert-danger">Name must be at least 2 characters long!</div>'
            return data_manager.read_html_file('templates/register.html').replace('{{error}}', error)
        
        if len(username.strip()) < 3:
            error = '<div class="alert alert-danger">Username must be at least 3 characters long!</div>'
            return data_manager.read_html_file('templates/register.html').replace('{{error}}', error)
            
        if len(password) < 6:
            error = '<div class="alert alert-danger">Password must be at least 6 characters long!</div>'
            return data_manager.read_html_file('templates/register.html').replace('{{error}}', error)
        
        # Check if passwords match
        if password != confirm_password:
            error = '<div class="alert alert-danger">Passwords do not match!</div>'
            return data_manager.read_html_file('templates/register.html').replace('{{error}}', error)
        
        # Check if the invite code is correct
        if invite_code != "JOIN2024":  # Simple invite code
            error = '<div class="alert alert-danger">Invalid invite code! Ask your teacher for the correct code: <strong>JOIN2024</strong></div>'
            return data_manager.read_html_file('templates/register.html').replace('{{error}}', error)
        
        # Check if username already exists
        if data_manager.username_exists(username.strip()):
            error = '<div class="alert alert-danger">Username already exists! Please choose a different one.</div>'
            return data_manager.read_html_file('templates/register.html').replace('{{error}}', error)
        
        # Create new student account
        data_manager.add_student(name.strip(), username.strip(), password)
        success = '<div class="alert alert-success"><strong>Account created successfully!</strong><br>You can now <a href="/student_login" class="alert-link">login here</a> with your username and password.</div>'
        return data_manager.read_html_file('templates/register.html').replace('{{error}}', success)
    
    # Show registration form with pre-filled invite code if coming from admin link
    invite_code = request.args.get('code', '')  # Get invite code from URL if present
    html_content = data_manager.read_html_file('templates/register.html')
    html_content = html_content.replace('{{error}}', '')
    html_content = html_content.replace('{{invite_code}}', invite_code)
    return html_content

# Get Invite Link (Admin only)
@app.route('/invite_link')
def invite_link():
    """
    Shows the invite link that admin can share with students.
    Only admin can access this.
    """
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/admin_login')
    
    # Get the current website URL and create invite link
    base_url = request.host_url  # Gets the website's main URL
    invite_url = base_url + "register"
    invite_url_with_code = base_url + "register?code=JOIN2024"  # Pre-filled code
    invite_code = "JOIN2024"
    
    html_content = data_manager.read_html_file('templates/invite_link.html')
    html_content = html_content.replace('{{invite_url}}', invite_url)
    html_content = html_content.replace('{{invite_url_with_code}}', invite_url_with_code)
    html_content = html_content.replace('{{invite_code}}', invite_code)
    
    return html_content
