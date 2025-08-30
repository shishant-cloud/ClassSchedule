# ClassSchedule

A simple classroom scheduling and management web application built with Python and Flask. This app allows administrators and students to manage class schedules, attendance, assignments, and events using a user-friendly web interface. Data is stored in JSON files, making it easy to deploy and maintain without a database.

## Features

- **Admin Dashboard**: Manage users, schedules, assignments, attendance, and events.
- **Student Dashboard**: View schedules, assignments, attendance, and events.
- **User Authentication**: Separate login for admins and students.
- **Class Scheduling**: Add, view, and manage class schedules.
- **Attendance Tracking**: Mark and view attendance records.
- **Assignment Management**: Add and view assignments with links.
- **Event Calendar**: Add and view important events (exams, holidays, etc).
- **Simple Data Storage**: All data is stored in JSON files (no database required).

## Folder Structure

```
ClassSchedule/
├── app.py                # Flask app and routes
├── data_manager.py       # Handles all data storage and retrieval
├── main.py               # Entry point to run the app
├── data/                 # JSON files for users, schedules, attendance, assignments, events
├── static/               # Static files (CSS)
├── templates/            # HTML templates for all pages
├── pyproject.toml        # Project metadata
├── uv.lock               # Dependency lock file
└── replit.md             # Replit configuration (if using Replit)
```

## Getting Started

### Prerequisites
- Python 3.8+
- Flask (`pip install flask`)

### Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/ClassSchedule.git
   cd ClassSchedule
   ```
2. **Install dependencies:**
   ```sh
   pip install flask
   ```
3. **Run the application:**
   ```sh
   python main.py
   ```
   The app will be available at `http://localhost:5000`.

## Usage
- **Admin Login:** Username: `admin`, Password: `admin123`
- **Student Login:** Username: `student1`, Password: `student123`
- Access different dashboards and features based on your role.

## Customization
- To add more users, edit `data/users.json` or use the registration page.
- To change the admin password, use the admin settings page.

## Security Note
- Passwords are stored in plain text for simplicity. For production, use password hashing and secure authentication.

## License
This project is licensed under the MIT License.
