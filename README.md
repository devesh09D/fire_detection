# 🔥 Fire Detection System

A real-time fire detection system that uses OpenCV for enhanced fire detection in video streams. The system leverages Flask for the backend and Flask-SocketIO for real-time updates to the frontend.

## 🚀 Features

- **Real-time Detection**: Detects fire in a video stream from a connected camera.
- **Enhanced Accuracy**: Utilizes multiple color spaces and contour analysis for reliable detection.
- **Confidence Scores**: Displays confidence levels of fire detection.
- **File Uploads**: Allows analyzing static image files for fire presence.
- **Web Interface**: User-friendly interface for monitoring and control.
- **Statistics Dashboard**: Tracks detection statistics including total frames, fire detected frames, and more.

---

## 📋 Project Structure

Fire-Detection-System/
├── app.py # Main Flask application
├── templates/
│ └── index.html # Frontend for the web interface
├── static/ # Static files (CSS/JS/images if needed)
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## 🛠️ Installation

### Prerequisites

- Python 3.7 or above
- pip (Python package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fire-detection-system.git
   cd fire-detection-system
pip install -r requirements.txt

python app.py

http://localhost:5000


🎥 Usage
Start Real-Time Detection
Navigate to the web interface at http://localhost:5000.

Click "Start Detection" to begin monitoring for fire using the connected camera.

Stop Detection
Click "Stop Detection" to end the monitoring session.



🖥️ API Endpoints
/api/start_detection
Method: POST

Description: Starts the real-time fire detection process.

/api/stop_detection
Method: POST

Description: Stops the real-time fire detection process.

/api/upload_and_analyze
Method: POST

Description: Uploads and analyzes an image file for fire detection.

Request Body: Multipart form-data containing image files.

/api/status
Method: GET

 Retrieves the current status and detection statistics.

🧪 Fire Detection Logic
Converts each video frame to multiple color spaces (HSV, LAB).

Masks the frame using specific color thresholds for fire-like colors.

Applies morphological operations to refine the mask.

Analyzes contours to detect significant fire regions.

Calculates confidence based on fire area and intensity.

🛡️ Error Handling
Displays errors if the camera cannot be accessed.

Handles exceptions during image processing gracefully.

Ensures application stability with clear logging.

📊 Statistics
The system tracks:

Total Frames Processed

Frames with Fire Detected

Alerts Sent

Last Detection Timestamp

📦 Dependencies
Flask

Flask-SocketIO

OpenCV

NumPy

Install all dependencies using:



pip install -r requirements.txt
🛠️ Future Enhancements
Multi-Camera Support: Extend to monitor multiple cameras simultaneously.

Improved Accuracy: Implement machine learning models for detection.

Mobile Notifications: Send alerts to mobile devices when fire is detected.

Cloud Integration: Save detection logs and stats in a cloud database.

🙌 Contribution
Fork the repository.

Create a new branch for your feature:


git checkout -b feature-name
Commit your changes:



git commit -m "Add your message here"
Push to your branch:



git push origin feature-name
Submit a pull request!





Image Analysis

🌟 Acknowledgements
Flask - Web framework

OpenCV - Computer vision library

Socket.IO - Real-time bi-directional communication

💬 Contact
For questions or support, feel free to reach out via your email or GitHub Issues.
EMAIL: devesh090905@gmail.com
