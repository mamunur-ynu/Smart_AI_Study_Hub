import threading
import ttkbootstrap as tb
from ttkbootstrap.constants import *

# ✅ exact class names from your files:
from ui.study_timer_ui import StudyTimerUI
from ui.tts_ui import TextToSpeechUI
from ui.mcq_ui import MCQUI
from ui.vocab_ui import VocabUI


import os
from ui.utils import BackgroundManager
from database import Database

class MainWindow(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Smart AI Study Hub")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # Path to background image
        # Assuming running from src/ or similar, but let's be robust relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, "images", "image8.jpg")

        # Setup Background
        self.bg_manager = BackgroundManager(self, img_path)
        self.main_container = self.bg_manager.get_content_frame()
        
        # Layout inside the glass card (main_container)
        self.main_container.columnconfigure(0, weight=0)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(0, weight=1)

        sidebar = tb.Frame(self.main_container, padding=14)
        sidebar.grid(row=0, column=0, sticky="ns")

        content_area = tb.Frame(self.main_container, padding=18)
        content_area.grid(row=0, column=1, sticky="nsew")

        tb.Label(sidebar, text="Smart AI\nStudy Hub", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 12))
        tb.Label(sidebar, text="Choose a feature", font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 14))

        tb.Button(sidebar, text="⏱ Study Timer", bootstyle=PRIMARY, width=20, command=self.open_timer).pack(fill="x", pady=6)
        tb.Button(sidebar, text="🔊 Text to Speech", bootstyle=INFO, width=20, command=self.open_tts).pack(fill="x", pady=6)
        tb.Button(sidebar, text="📝 MCQ Hub", bootstyle=WARNING, width=20, command=self.open_mcq).pack(fill="x", pady=6)
        tb.Button(sidebar, text="📚 Vocabulary Builder", bootstyle=SUCCESS, width=20, command=self.open_vocab).pack(fill="x", pady=6)

        tb.Separator(sidebar).pack(fill="x", pady=14)
        tb.Button(sidebar, text="❌ Exit", bootstyle=DANGER, width=20, command=self.destroy).pack(fill="x")

        card = tb.Labelframe(content_area, text="Dashboard", padding=18)
        card.pack(fill="both", expand=True)

        # Stats Label
        self.stats_label = tb.Label(card, text="Loading stats...", font=("Segoe UI", 14), justify=LEFT)
        self.stats_label.pack(anchor="nw")

        # Start auto-refresh
        self.update_stats()

    def update_stats(self):
        try:
            stats = Database.get_stats()
            h = stats['total_seconds'] // 3600
            m = (stats['total_seconds'] % 3600) // 60
            
            msg = (
                f"🎓 Total Study Time: {h}h {m}m\n\n"
                f"📚 Vocabulary Words: {stats['vocab_count']}\n\n"
                f"📝 MCQs Created: {stats['mcq_count']}\n"
            )
            self.stats_label.config(text=msg)
        except Exception as e:
            print(f"Stats update error: {e}")

        # Schedule next update in 5 seconds
        self.after(5000, self.update_stats)

    def open_timer(self):
        self.timer_win = StudyTimerUI(self)
        self.timer_win.geometry("1000x700")
        self.timer_win.minsize(900, 600)
        self.timer_win.lift()

    def open_tts(self):
        self.tts_win = TextToSpeechUI(self)
        self.tts_win.geometry("1000x700")
        self.tts_win.minsize(900, 600)
        self.tts_win.lift()

    def open_mcq(self):
        self.mcq_win = MCQUI(self)
        self.mcq_win.geometry("1100x750")
        self.mcq_win.minsize(950, 650)
        self.mcq_win.lift()

    def open_vocab(self):
        self.vocab_win = VocabUI(self)
        self.vocab_win.geometry("1100x750")
        self.vocab_win.minsize(950, 650)
        self.vocab_win.lift()


