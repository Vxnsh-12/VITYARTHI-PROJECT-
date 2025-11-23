● Project Title --SLEEPGUARD SMART DRIVER ALARMING SYSTEM 

● Overview of the Project

Drowsy driving is a leading cause of traffic accidents worldwide. Traditional monitoring solutions are often passive, merely recording footage without active intervention.

SleepGuard is an Active Intervention System designed to enhance road safety. It transforms a standard laptop webcam into an intelligent sensor that monitors a driver's head posture in real-time. Utilizing computer vision, the system detects signs of fatigue (specifically nodding off) and triggers an immediate audio-visual alarm to wake the driver.It also collects a evidence of that exact moment when the person fell asleep in a dedicated folder.

● Features

Gamified Safety Score (Health Bar):
Unlike simple on/off detectors, SleepGuard employs a dynamic "Fatigue Score" (0-100). This intuitive "Health Bar" visualizes the driver's alertness level—decreasing when the head drops and regenerating when posture is corrected.

Adaptive posture calibiration:
The system eliminates the need for manual setup or hard-coded values. Upon initialization, it performs a 3-second "Learning Phase," analyzing the driver's specific height and seating position to establish a personalized safety baseline.

Offline evidence collection :
Designed for reliability, the system operates entirely offline. In the event of a detected microsleep, it automatically generates a secure 'evidence' folder, saving a timestamped photo of the incident along with a detailed text log entry.

 Heads-Up Display (HUD):
A futuristic, transparent overlay is drawn directly onto the video feed using image processing techniques. This HUD provides critical real-time feedback, including system status, low-light warnings, and target tracking indicators.

Integrated Command Center using python library:
A professional Graphical User Interface (GUI) serves as the launchpad, allowing users to easily initialize the camera, view logs, or shut down the system with a single click.

● Technologies/Tools Used

Programming Language: Python 3.x

Core Logic: Geometric Centroid Tracking (Vertical Displacement Analysis)

Computer Vision Library: OpenCV (cv2) - For face detection and image manipulation.

Numerical Processing: NumPy - For calculating averages and handling array data.

User Interface (GUI): Tkinter - For the main menu/launchpad window.

Audio Alerts: Winsound (Built-in Windows library) - For generating alarm beeps.

File Management: OS & Subprocess modules - For file creation and folder management.

AI Model: Haar Cascade Classifiers (haarcascade_frontalface_default.xml) - For robust face detection.

● Steps to Install & Run the Project

Install Python: Ensure Python 3.x is installed on your machine.

Install Dependencies: Open your Command Prompt (CMD) or Terminal and run the following command:
pip install opencv-python numpy

Download the Model: You must download the haarcascade_frontalface_default.xml file from the official OpenCV repository.

Download Link: https://github.com/opencv/opencv/tree/master/data/haarcascades

File Setup: Create a project folder and ensure the following two files are inside it:

The Python script main.py  which is inside the repository 

The XML file (haarcascade_frontalface_default.xml) given inside the repo as well .

Launch:

Open the project folder in File Explorer.

Click the address bar at the top, type cmd, and press Enter.

In the black window, type: python main.py 

● Instructions for Testing

Initialize: On the SleepGuard Command Center window, click the green "INITIALIZE CAMERA" button.

Calibrate: Sit upright and look directly at the webcam. Wait for the yellow "CALIBRATING..." text on the screen to reach 100% and listen for the confirmation BEEP.

Monitor: Observe the Green "HP Bar" on the left side of the HUD. This indicates normal alertness.

Simulate Fatigue: Slowly lower your head (chin towards chest) to mimic falling asleep.

Observe Reaction: Watch the HP Bar deplete. Once it hits zero, the screen will flash RED, and the audio alarm will sound.

Review Evidence: Press 'q' on your keyboard to close the camera. Back on the main menu, click "OPEN LOCAL LOGS" to verify that the system successfully captured and saved the incident photo and text log.
