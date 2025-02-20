import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QTextEdit, QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from scramble_generator import ScrambleGenerator

class RubiksCubeAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rubik's Cube Solver Analyzer")
        self.setGeometry(100, 100, 1000, 800)

        # Initialize scramble generator
        self.scramble_generator = ScrambleGenerator()

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Scramble display
        scramble_layout = QHBoxLayout()
        self.scramble_text = QTextEdit()
        self.scramble_text.setReadOnly(True)
        self.scramble_text.setMaximumHeight(60)
        scramble_layout.addWidget(self.scramble_text)
        
        self.generate_scramble_button = QPushButton("Generate New Scramble")
        self.generate_scramble_button.clicked.connect(self.generate_new_scramble)
        scramble_layout.addWidget(self.generate_scramble_button)
        
        layout.addLayout(scramble_layout)

        # Scramble explanation
        self.scramble_explanation = QTextEdit()
        self.scramble_explanation.setReadOnly(True)
        self.scramble_explanation.setMaximumHeight(100)
        layout.addWidget(self.scramble_explanation)

        # Video display
        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        layout.addWidget(self.video_label)

        # Controls
        controls_layout = QHBoxLayout()
        
        self.camera_button = QPushButton("Start Camera")
        self.camera_button.clicked.connect(self.toggle_camera)
        controls_layout.addWidget(self.camera_button)

        self.record_button = QPushButton("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        self.record_button.setEnabled(False)  # Disabled until camera starts
        controls_layout.addWidget(self.record_button)
        
        layout.addLayout(controls_layout)

        # Analysis output
        self.analysis_text = QTextEdit()
        self.analysis_text.setReadOnly(True)
        self.analysis_text.setMaximumHeight(100)
        layout.addWidget(self.analysis_text)

        # Initialize camera-related variables
        self.camera = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.is_camera_running = False
        self.is_recording = False
        self.recorded_frames = []

        # Generate initial scramble
        self.generate_new_scramble()

    def toggle_camera(self):
        if not self.is_camera_running:
            # Try to start the camera
            self.camera = cv2.VideoCapture(0)
            if self.camera.isOpened():
                ret, frame = self.camera.read()
                if ret:
                    self.is_camera_running = True
                    self.timer.start(30)  # 30ms = ~33fps
                    self.camera_button.setText("Stop Camera")
                    self.record_button.setEnabled(True)
                    return
                else:
                    self.camera.release()
            
            # If we get here, camera failed to start
            QMessageBox.warning(self, "Camera Error", 
                              "Could not start the camera. Please check if:\n"
                              "1. Your camera is properly connected\n"
                              "2. No other application is using the camera\n"
                              "3. You have given camera permissions to this application")
        else:
            # Stop the camera
            self.stop_camera()

    def stop_camera(self):
        if self.camera is not None:
            self.timer.stop()
            self.camera.release()
            self.camera = None
        self.is_camera_running = False
        self.camera_button.setText("Start Camera")
        self.record_button.setEnabled(False)
        self.video_label.clear()
        if self.is_recording:
            self.toggle_recording()

    def generate_new_scramble(self):
        scramble, explanations = self.scramble_generator.get_scramble_with_explanation()
        self.scramble_text.setText(f"Scramble: {scramble}")
        self.scramble_explanation.setText("Move explanations:\n" + "\n".join(
            f"{i+1}. {exp}" for i, exp in enumerate(explanations)
        ))

    def toggle_recording(self):
        if not self.is_camera_running:
            return
            
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.record_button.setText("Stop Recording")
            self.recorded_frames = []
        else:
            self.record_button.setText("Start Recording")
            self.analyze_solve()

    def update_frame(self):
        if self.camera is None or not self.camera.isOpened():
            self.stop_camera()
            return

        ret, frame = self.camera.read()
        if ret:
            if self.is_recording:
                self.recorded_frames.append(frame.copy())
            
            # Convert frame to Qt format for display
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.stop_camera()

    def analyze_solve(self):
        if len(self.recorded_frames) == 0:
            self.analysis_text.setText("No solve recorded!")
            return

        # Basic analysis (to be expanded)
        solve_time = len(self.recorded_frames) / 33  # Approximate seconds
        self.analysis_text.setText(
            f"Solve Time: {solve_time:.2f} seconds\n"
            f"Suggestions:\n"
            f"- Practice F2L lookahead to reduce pauses\n"
            f"- Consider learning advanced PLL algorithms\n"
            f"- Work on finger tricks for faster execution"
        )

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RubiksCubeAnalyzer()
    window.show()
    sys.exit(app.exec())
