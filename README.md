# README
## Project Title: Weapon Detection System using YOLOv3 and Flask
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

> ### Project Overview
> Weapon Detection System is a real-time web application that utilizes YOLOv3 for automated weapon detection through webcam feed. Built with Flask and OpenCV, this system provides real-time object detection with confidence scores, making it a valuable tool for security monitoring. The application features a clean, browser-based interface with live video processing capabilities.

<br/>

![Screenshot](https://github.com/user-attachments/assets/f16fb1b7-ac29-45bb-a770-afd6432fb5c0)


### ✨ Key Features

| |
|---|
| 🎯 Real-time Detection with YOLOv3 |
| 🎥 Live Video Feed Processing |
| 🌐 Clean Browser-based Interface |
| 📊 Detection Confidence Scoring |
| 🔒 Secure Camera Permission System |
| 💻 Cross-platform Compatibility |


## Installation Guidelines
1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/swatified/weapon-detection-system.git
   ```
2. **Navigate to the Project Directory**: 
   ```bash
   cd weapon-detection-system
   ```
3. **Create and Activate Virtual Environment**: 
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```
4. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Download YOLOv3 Files**:
   - Place `yolov3_training_2000.weights` in the `weights` folder
   - Place `yolov3_testing.cfg` in the `weights` folder

6. **Start the Application**:
   ```bash
   python app.py
   ```
<br/>

## Usage Guide
- Open `http://localhost:5000` in your browser
- Allow camera permissions when prompted
- The system will begin real-time weapon detection
- Detection results show confidence scores and bounding boxes
- Configure detection parameters in `camera.py` if needed
<br/><br/>

## Project Structure
```
weapon_detection/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/
│   ├── base.html
│   └── index.html
├── weights/
│   ├── yolov3_training_2000.weights
│   └── yolov3_testing.cfg
├── app.py
├── camera.py
├── requirements.txt
└── README.md
```


### Important Notes
- This system is for educational purposes only
- Ensure appropriate permissions and legal compliance before deployment
- System accuracy depends on training data quality and environmental conditions

### Contribution Guidelines
Contributions are welcome! If you find a bug or have a feature request, feel free to open an issue or submit a pull request.

### Contact Me
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2.svg?style=for-the-badge&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/dev-swati/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://www.github.com/swatified/)
