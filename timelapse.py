import cv2
import numpy as np
from datetime import datetime, timedelta
import time
import os

# Arduino Code as Comment
'''
const int buttonPin = 2; // Change this to the pin where you connect the button

void setup() {
  pinMode(buttonPin, INPUT);
  Serial.begin(9600);
}

void enterSleepMode() {
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  attachInterrupt(digitalPinToInterrupt(buttonPin), wakeUp, HIGH);
  sleep_mode();
  sleep_disable();
  detachInterrupt(digitalPinToInterrupt(buttonPin));
}

void wakeUp() {
  // Do nothing on wake-up
}

void loop() {
  if (digitalRead(buttonPin) == HIGH) {
    // Send a signal to the Python script to capture an image
    Serial.println("Capture");
    delay(1000); // Debounce delay
  }

  // Enter sleep mode for power savings
  enterSleepMode();
}
'''

IMAGES_FOLDER = "images"
MONTHLY_VIDEO_FOLDER = "MonthlyVideo"
SIX_MONTH_VIDEO_FOLDER = "SixMonthVideo"
YEARLY_VIDEO_FOLDER = "OneYearVideo"

CAPTURE_INTERVAL = 300  # 5 minutes in seconds

# Variable to store the start time of the current video
current_video_start_time = datetime.now()

# Rest of the Python code remains unchanged...

def capture_image():
    # Use cv2 to capture an image
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = os.path.join(IMAGES_FOLDER, f"{timestamp}.jpg")
    camera = cv2.VideoCapture(0)  # Use 0 for the default camera
    _, frame = camera.read()

    # Increase brightness of the image
    brightness_factor = 2.0  # Adjust as needed
    brightened_frame = cv2.addWeighted(frame, brightness_factor, np.zeros(frame.shape, frame.dtype), 0, 0)

    # Add text to the image
    brightened_frame = add_text_to_image(brightened_frame, timestamp)

    cv2.imwrite(image_path, brightened_frame)
    camera.release()
    return image_path

def add_text_to_image(image, timestamp):
    global current_video_start_time  # Use the global variable

    # Calculate the duration of the current video
    video_duration = datetime.now() - current_video_start_time

    # Add text to the top of the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_content = (
        f"{datetime.now().strftime('%H:%M:%S')}  {datetime.now().strftime('%Y-%m-%d')}  "
        f"{datetime.now().strftime('%A')}  Created by Ahmed Alzeidi Software Engineering\n"
        f"Video Duration: {str(video_duration).split('.')[0]}")
    text_color = (0, 255, 255)  # Yellow color in BGR format
    font_scale = 0.8
    font_thickness = 1
    text_size = cv2.getTextSize(text_content, font, font_scale, font_thickness)[0]
    text_position = ((image.shape[1] - text_size[0]) // 2, 20)
    cv2.putText(image, text_content, text_position, font, font_scale, text_color, font_thickness, cv2.LINE_AA)

    return image

def create_video(images_folder, video_name):
    global current_video_start_time  # Use the global variable

    image_files = [f for f in os.listdir(images_folder) if f.endswith(".jpg")]
    image_files.sort()

    if not image_files:
        print("No images found to create video.")
        return

    video_path = os.path.join(video_name, f"{video_name}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    frame = cv2.imread(os.path.join(images_folder, image_files[0]))
    video = cv2.VideoWriter(video_path, fourcc, 1, (frame.shape[1], frame.shape[0]))

    for image_file in image_files:
        image_path = os.path.join(images_folder, image_file)
        frame = cv2.imread(image_path)

        # Increase brightness of the video frames
        alpha = 2.0  # Brightness factor, adjust as needed
        brightened_frame = cv2.multiply(frame, np.array([alpha]))

        # Add text to the video frames
        brightened_frame = add_text_to_image(brightened_frame, image_file.split(".")[0])

        video.write(brightened_frame)

    video.release()
    print(f"Video '{video_name}.mp4' created successfully.")

if __name__ == "__main__":
    try:
        while True:
            # Capture one snapshot every 5 minutes
            capture_image()
            time.sleep(CAPTURE_INTERVAL)

            # Update the start time of the current video
            current_video_start_time = datetime.now()

            # Create Monthly Video
            create_video(IMAGES_FOLDER, MONTHLY_VIDEO_FOLDER)

            # Create 6-Month Video (after 6 months)
            if datetime.now().month % 6 == 0:
                create_video(IMAGES_FOLDER, SIX_MONTH_VIDEO_FOLDER)

            # Create Yearly Video (after 12 months)
            if datetime.now().month == 12:
                create_video(IMAGES_FOLDER, YEARLY_VIDEO_FOLDER)

    except KeyboardInterrupt:
        print("Script interrupted. Exiting.")
