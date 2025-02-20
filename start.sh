#!/bin/bash
cd backend  # Move into the backend folder
gunicorn -w 4 -b 0.0.0.0:5000 app:app  # Start Flask with Gunicorn
