#!/usr/bin/env bash

# Path to your project (can be ".")
WATCH_DIR="."

# Flask settings
export FLASK_APP=app.py
export FLASK_ENV=development

# Function to start Flask
start_flask() {
    echo "Starting Flask..."
    flask run --host=0.0.0.0 --port=5000 &
    FLASK_PID=$!
}

# Function to stop Flask
stop_flask() {
    if [ -n "$FLASK_PID" ]; then
        echo "Stopping Flask (PID: $FLASK_PID)..."
        kill $FLASK_PID
    fi
}

cleanup(){
    echo "Ctrl-C: Exit. Cleaning..."
    if pgrep flask > /dev/null; then
        kill -9 $(pgrep flask)
        exit 0
    fi
}

trap cleanup SIGINT

# Start first run
start_flask

# Watch for changes
echo "Watching for changes in $WATCH_DIR..."
inotifywait -m -r -e modify,create,delete,move "$WATCH_DIR" \
--exclude '(\.git|__pycache__|\.pyc|\.db|\.sqlite|\.log|^\.?/static/uploads/)' |
while read -r directory events filename; do
    echo "Change detected: $filename"
    stop_flask
    start_flask
done

