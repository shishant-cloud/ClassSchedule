# This is the main file that starts our web application
# It imports our Flask app and runs it on port 5000

from app import app

if __name__ == '__main__':
    # Start the web server on port 5000
    # host='0.0.0.0' means the app can be accessed from outside
    # debug=True helps us see errors when developing
    app.run(host='0.0.0.0', port=5000, debug=True)
