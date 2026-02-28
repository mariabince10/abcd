
# Kerala Pothole Detection 
Basic Details

# # Team Name: Baddiesss

 # # # Team Members

Maria Bince – Mar athanascious college of engineering

Sadiya Shamsuddin – Mar athanascious college of engineering

# # Hosted Project Link

https://cjaogsegbnzutax6jnsas5.streamlit.app/

 # # Project Description

Kerala Pothole Detection is an AI-powered road damage monitoring system built using computer vision and Streamlit. It allows citizens to upload road images or capture live camera input to detect potholes, assess severity, extract GPS location, generate official PDF reports, and visualize complaints on an interactive Kerala map dashboard.

 # # Problem Statement

Potholes on roads in Kerala cause accidents, vehicle damage, and traffic disruption.

Current complaint systems:

Are manual and slow

Lack structured damage assessment

Do not provide geo-tagged reporting

Have no centralized visualization system

There is a need for an intelligent, automated road damage monitoring solution.

# # The Solution

We developed a computer vision-based system that:

Detects potholes using OpenCV edge detection and contour analysis

Classifies severity (LOW / MEDIUM / HIGH)

Extracts GPS location from image metadata (EXIF)

Generates official PWD-style PDF reports

Displays reports on a real-time interactive dashboard map

Filters images containing human faces for privacy

This creates a structured, transparent, and technology-driven complaint system.

# Technical Details
# # Technologies / Components Used
# # # For Software

Language Used

Python

Framework Used

Streamlit

Libraries Used

OpenCV (cv2)

NumPy

Pillow

piexif

Folium

streamlit-folium

ReportLab

Branca

Tools Used

VS Code

Git

GitHub

# Features

feature 1: Citizen road image upload

feature 2: Live camera pothole detection

 feature 3:Smart severity classification

 feature 4:GPS extraction from image metadata

 feature 5:Automated official PWD-style PDF report generation

 feature 6:Interactive Kerala dashboard with severity markers

 feature 7:Face detection for privacy filtering

 feature 8:Risk score calculation (0–100 scale)

 feature 9:Complaint registration simulation

 # Implementation
# # Installation

Clone the repository:

git clone https://github.com/yourusername/kerala-pothole-detection.git
cd kerala-pothole-detection

Install dependencies:

pip install streamlit opencv-python numpy pillow piexif folium streamlit-folium reportlab branca
Run the Application
streamlit run app.py

The app will open in your browser automatically.
# project documentation
 Citizen Upload Interface
<img width="1217" height="673" alt="Screenshot 2026-02-28 080314" src="https://github.com/user-attachments/assets/b40c8377-f8df-493c-959b-94719b54ca7f" />=
The system detects four pothole regions with a total relative damaged area of 2966, classifies the severity as LOW (adjustable by the user), and—since no GPS metadata was found—prompts retrieval of the current location (10.850500, 76.271100) while also displaying contextual data like recent rainfall for risk evaluation


<img width="1830" height="856" alt="Screenshot 2026-02-28 080323" src="https://github.com/user-attachments/assets/aa3f56ef-b434-4651-9604-e24120ec911b" />=
The system detects four pothole regions with a total relative damaged area of 2966, confirms LOW severity (user-adjustable), retrieves current GPS coordinates (10.850500, 76.271100) due to missing EXIF data, factors in assumed rainfall (5.0 mm), and computes a maximum estimated risk score of 100/100 for reporting and dashboard visualization.



Generated PWD Report
<img width="1060" height="686" alt="Screenshot 2026-02-28 082354" src="https://github.com/user-attachments/assets/ca02d117-4cee-4527-81d1-9ea939c16f16" />=An automated Public Works Department road damage report documenting location (10.850500 N, 76.271100 E), HIGH severity with 19 detected damaged regions, a maximum risk score of 100/100, and recommending immediate inspection and emergency maintenance, with official action fields for follow-up.


Kerala Dashboard Map
<img width="1206" height="858" alt="Screenshot 2026-02-28 080342" src="https://github.com/user-attachments/assets/f6aff2fc-3658-4572-a3cd-d34858d1655c" />
An interactive Kerala Road Damage Dashboard displaying geotagged pothole reports on a map with severity-based markers and controls for managing saved road segments, enabling real-time visualization of affected areas for monitoring and action

<img width="1656" height="697" alt="Screenshot 2026-02-28 080414" src="https://github.com/user-attachments/assets/8f0a0135-96dd-4da3-98bc-ff07ea57b0d6" />
A live camera interface that captures real-time video input to analyze road surfaces for pothole detection and on-the-spot damage assessment.



# # System Architecture
Architecture Overview

User (Upload / Camera)
↓
Image Processing (OpenCV)

Grayscale conversion

Gaussian blur

Canny edge detection

Contour filtering
↓
Severity Classification
↓
GPS Extraction (EXIF Metadata)
↓
Risk Score Calculation
↓
PDF Report Generation (ReportLab)
↓
Dashboard Visualization (Folium Map)

# # Application Workflow

User uploads road image or captures live frame

System verifies road surface

Face detection ensures privacy compliance

Potholes detected using contour area threshold

Severity calculated based on count & total damaged area

GPS coordinates extracted

PDF report generated

Complaint saved to dashboard map

 Dashboard Logic

HIGH severity → Red marker

MEDIUM severity → Orange marker

LOW severity → Green marker

Marker size proportional to risk score

# Project Demo
# # video
Video Link: https://drive.google.com/file/d/1GEOf-7k0CkQK7kxuhwfRkFJGmO9o063-/view?usp=sharing

Demo showcases:

Uploading road image

Live camera detection

Generating official report

Dashboard visualization

# AI Tools Used (Transparency)

Tool Used: ChatGPT

# # Purpose:

Debugging OpenCV logic

Structuring PDF generation

Code refinement

Documentation formatting

Estimated AI-assisted code: ~20%

# # Human Contributions:

System architecture design

Detection threshold tuning

Risk scoring model

UI logic and dashboard integration

Testing and validation

 # Team Contributions

# # Maria Bince

Computer vision implementation

Severity classification logic

PDF automation

Streamlit UI development

Dashboard integration

# # Sadiya Shamsuddin

Testing and debugging

UI refinement

Feature validation

Documentation

#  License

This project is licensed under the MIT License.
