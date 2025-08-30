# This is the MAIN starting file for our classroom scheduler
# Think of this as pressing the "START" button for our website
# It tells Python to run our web application

# Import our Flask app from the app.py file
from app import app

# This only runs when we start this file directly
if __name__ == '__main__':
    # Start our web server
    # host='0.0.0.0' - lets anyone access our website
    # port=5000 - our website will be available at :5000
    # debug=True - shows us helpful error messages
    app.run(host='0.0.0.0', port=5000, debug=True)
