import cv2
import pytesseract
import datetime
import json
import re
import os  # Import the os module

# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = 'path to tesseract'

# Define the path to the JSON file
output_path = r'ok.json'

# Minimum number of seconds a plate must be out of the frame to be considered a new entry
min_seconds_between_entries = 5

# Function to recognize number plates in real-time video feed
def recognize_number_plates():
    cap = cv2.VideoCapture(0)  # Open the default camera (usually the built-in webcam)

    plate_log = []  # List to track entry and exit times

    recognized_plate = None

    # Check if the JSON file already exists and load its content
    if os.path.exists(output_path):
        with open(output_path, 'r') as json_file:
            plate_log = json.load(json_file)

    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        # Your number plate detection and recognition logic here
        # Use OpenCV for detection and pytesseract for character recognition

        # For example, you can use pytesseract for OCR
        plate_text = pytesseract.image_to_string(frame)
        
        # Apply regex to filter out unwanted characters
        clean_text = re.sub(r'[^A-Z0-9]', '', plate_text)

        current_time = datetime.datetime.now()

        # Check if the clean_text is not empty
        if clean_text:
            recognized_plate = clean_text

        # Display the recognized number plate on the video feed
        cv2.putText(frame, recognized_plate, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Number Plate Recognition', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('n') and recognized_plate:
            # Store the recognized plate when 'N' is pressed
            entry = {"plate": recognized_plate, "datetime": current_time.strftime('%Y-%m-%d %H:%M:%S')}
            plate_log.append(entry)
            with open(output_path, 'w') as json_file:
                json.dump(plate_log, json_file, indent=4)

    cap.release()
    cv2.destroyAllWindows()

# Call the function to start real-time recognition
recognize_number_plates()
