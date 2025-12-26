from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import time
import threading
import os
from ui.utils import BackgroundManager
from database import Database

class StudyTimerUI(tb.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Study Timer")
        self.geometry("800x600")

        # Background
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, "images", "image6.jpg")
        self.bg_manager = BackgroundManager(self, img_path, resize_content=False)
        self.content_frame = self.bg_manager.get_content_frame()

        # Example timer label and start button setup:
        self.timer_label = tb.Label(self.content_frame, text="Time: 00:00", font=("Segoe UI", 48, "bold"), bootstyle="primary")
        self.timer_label.pack(pady=40)

        btn_frame = tb.Frame(self.content_frame)
        btn_frame.pack(pady=20)

        start_btn = tb.Button(btn_frame, text="▶ Start", bootstyle="success", command=self.start_timer)
        start_btn.pack(side=LEFT, padx=10)

        stop_btn = tb.Button(btn_frame, text="⏹ Stop & Save", bootstyle="danger", command=self.stop_timer)
        stop_btn.pack(side=LEFT, padx=10)

        # Initialize timer duration (in seconds, e.g., 25 minutes = 1500 seconds)
        self.initial_duration = 1500
        self.time_left = self.initial_duration
        self.running = False
        print("StudyTimerUI initialized successfully")

    def start_timer(self):
        """Start the countdown in a separate thread to avoid freezing the UI."""
        if self.running:
            return  # Already running

        self.time_left = self.initial_duration # Reset for demo or start from current
        self.running = True

        # Create and start a background thread for the countdown
        self._timer_thread = threading.Thread(target=self._run_timer)
        self._timer_thread.daemon = True  # Daemon thread will exit when app closes
        self._timer_thread.start()

    def stop_timer(self):
        if not self.running:
            return

        self.running = False
        # Calculate elapsed time
        elapsed = self.initial_duration - self.time_left
        if elapsed > 0:
            Database.log_study_session(elapsed)
            messagebox.showinfo("Saved", f"✅ Session saved: {elapsed} seconds")
        self.timer_label.config(text="Stopped")

    def _run_timer(self):
        """Background thread method for counting down the time."""
        while self.time_left > 0 and self.running:
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            time_text = f"{minutes:02d}:{seconds:02d}"
            # Update the label on the main thread using .after
            self.timer_label.after(0, lambda txt=time_text: self.timer_label.config(text=txt))
            time.sleep(1)            # Wait for 1 second (background thread)
            self.time_left -= 1

        if self.running and self.time_left <= 0:
            # Countdown is finished; update the label one last time on the main thread
            self.timer_label.after(0, lambda: self.timer_label.config(text="Time's up!"))
            # Log to Database
            self.running = False
            Database.log_study_session(self.initial_duration)
            print(f"Logged study session: {self.initial_duration} seconds")
