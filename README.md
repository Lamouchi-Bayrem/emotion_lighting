
# 🎭 Facial Emotion-Based Mood Lighting Controller

A real-time **AI-powered web application** that detects **facial emotions via webcam** and dynamically adjusts **ambient lighting (simulated smart lights)** to reflect the user’s emotional state.

This project combines **computer vision**, **deep learning**, and **human-centered smart environments**, making it ideal for **smart homes**, **ambient therapy**, and **AI portfolios**.

---

## 📌 Project Overview

The system captures live video from a webcam, analyzes facial expressions using deep learning models, classifies emotions in real time, and maps those emotions to lighting colors with smooth transitions.

**Example behavior:**
- 😊 Happy → Warm yellow lighting  
- 😢 Sad → Cool blue lighting  
- 😠 Angry → Red lighting  

---

## ✨ Features

- ✅ **Real-Time Emotion Detection**  
  Powered by **DeepFace** deep learning models

- ✅ **7 Supported Emotions**  
  `happy`, `sad`, `angry`, `surprise`, `fear`, `disgust`, `neutral`

- ✅ **Emotion-to-Light Mapping**  
  Each emotion triggers a predefined RGB lighting color

- ✅ **Smooth Color Transitions**  
  Natural lighting changes instead of abrupt switching

- ✅ **Brightness Control**  
  Adjustable brightness via UI slider

- ✅ **Session Logging**  
  Logs emotion changes with timestamps (no images stored)

- ✅ **Privacy-Focused Design**  
  No data upload, no image storage, local processing only

- ✅ **Calibration Mode**  
  Manually test and preview lighting colors

---

## 🎨 Emotion → Color Mapping

| Emotion | Lighting Color | RGB |
|-------|---------------|-----|
| 😊 Happy | Warm Yellow / Orange | (255, 200, 0) |
| 😢 Sad | Cool Blue | (100, 150, 255) |
| 😠 Angry | Red | (255, 50, 50) |
| 😲 Surprise | Bright Yellow | (255, 255, 100) |
| 😨 Fear | Purple | (150, 100, 200) |
| 🤢 Disgust | Green | (100, 200, 100) |
| 😐 Neutral | Soft White | (200, 200, 200) |

---

## 🧠 System Architecture

```

Webcam
↓
OpenCV Frame Capture
↓
DeepFace Emotion Detection
↓
Emotion Aggregation & Smoothing
↓
Lighting Controller (Simulated)
↓
Streamlit UI Visualization

````

---

## 🧩 Requirements

### Software
- Python **3.8+**
- Streamlit
- OpenCV
- DeepFace
- NumPy
- Pillow

### Hardware
- Webcam / Camera device
- Modern web browser (Chrome, Firefox, Edge)

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Lamouchi-Bayrem/emotion_lighting.git
cd emotion_lighting
````

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Note**
> DeepFace downloads pre-trained models automatically on first run
> (~300–500 MB, internet required).

---

### 3️⃣ Run the Application

Using Streamlit:

```bash
streamlit run app.py
```

Or using the launcher:

```bash
python run.py
```

---

### 4️⃣ Open in Browser

```
http://localhost:8501
```

---

## 🚀 Usage Guide

### 📷 Start Camera

* Click **Start Camera**
* Allow camera permissions
* Ensure your face is centered and well-lit

---

### 💡 Lighting Control

* Turn lighting **ON / OFF**
* Adjust **brightness**
* Lighting color updates automatically based on detected emotion

---

### 📊 Emotion Dashboard

* Live emotion label
* Emotion confidence scores
* Average emotion over recent frames
* Current lighting color preview

---

### 🎛 Calibration Mode

* Enable calibration to manually test colors
* Useful for demos or preference tuning

---

## 🔐 Privacy & Security

🔒 **Designed with privacy in mind**

* All processing happens **locally**
* No images or videos are stored
* No facial embeddings are saved
* No cloud APIs involved
* Logs contain only emotion labels and timestamps

---

## 🧯 Troubleshooting

### ❌ DeepFace Model Download Issues

* Ensure stable internet connection
* Restart application after download
* Models are cached for future use

---

### 😐 No Face Detected

* Improve lighting conditions
* Face the camera directly
* Remove masks or obstructions
* Adjust camera angle

---

### 🤔 Emotion Detection Accuracy

* Use frontal face position
* Avoid extreme lighting
* Maintain neutral expression during calibration

---

### 🐢 Performance Issues

* Close other camera applications
* Reduce background processes
* Lower camera resolution if needed

---

## 🌐 Smart Light Integration (Optional)

Currently, lighting is **simulated**.

You can integrate real smart lights by replacing the lighting controller:

* **Philips Hue** → `phue`
* **LIFX** → `lifxlan`
* **Tuya / Generic APIs** → REST
* **IoT / MQTT** → `paho-mqtt`

Example:

```python
# lighting_controller.py
def set_emotion_color(self, color):
    api.set_color(color)
```

---

## 🔮 Future Enhancements

* [ ] Real smart light hardware integration
* [ ] Multi-emotion blending
* [ ] User-defined emotion-color mapping
* [ ] Schedule-based lighting automation
* [ ] Mobile application
* [ ] Multi-user emotion detection
* [ ] Personalized emotion-color learning model

---

## 📂 Project Structure (Example)

```
emotion_lighting/
├── app.py
├── run.py
├── lighting_controller.py
├── emotion_detector.py
├── requirements.txt
├── README.md
└── assets/
```

---

## 📜 License

This project is released **as-is** for:

* Educational use
* Research
* Personal & portfolio projects

---

## 🙏 Acknowledgments

* **DeepFace** – Facial emotion recognition
* **Streamlit** – Web application framework
* **OpenCV** – Computer vision processing
* **NumPy** – Numerical computing




