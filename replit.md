# Overview

A classroom management web application built with Flask that provides scheduling, attendance tracking, and assignment management features. The system supports role-based access with separate dashboards for administrators and students. Administrators can manage schedules, track attendance, create assignments, and organize events, while students have read-only access to view their information.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Web Framework
- **Flask**: Lightweight Python web framework chosen for its simplicity and ease of learning
- **Session-based Authentication**: Uses Flask sessions with a secret key for user login state management
- **Role-based Access Control**: Implements admin and student roles with different permission levels

## Frontend Architecture
- **Server-side Rendering**: Uses Jinja2 templating engine with HTML templates
- **Bootstrap CSS Framework**: Provides responsive design and consistent UI components
- **Static Assets**: Custom CSS for additional styling stored in `/static` directory
- **Responsive Design**: Mobile-friendly interface using Bootstrap's grid system

## Data Storage
- **JSON File-based Storage**: Uses local JSON files instead of a traditional database
- **File Structure**: Separate JSON files for users, schedules, attendance, assignments, and events
- **Data Manager Pattern**: Centralized `DataManager` class handles all file I/O operations
- **Error Handling**: Graceful handling of missing or corrupted JSON files

## Application Structure
- **MVC Pattern**: Clear separation with routes in `app.py`, data logic in `data_manager.py`, and views in templates
- **Module Organization**: Main application logic separated from server startup (`main.py`)
- **Template Inheritance**: Consistent layout across pages using shared navigation and styling

## Security Considerations
- **Environment Variables**: Session secret key configurable via environment variables
- **Form-based Authentication**: Simple username/password authentication
- **Session Management**: Server-side session storage for user state

## User Interface Design
- **Dual Dashboard System**: Separate interfaces for admin and student roles
- **CRUD Operations**: Full create, read, update, delete functionality for admin users
- **Read-only Access**: Students can view but not modify data
- **Navigation Consistency**: Shared navigation bar across all authenticated pages

# External Dependencies

## Frontend Libraries
- **Bootstrap CSS**: Dark theme variant hosted on CDN for styling and responsive layout
- **Custom CSS**: Local stylesheet for application-specific styling overrides

## Python Packages
- **Flask**: Core web framework for routing, templating, and session management
- **Standard Library**: Uses built-in `json`, `os`, `datetime`, and `logging` modules

## Development Tools
- **Debug Mode**: Flask development server with debugging enabled
- **Logging**: Python logging module for debugging and error tracking
- **Port Configuration**: Runs on port 5000 with external access enabled

## Data Storage
- **Local File System**: JSON files stored in `/data` directory for persistence
- **No External Database**: Self-contained storage solution requiring no additional services