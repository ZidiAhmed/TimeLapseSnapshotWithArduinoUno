# Time-Lapse Snapshot System

## Overview
The Time-Lapse Snapshot System is a versatile solution designed to capture images at specified intervals and create time-lapse videos. It includes both Python and Arduino components for seamless integration and extended functionality.

## Components
1. **Python Script:**
   - Captures images at regular intervals.
   - Embeds timestamp, date, and day name in each image.
   - Organizes images into folders based on capture frequency.
   - Creates time-lapse videos from captured images.

2. **Arduino Integration:**
   - Enables low-power operation and hardware-triggered image capture.
   - Enhances battery efficiency for long-term projects.

## Features
- Long-term image capture for projects spanning months or years.
- Adjustable capture intervals to suit project requirements.
- Automatic compilation of images into monthly, 6-month, and yearly time-lapse videos.
- Embedded timestamp and date information for reference.
- Optional integration with Arduino for power-efficient operation.

## Installation
1. **Python Setup:**
   - Ensure Python is installed on your system.
   - Clone this repository to your local machine.
   - Install required Python dependencies using `pip install -r requirements.txt`.

2. **Arduino Setup:**
   - Connect the Arduino Uno to your computer.
   - Upload the provided Arduino sketch to the board.

3. **Usage:**
   - Run the Python script using `python timelapse.py`.
   - Adjust settings as needed in the script (e.g., capture interval).

## Battery and Memory Requirements
- Battery life depends on capture frequency and project duration.
- Ensure sufficient memory for storing images and videos on the device.

## Contributors
- Ahmed Alzeidi

## License
This project is licensed under the [MIT License](LICENSE).

