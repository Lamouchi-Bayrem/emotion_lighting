

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import pandas as pd

from src.emotion_detector import EmotionDetector
from src.lighting_controller import LightingController


# Page configuration
st.set_page_config(
    page_title="Emotion-Based Mood Lighting",
    page_icon="💡",
    layout="wide"
)

# Initialize session state
if 'emotion_detector' not in st.session_state:
    st.session_state.emotion_detector = EmotionDetector()
if 'lighting_controller' not in st.session_state:
    st.session_state.lighting_controller = LightingController()
if 'camera_active' not in st.session_state:
    st.session_state.camera_active = False
if 'calibration_mode' not in st.session_state:
    st.session_state.calibration_mode = False


def rgb_to_hex(rgb):
    """Convert RGB to hex color"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def create_color_overlay(width, height, color, alpha=0.3):
    """Create color overlay for lighting simulation"""
    overlay = np.zeros((height, width, 3), dtype=np.uint8)
    overlay[:, :] = color
    return overlay


def main():
    """Main application"""
    st.title("💡 Facial Emotion-Based Mood Lighting Controller")
    st.markdown("Analyze facial emotions and adjust smart lights for ambient therapy or smart homes")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Lighting controls
        st.subheader("💡 Lighting Controls")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔛 Turn On"):
                st.session_state.lighting_controller.turn_on()
        with col2:
            if st.button("🔴 Turn Off"):
                st.session_state.lighting_controller.turn_off()
        
        # Brightness control
        brightness = st.slider("Brightness", 0.0, 1.0, 0.7, 0.1)
        st.session_state.lighting_controller.set_brightness(brightness)
        
        # Emotion info
        st.subheader("😊 Emotion Guide")
        st.markdown("""
        - 😊 **Happy**: Warm yellow/orange
        - 😢 **Sad**: Cool blue
        - 😠 **Angry**: Red
        - 😲 **Surprise**: Bright yellow
        - 😨 **Fear**: Purple
        - 🤢 **Disgust**: Green
        - 😐 **Neutral**: White
        """)
        
        # Calibration mode
        st.subheader("🔧 Calibration")
        calibration_mode = st.checkbox("Calibration Mode", value=st.session_state.calibration_mode)
        st.session_state.calibration_mode = calibration_mode
        
        if calibration_mode:
            st.info("Calibration mode: Adjust lighting manually to test colors")
        
        # Session log
        st.subheader("📊 Session Log")
        if st.button("Clear Log"):
            st.session_state.lighting_controller.clear_log()
        
        log = st.session_state.lighting_controller.get_session_log()
        if log:
            log_df = pd.DataFrame(log[-10:])  # Show last 10 entries
            st.dataframe(log_df, use_container_width=True, hide_index=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📹 Camera Feed")
        
        # Camera toggle
        if st.button("🎥 Start Camera" if not st.session_state.camera_active else "🛑 Stop Camera"):
            st.session_state.camera_active = not st.session_state.camera_active
        
        if st.session_state.camera_active:
            camera_input = st.camera_input("Show your face to the camera")
            
            if camera_input:
                # Convert to OpenCV format
                img = Image.open(camera_input)
                frame = np.array(img)
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Detect emotion
                result = st.session_state.emotion_detector.detect_emotion(frame_bgr)
                
                if result['face_detected']:
                    # Update lighting based on emotion
                    if not st.session_state.calibration_mode:
                        st.session_state.lighting_controller.set_emotion_color(result['color'])
                    
                    # Update lighting state
                    st.session_state.lighting_controller.update()
                    
                    # Get current lighting color
                    light_color = st.session_state.lighting_controller.get_current_color()
                    
                    # Create overlay
                    height, width = frame.shape[:2]
                    overlay = create_color_overlay(width, height, light_color, alpha=0.4)
                    
                    # Blend with original frame
                    blended = cv2.addWeighted(frame, 0.6, overlay, 0.4, 0)
                    
                    # Display
                    st.image(blended, use_container_width=True)
                    
                    # Log emotion change
                    if result['emotion'] != st.session_state.emotion_detector.last_emotion:
                        st.session_state.lighting_controller.log_event(
                            "emotion_change",
                            result['emotion'],
                            result['color']
                        )
                else:
                    # No face detected
                    st.image(frame, use_container_width=True)
                    st.warning("No face detected. Please position your face in front of the camera.")
        else:
            st.info("Click 'Start Camera' to begin emotion detection")
    
    with col2:
        st.subheader("📊 Emotion Analysis")
        
        # Current emotion
        if st.session_state.emotion_detector.last_emotion:
            emotion = st.session_state.emotion_detector.last_emotion
            color = st.session_state.emotion_detector.get_color_for_emotion(emotion)
            
            st.metric("Current Emotion", emotion.upper())
            
            # Color display
            st.markdown("**Lighting Color:**")
            hex_color = rgb_to_hex(color)
            st.markdown(f'<div style="background-color: {hex_color}; padding: 20px; border-radius: 10px; text-align: center; color: {"black" if sum(color) > 400 else "white"}">{hex_color}</div>', 
                       unsafe_allow_html=True)
        else:
            st.info("No emotion detected yet")
        
        # Emotion scores
        if st.session_state.emotion_detector.emotion_history:
            latest = st.session_state.emotion_detector.emotion_history[-1]
            scores = latest.get('scores', {})
            
            if scores:
                st.markdown("**Emotion Probabilities:**")
                scores_df = pd.DataFrame([
                    {'Emotion': k, 'Probability': f"{v:.1f}%"}
                    for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True)
                ])
                st.dataframe(scores_df, use_container_width=True, hide_index=True)
        
        # Average emotion
        st.markdown("**Average Emotion (Last 10):**")
        avg_emotion = st.session_state.emotion_detector.get_average_emotion(10)
        if avg_emotion:
            st.metric("Dominant", avg_emotion['emotion'].upper())
            avg_color = avg_emotion['color']
            hex_color = rgb_to_hex(avg_color)
            st.markdown(f'<div style="background-color: {hex_color}; padding: 10px; border-radius: 5px;"></div>', 
                       unsafe_allow_html=True)
        
        # Lighting status
        st.subheader("💡 Lighting Status")
        controller = st.session_state.lighting_controller
        status = "ON" if controller.is_on else "OFF"
        st.metric("Status", status)
        
        current_light_color = controller.get_current_color()
        if controller.is_on:
            hex_color = rgb_to_hex(current_light_color)
            st.markdown(f'<div style="background-color: {hex_color}; padding: 20px; border-radius: 10px; text-align: center; color: {"black" if sum(current_light_color) > 400 else "white"}">Current Light Color</div>', 
                       unsafe_allow_html=True)
        
        st.metric("Brightness", f"{int(controller.brightness * 100)}%")
    
    # Privacy notice
    st.markdown("---")
    st.info("🔒 **Privacy**: Images are processed in real-time and not stored. No facial data is saved or transmitted.")


if __name__ == "__main__":
    main()





