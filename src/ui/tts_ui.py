import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from tkinter import messagebox
import os
from ui.utils import BackgroundManager

try:
    import pyttsx3
except Exception:
    pyttsx3 = None


class TextToSpeechUI(tb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Text to Speech")
        self.geometry("800x600")
        # self.resizable(False, False)

        # Background
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, "images", "image4.jpg")
        self.bg_manager = BackgroundManager(self, img_path)
        self.content_frame = self.bg_manager.get_content_frame()

        self.engine = None
        if pyttsx3:
            try:
                self.engine = pyttsx3.init()
            except Exception:
                self.engine = None

        # Header Frame (Title Left, Buttons Right)
        header = tb.Frame(self.content_frame)
        header.pack(fill=X, padx=16, pady=(14, 10))

        title = tb.Label(header, text="Text to Speech", font=("Segoe UI", 18, "bold"), bootstyle="primary")
        title.pack(side=LEFT)

        btn_row = tb.Frame(header)
        btn_row.pack(side=RIGHT)

        speak_btn = tb.Button(btn_row, text="🔊 Speak", bootstyle=SUCCESS, command=self.speak)
        speak_btn.pack(side=LEFT, padx=(0, 10))

        clear_btn = tb.Button(btn_row, text="🧹 Clear", bootstyle=SECONDARY, command=lambda: self.text_area.delete("1.0", END))
        clear_btn.pack(side=LEFT)

        # Text Area
        # self.text_area = ScrolledText(self.content_frame, font=("Segoe UI", 12), padding=15) 
        # Using simple Text if ScrolledText causing issues, but ScrolledText usually fine.
        # Ensure it takes remaining space but doesn't push header out.
        self.text_area = ScrolledText(self.content_frame, font=("Segoe UI", 12), padding=15)
        self.text_area.pack(fill=BOTH, expand=True, padx=16, pady=(0, 16))
        self.text_area.focus()

        note = "Note: If voice doesn't work, install: pip install pyttsx3"
        tb.Label(self.content_frame, text=note, bootstyle="secondary").pack(pady=(12, 0))

    def speak(self):
        txt = self.text_area.get("1.0", END).strip()
        if not txt:
            messagebox.showwarning("Empty", "Please type something first.")
            return

        if not self.engine:
            messagebox.showinfo("TTS not ready", "pyttsx3 not available.\nRun: pip install pyttsx3")
            return

        try:
            self.engine.say(txt)
            self.engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Error", str(e))
