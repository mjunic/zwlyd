"""
This script runs the main application using a development server.
"""

from os import environ
from main import app
import os

if __name__ == '__main__':
    #os.startfile('server.py')
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
