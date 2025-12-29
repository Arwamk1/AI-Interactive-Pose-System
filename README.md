# AI Pose Interaction Demo (WOW Project) 🌟

An interactive installation system that transforms body movements into visual art using **Computer Vision** and **AI**.
Built with Python, OpenCV, and MediaPipe.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose%20Estimation-orange)

## 🎥 Features

- **Real-time Pose Detection**: Tracks 33 body landmarks with high precision.
- **Interactive Visuals**:
  - **Dynamic Background**: Changes color when you raise your hands (Left = Red, Right = Blue, Both = Green).
  - **Motion Trails**: Neon trails follow your hand movements.
  - **Particle Effects**: Bursts of particles appear when you move quickly.
- **Mirror Effect**: Acts like a smart mirror for intuitive interaction.
- **Performance Optimized**: Runs smoothly on standard CPUs.

## 🚀 Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/yourusername/AI-Interactive-Pose-System.git
    cd AI-Interactive-Pose-System
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 How to Run

Simply run the `run.bat` file or execute the python script:

```bash
python main.py
```

## 🕹️ Controls & Interactions

| Action | Effect |
| :--- | :--- |
| **Raise Left Hand** | Screen tints **RED** 🔴 |
| **Raise Right Hand** | Screen tints **BLUE** 🔵 |
| **Raise Both Hands** | Screen tints **GREEN** (Power Up!) 🟢 |
| **Move Hands** | Neon trails and particles follow your movement ✨ |
| **Press 'q'** | Exit the application |

## 📂 Project Structure

```
├── main.py                 # Entry point of the application
├── requirements.txt        # Python dependencies
├── run.bat                 # One-click launcher for Windows
├── src/
│   ├── pose_detector.py    # MediaPipe Pose estimation wrapper
│   └── visual_effects.py   # Visual effects engine (Trails, Particles)
└── README.md               # Documentation
```

## 🛠️ Customization

- **Adjust Sensitivity**: Modify `detection_con` and `track_con` in `src/pose_detector.py`.
- **Change Colors**: Edit the RGB values in `src/visual_effects.py`.
- **Resolution**: Change `cap.set(3, width)` and `cap.set(4, height)` in `main.py`.

---
*Created for the WOW Project.*
