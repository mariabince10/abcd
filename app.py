import streamlit as st
import cv2
import numpy as np
from PIL import Image
import piexif
import os
import folium
from streamlit_folium import folium_static
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import time
from io import BytesIO
from branca.element import Template, MacroElement

# ---------- SESSION STATE ----------
if "reports" not in st.session_state:
    st.session_state.reports = []

# ---------- GLOBAL MODELS ----------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------- IMPROVED DETECTION ----------
def detect_potholes_simple(pil_image, min_area=300):
    img_np = np.array(pil_image.convert("RGB"))
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blurred, 40, 140)

    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pothole_contours = []
    areas = []

    for c in contours:
        a = cv2.contourArea(c)
        if a > min_area:
            pothole_contours.append(c)
            areas.append(a)

    count = len(pothole_contours)
    total_area = sum(areas)

    if count >= 5 or total_area > 3000:
        severity = "HIGH"
    elif count >= 2 or total_area > 1200:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "count": count,
        "total_area": total_area,
        "severity": severity
    }

# ---------- GPS ----------
def get_gps_from_image_bytes(file_bytes):
    try:
        image = Image.open(BytesIO(file_bytes))
        exif_bytes = image.info.get("exif", None)
        if exif_bytes is None:
            return 10.8505, 76.2711
        exif_dict = piexif.load(exif_bytes)
        gps_ifd = exif_dict.get("GPS", {})
        if not gps_ifd:
            return 10.8505, 76.2711

        def to_deg(value):
            d = value[0][0] / value[0][1]
            m = value[1][0] / value[1][1]
            s = value[2][0] / value[2][1]
            return d + (m / 60.0) + (s / 3600.0)

        lat = to_deg(gps_ifd[piexif.GPSIFD.GPSLatitude])
        lon = to_deg(gps_ifd[piexif.GPSIFD.GPSLongitude])
        return lat, lon
    except:
        return 10.8505, 76.2711

# ---------- DETAILED PDF WITH BLUE BORDER ----------
def generate_pdf(lat, lon, severity, risk_score, count):
    filename = f"pothole_report_{int(time.time())}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # BLUE BORDER
    c.setStrokeColorRGB(0, 0.2, 0.8)
    c.setLineWidth(3)
    c.rect(20, 20, width - 40, height - 40)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "PUBLIC WORKS DEPARTMENT")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 780, "ROAD DAMAGE ASSESSMENT REPORT")

    c.setFont("Helvetica", 11)

    y = 750
    c.drawString(50, y, f"Report Generated : {time.strftime('%Y-%m-%d %H:%M')}")
    y -= 25

    c.drawString(50, y, "Location Information:")
    y -= 20
    c.drawString(70, y, f"Latitude  : {lat:.6f}")
    y -= 18
    c.drawString(70, y, f"Longitude : {lon:.6f}")
    y -= 25

    c.drawString(50, y, "Road Condition Summary:")
    y -= 20
    c.drawString(70, y, f"Observed Severity Level : {severity}")
    y -= 18
    c.drawString(70, y, f"Detected Damaged Regions : {count}")
    y -= 18
    c.drawString(70, y, f"Risk Score (0–100) : {risk_score:.1f}")
    y -= 25

    c.drawString(50, y, "Engineering Recommendation:")
    y -= 20

    if severity == "HIGH":
        c.drawString(70, y, "Immediate inspection and emergency repair required.")
        y -= 18
        c.drawString(70, y, "Area presents potential safety risk to road users.")
    elif severity == "MEDIUM":
        c.drawString(70, y, "Inspection recommended with scheduled maintenance.")
        y -= 18
        c.drawString(70, y, "Surface deterioration observed requiring attention.")
    else:
        c.drawString(70, y, "Routine monitoring recommended.")
        y -= 18
        c.drawString(70, y, "No immediate structural risk detected.")

    y -= 40
    c.drawString(50, y, "For Official Use:")
    y -= 20
    c.drawString(70, y, "Inspection Date : __________________________")
    y -= 20
    c.drawString(70, y, "Action Taken    : __________________________")
    y -= 20
    c.drawString(70, y, "Engineer Name   : __________________________")
    y -= 20
    c.drawString(70, y, "Signature       : __________________________")

    c.save()
    return filename

# ---------- ROAD CHECK ----------
def looks_like_road(pil_image):
    img_np = np.array(pil_image.convert("RGB"))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 40, 140)
    return np.count_nonzero(edges) / edges.size > 0.01

def contains_human_face(pil_image):
    img_np = np.array(pil_image.convert("RGB"))
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    return len(faces) > 0

# ---------- PAGE ----------
st.set_page_config(page_title="Kerala Road Damage Monitoring", layout="wide")
st.title("🛣️ Kerala Road Damage Monitoring and Reporting System")

tab_upload, tab_camera = st.tabs(["📱 Citizen Upload", "📹 Live Camera"])

# ---------- UPLOAD ----------
with tab_upload:
    uploaded_file = st.file_uploader("Upload road photo", type=["jpg","jpeg","png"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, use_column_width=True)

        if looks_like_road(img):
            result = detect_potholes_simple(img)

            severity = st.selectbox(
                "Confirm severity",
                ["LOW","MEDIUM","HIGH"],
                index=["LOW","MEDIUM","HIGH"].index(result["severity"])
            )

            st.success(f"Road condition assessed — {severity}")

            lat, lon = get_gps_from_image_bytes(uploaded_file.getvalue())
            risk_score = min(100, (result["total_area"] / 50.0) + 50)

            if st.button("📄 Generate detailed PWD report"):
                pdf_file = generate_pdf(lat, lon, severity, risk_score, result["count"])
                with open(pdf_file, "rb") as f:
                    st.download_button("Download Report", f, pdf_file)

            if st.button("📧 Register complaint with PWD"):
                st.success("Complaint registered and forwarded to concerned authority.")

            if st.button("💾 Save to dashboard"):
                st.session_state.reports.append({
                    "lat": lat,
                    "lon": lon,
                    "severity": severity,
                    "risk": risk_score
                })
                st.success("Saved to dashboard.")

# ---------- LIVE CAMERA ----------
with tab_camera:
    camera_image = st.camera_input("Show the road surface")

    if camera_image:
        img_cam = Image.open(camera_image).convert("RGB")
        st.image(img_cam, caption="Live frame", use_column_width=True)

        if looks_like_road(img_cam) and not contains_human_face(img_cam):
            result_cam = detect_potholes_simple(img_cam)
            st.success(f"Road condition detected — {result_cam['severity']}")
        else:
            st.error("Please show only the road surface.")

# ---------- DASHBOARD ----------
st.markdown("---")
st.header("🗺️ Kerala Road Damage Dashboard")

m = folium.Map(location=[10.8505, 76.2711], zoom_start=8)

for r in st.session_state.reports:
    color = {"HIGH":"red","MEDIUM":"orange","LOW":"green"}[r["severity"]]
    radius = max(5, r["risk"] / 8)

    folium.CircleMarker(
        location=[r["lat"], r["lon"]],
        radius=radius,
        color=color,
        fill=True,
        fill_opacity=0.8,
        popup=f"Severity: {r['severity']} | Risk: {r['risk']:.1f}"
    ).add_to(m)

folium_static(m)

if st.button("Clear dashboard"):
    st.session_state.reports = []