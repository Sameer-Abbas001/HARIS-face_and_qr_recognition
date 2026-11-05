"""
HARIS - High-Accuracy Recognition & Identity System (Web Edition)
Creator & Lead Developer: Sameer Abbas
Faithful Web Port of the Cyberpunk Desktop GUI (app-gui.py)
"""

import os
import io
import time
import cv2
import numpy as np
from PIL import Image
import streamlit as st

# Project Modules
import qr_generator
from create_classifier import train_classifer

# Streamlit Page Config
st.set_page_config(
    page_title="HARIS - AI Biometric & QR Access Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk Theme CSS matching app-gui.py
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1527 0%, #060913 100%);
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, .cyber-title {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1.5px;
    }

    .main-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.7) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 242, 254, 0.12);
        backdrop-filter: blur(8px);
        text-align: center;
    }

    .status-card {
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        margin-bottom: 15px;
        font-weight: 600;
        text-align: center;
        letter-spacing: 1px;
    }

    .status-granted {
        background: rgba(16, 185, 129, 0.15);
        border: 2px solid #10b981;
        color: #34d399;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.3);
    }

    .status-denied {
        background: rgba(239, 68, 68, 0.15);
        border: 2px solid #ef4444;
        color: #f87171;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.3);
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff4500 0%, #ff6347 100%);
        color: #ffffff;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(255, 69, 0, 0.6);
        transform: translateY(-2px);
    }

    .feature-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: border 0.3s;
    }
    .feature-card:hover {
        border-color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)


def load_cascade():
    cascade_path = os.path.join("data", "haarcascade_frontalface_default.xml")
    if not os.path.isfile(cascade_path):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(cascade_path)


def get_registered_users():
    users = []
    names_file = "nameslist.txt"
    if os.path.isfile(names_file):
        with open(names_file, "r") as f:
            for line in f:
                name = line.strip()
                if name and name not in users:
                    users.append(name)
    data_dir = "data"
    if os.path.isdir(data_dir):
        for entry in os.listdir(data_dir):
            full_p = os.path.join(data_dir, entry)
            if os.path.isdir(full_p) and entry not in ["classifiers", "qrcodes", "__pycache__"]:
                if entry not in users:
                    users.append(entry)
    return sorted(users)


def add_user_to_nameslist(name):
    name = name.strip()
    if not name:
        return
    current = get_registered_users()
    if name not in current:
        with open("nameslist.txt", "a") as f:
            f.write(f"\n{name}")


# Sidebar Navigation matching app-gui.py structure
st.sidebar.markdown("""
<div style="text-align: center; padding: 15px 0;">
    <h2 style="color: #38bdf8; margin: 0;">⚡ HARIS</h2>
    <p style="color: #94a3b8; font-size: 13px;">AI Biometric & QR Access Suite</p>
</div>
""", unsafe_allow_html=True)

nav_choice = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Home Dashboard",
        "➕ Sign Up User (50 Frames)",
        "🔍 Check a User (Biometrics)",
        "🪪 QR Identity & Badge Hub",
        "🎯 Access Control HUD"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**System Architecture:**
- Dual Biometric LBPH Recognition
- Level-H Photo-Embedded QR
- Cybernetic Access ID Cards
- Cloud & Edge Ready
""")


# ==============================================================================
# PAGE 1: HOME DASHBOARD (Matching StartPage in app-gui.py)
# ==============================================================================
if nav_choice == "🏠 Home Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1 style="color: #ffffff; margin-bottom: 5px;">HARIS ACCESS INTELLIGENCE</h1>
        <p style="color: #38bdf8; font-size: 15px; margin: 0; letter-spacing: 1px;">
            Real-Time Facial Recognition & Photo-Embedded QR Verification Core
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_hero_1, col_hero_2, col_hero_3 = st.columns([1, 2, 1])
    with col_hero_2:
        if os.path.isfile("homepagepic.png"):
            st.image("homepagepic.png", caption="HARIS Biometric Terminal", use_container_width=True)
        else:
            st.info("HARIS Biometric Terminal Ready")

    st.markdown("### 🚀 Quick Access Modules")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #ff4500;">➕ Sign Up User</h3>
            <p style="font-size: 13px; color: #94a3b8;">Enroll user portraits and generate 50-frame localized biometric dataset.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #0284c7;">🔍 Check User</h3>
            <p style="font-size: 13px; color: #94a3b8;">Train and verify custom LBPH neural classifier models per registered profile.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #7c3aed;">🪪 QR Badge Hub</h3>
            <p style="font-size: 13px; color: #94a3b8;">Generate Level-H Photo-embedded QR tokens and cybernetic access passes.</p>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #10b981;">🎯 Access HUD</h3>
            <p style="font-size: 13px; color: #94a3b8;">Live verification stream running simultaneous face and QR authentication.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    > **Tip on Camera Access**: If your browser asks for camera permissions or restricts video on `http://`, 
    > you can either use the **Image Uploader** directly on each page, or see the camera setup instructions.
    """)


# ==============================================================================
# PAGE 2: SIGN UP USER (Matching PageOne in app-gui.py)
# ==============================================================================
elif nav_choice == "➕ Sign Up User (50 Frames)":
    st.markdown("""
    <div class="main-header">
        <h1 style="color: #ff4500; margin-bottom: 5px;">➕ BIOMETRIC USER ENROLLMENT</h1>
        <p style="color: #94a3b8; margin: 0;">Register new user credentials, capture face dataset (50 frames), and prepare weights.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        new_name = st.text_input("Enter Full Name or User Identifier:", placeholder="e.g. Sameer")
        
        st.markdown("#### Input Source")
        tab_upload, tab_cam = st.tabs(["📁 Upload Photo(s) (Recommended)", "📷 Webcam Snapshot"])
        
        uploaded_portraits = None
        camera_snap = None
        
        with tab_upload:
            uploaded_portraits = st.file_uploader(
                "Upload 1 or more clear face photos:",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True
            )
        with tab_cam:
            camera_snap = st.camera_input("Take a portrait snapshot:")

        if st.button("🚀 Process & Generate 50 Biometric Frames"):
            if not new_name.strip():
                st.error("Please enter a valid user name.")
            else:
                u_name = new_name.strip()
                user_folder = os.path.join("data", u_name)
                os.makedirs(user_folder, exist_ok=True)
                
                face_cascade = load_cascade()
                saved_count = 0

                all_inputs = []
                if uploaded_portraits:
                    all_inputs.extend(uploaded_portraits)
                if camera_snap:
                    all_inputs.append(camera_snap)

                if not all_inputs:
                    st.warning("Please upload a photo or snap a portrait using the webcam.")
                else:
                    progress_bar = st.progress(0)
                    for idx, input_img in enumerate(all_inputs):
                        file_bytes = np.asarray(bytearray(input_img.read()), dtype=np.uint8)
                        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(80, 80))

                        primary_path = os.path.join(user_folder, f"0{u_name}.jpg")
                        if not os.path.isfile(primary_path):
                            cv2.imwrite(primary_path, img)

                        for (x, y, w, h) in faces:
                            face_crop = gray[y:y+h, x:x+w]
                            # Generate augmented 50 frames
                            for aug_i in range(50):
                                aug_face = cv2.convertScaleAbs(face_crop, alpha=1.0 + (aug_i - 25)*0.015, beta=(aug_i - 25))
                                save_p = os.path.join(user_folder, f"{saved_count}{u_name}.jpg")
                                cv2.imwrite(save_p, aug_face)
                                saved_count += 1
                                if saved_count >= 50:
                                    break
                            if saved_count >= 50:
                                break

                        progress_bar.progress(int((idx + 1) / len(all_inputs) * 100))

                    add_user_to_nameslist(u_name)
                    st.success(f"Successfully enrolled **{u_name}** with {saved_count} biometric samples saved in `data/{u_name}/`!")
                    st.info("👉 Next Step: Go to **Check a User (Biometrics)** to train the LBPH classifier.")

    with col2:
        st.subheader("👥 Currently Registered Users")
        current_users = get_registered_users()
        if current_users:
            for u in current_users:
                p_path = qr_generator.get_user_photo_path(u)
                c_a, c_b = st.columns([1, 3])
                with c_a:
                    if p_path and os.path.isfile(p_path):
                        st.image(p_path, width=65)
                    else:
                        st.markdown("👤")
                with c_b:
                    st.markdown(f"**{u}**")
                    clf_path = os.path.join("data", "classifiers", f"{u}_classifier.xml")
                    if os.path.isfile(clf_path):
                        st.caption("✅ Model Trained")
                    else:
                        st.caption("⚠️ Needs Training")
        else:
            st.info("No registered users enrolled yet.")


# ==============================================================================
# PAGE 3: CHECK A USER & TRAIN CLASSIFIER (Matching PageTwo in app-gui.py)
# ==============================================================================
elif nav_choice == "🔍 Check a User (Biometrics)":
    st.markdown("""
    <div class="main-header">
        <h1 style="color: #0284c7; margin-bottom: 5px;">🔍 BIOMETRIC CHECK & MODEL TRAINING</h1>
        <p style="color: #94a3b8; margin: 0;">Train user LBPH models and perform individual biometric verification.</p>
    </div>
    """, unsafe_allow_html=True)

    users = get_registered_users()
    if not users:
        st.warning("No enrolled users found. Please enroll a user first.")
    else:
        selected_user = st.selectbox("Select User Profile:", users)
        
        tab_train, tab_verify = st.tabs(["🧠 1. Train Biometric Classifier", "🎯 2. Verify Facial Biometrics"])

        with tab_train:
            st.write(f"Dataset location: `data/{selected_user}/`")
            col_t1, col_t2 = st.columns([1, 1])
            with col_t1:
                if st.button("⚡ Start LBPH Model Training"):
                    with st.spinner(f"Training LBPH Face Recognizer for {selected_user}..."):
                        try:
                            t0 = time.time()
                            train_classifer(selected_user)
                            dur = time.time() - t0
                            clf_path = os.path.join("data", "classifiers", f"{selected_user}_classifier.xml")
                            st.success(f"Training succeeded in {dur:.2f}s! Saved: `{clf_path}`")
                        except Exception as e:
                            st.error(f"Training error: {e}")
            with col_t2:
                clf_path = os.path.join("data", "classifiers", f"{selected_user}_classifier.xml")
                if os.path.isfile(clf_path):
                    st.success(f"✅ Trained Model Ready ({os.path.getsize(clf_path)/1024:.1f} KB)")
                else:
                    st.warning("⚠️ Model not trained yet.")

        with tab_verify:
            st.write(f"Testing biometric recognition specifically against profile: **{selected_user}**")
            test_img = st.file_uploader("Upload face photo to verify:", type=["jpg", "png", "jpeg"], key="check_upload")
            cam_test = st.camera_input("Or snap portrait with webcam:", key="check_cam")
            
            chosen_input = test_img if test_img else cam_test
            if chosen_input:
                file_bytes = np.asarray(bytearray(chosen_input.read()), dtype=np.uint8)
                frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face_cascade = load_cascade()
                faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(100, 100))

                clf_path = os.path.join("data", "classifiers", f"{selected_user}_classifier.xml")
                if not os.path.isfile(clf_path):
                    st.error(f"Classifier for {selected_user} has not been trained yet. Please train it first.")
                elif len(faces) == 0:
                    st.warning("No face detected in the image.")
                else:
                    clf = cv2.face.LBPHFaceRecognizer_create()
                    clf.read(clf_path)
                    
                    matched = False
                    for (x, y, w, h) in faces:
                        face_roi = gray[y:y+h, x:x+w]
                        id_, loss = clf.predict(face_roi)
                        conf = max(0, min(100, int(100 * (1 - (loss / 300.0)))))
                        
                        color = (16, 185, 129) if conf >= 48 else (239, 68, 68)
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                        cv2.putText(frame, f"{conf}%", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                        
                        if conf >= 48:
                            matched = True
                            st.markdown(f"""
                            <div class="status-card status-granted">
                                <h2>🟢 MATCH CONFIRMED: {selected_user}</h2>
                                <p>Confidence Score: <b>{conf}%</b></p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="status-card status-denied">
                                <h2>🔴 NOT MATCHED</h2>
                                <p>Confidence: {conf}% (Threshold: 48%)</p>
                            </div>
                            """, unsafe_allow_html=True)

                    st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Analysis Result", width=480)


# ==============================================================================
# PAGE 4: QR IDENTITY & BADGE HUB (Matching PageQR / PageFour in app-gui.py)
# ==============================================================================
elif nav_choice == "🪪 QR Identity & Badge Hub":
    st.markdown("""
    <div class="main-header">
        <h1 style="color: #7c3aed; margin-bottom: 5px;">🪪 PHOTO-QR & ACCESS BADGE HUB</h1>
        <p style="color: #94a3b8; margin: 0;">Generate High-Error-Correction QR tokens and cybernetic access passes.</p>
    </div>
    """, unsafe_allow_html=True)

    users = get_registered_users()
    if not users:
        st.warning("No registered users available. Please enroll a user first.")
    else:
        selected_user = st.selectbox("Select User for Badge Generation:", users)
        
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("🎨 Generate Photo-QR & ID Badge"):
                with st.spinner("Rendering High-Error-Correction QR with embedded portrait..."):
                    try:
                        qr_p = qr_generator.generate_photo_qr(selected_user)
                        badge_p = qr_generator.generate_id_badge(selected_user)
                        st.success("Successfully generated QR Code and Cybernetic ID Badge!")
                    except Exception as e:
                        st.error(f"Generation error: {e}")

            qr_path = os.path.join("data", "qrcodes", f"{selected_user}_qr.png")
            if os.path.isfile(qr_path):
                st.subheader("Photo-Embedded QR Code (Level-H)")
                st.image(qr_path, width=280)
                with open(qr_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Photo-QR (PNG)",
                        data=f.read(),
                        file_name=f"{selected_user}_qr.png",
                        mime="image/png"
                    )

        with col2:
            badge_path = os.path.join("data", "qrcodes", f"{selected_user}_badge.png")
            if os.path.isfile(badge_path):
                st.subheader("Cybernetic ID Badge Card")
                st.image(badge_path, width=320)
                with open(badge_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Full ID Badge (PNG)",
                        data=f.read(),
                        file_name=f"{selected_user}_badge.png",
                        mime="image/png"
                    )


# ==============================================================================
# PAGE 5: DUAL ACCESS CONTROL HUD (Matching PageThree in app-gui.py)
# ==============================================================================
elif nav_choice == "🎯 Access Control HUD":
    st.markdown("""
    <div class="main-header">
        <h1 style="color: #10b981; margin-bottom: 5px;">🎯 DUAL ACCESS CONTROL HUD</h1>
        <p style="color: #94a3b8; margin: 0;">Simultaneous Real-Time Facial Recognition & QR Code Token Decoding</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("📷 Verification Input")
        tab_u, tab_c = st.tabs(["📁 Upload Image / Snapshot", "📷 Live Webcam Snapshot"])
        
        up_img = None
        cam_img = None
        with tab_u:
            up_img = st.file_uploader("Upload image containing face and/or QR badge:", type=["jpg", "jpeg", "png"], key="hud_up")
        with tab_c:
            cam_img = st.camera_input("Take photo for verification:", key="hud_cam")

        chosen_feed = up_img if up_img else cam_img

    with col2:
        st.subheader("🛡️ Telemetry & Decision Engine")
        
        if chosen_feed is not None:
            file_bytes = np.asarray(bytearray(chosen_feed.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 1. Detect QR Code
            qr_detector = cv2.QRCodeDetector()
            qr_data, qr_bbox, _ = qr_detector.detectAndDecode(frame)
            parsed_qr_user = None
            if qr_data:
                parsed_qr_user = qr_generator.parse_qr_data(qr_data)

            # 2. Detect Faces
            face_cascade = load_cascade()
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

            best_match_name = None
            best_confidence = 0
            
            classifiers_dir = os.path.join("data", "classifiers")
            available_classifiers = []
            if os.path.isdir(classifiers_dir):
                for f in os.listdir(classifiers_dir):
                    if f.endswith("_classifier.xml"):
                        u_name = f.replace("_classifier.xml", "")
                        available_classifiers.append((u_name, os.path.join(classifiers_dir, f)))

            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 242, 254), 3)

                for u_name, clf_path in available_classifiers:
                    try:
                        clf = cv2.face.LBPHFaceRecognizer_create()
                        clf.read(clf_path)
                        id_, loss = clf.predict(face_roi)
                        conf = max(0, min(100, int(100 * (1 - (loss / 300.0)))))
                        if conf > best_confidence:
                            best_confidence = conf
                            best_match_name = u_name
                    except Exception:
                        pass

            access_granted = False
            verified_name = None
            reasons = []

            if parsed_qr_user:
                reasons.append(f"QR Token Decoded: **{parsed_qr_user}**")
            if best_match_name and best_confidence >= 45:
                reasons.append(f"Face Biometric Match: **{best_match_name}** ({best_confidence}% score)")

            if parsed_qr_user and best_match_name:
                if parsed_qr_user.lower() == best_match_name.lower():
                    access_granted = True
                    verified_name = best_match_name
                else:
                    access_granted = False
                    reasons.append("⚠️ Mismatch between Face Biometrics and QR Token!")
            elif best_match_name and best_confidence >= 55:
                access_granted = True
                verified_name = best_match_name
            elif parsed_qr_user:
                access_granted = True
                verified_name = parsed_qr_user

            if access_granted and verified_name:
                st.markdown(f"""
                <div class="status-card status-granted">
                    <h2 style="margin: 0; color: #34d399;">🟢 ACCESS GRANTED</h2>
                    <h3 style="margin: 5px 0 0 0; color: #ffffff;">{verified_name.upper()}</h3>
                </div>
                """, unsafe_allow_html=True)

                p_path = qr_generator.get_user_photo_path(verified_name)
                if p_path and os.path.isfile(p_path):
                    st.image(p_path, caption=f"Registered Profile: {verified_name}", width=150)
            else:
                st.markdown("""
                <div class="status-card status-denied">
                    <h2 style="margin: 0; color: #f87171;">🔴 ACCESS DENIED</h2>
                    <p style="margin: 5px 0 0 0; color: #cbd5e1;">Face / QR Unrecognized or Confidence Low</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("#### 📊 Diagnostic Stream")
            for r in reasons:
                st.write(f"- {r}")
            if not reasons:
                st.info("No credentials detected in current frame.")

            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Processed Frame HUD", use_container_width=True)
        else:
            st.info("Awaiting input: Upload an image or capture a webcam snapshot to test verification.")
