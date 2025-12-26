import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os
from pathlib import Path
from ui.utils import BackgroundManager
from database import Database

class VocabUI(tb.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Vocabulary Builder")
        self.geometry("900x650")
        
        # Background
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, "images", "image9.jpg")
        self.bg_manager = BackgroundManager(self, img_path)
        self.content_frame = self.bg_manager.get_content_frame()

        tb.Label(self.content_frame, text="Vocabulary Builder", font=("Segoe UI", 18, "bold"), bootstyle="primary").pack(pady=12)

        # Mapping listbox index -> word ID (for deletion)
        self.index_map = [] 

        top = tb.Frame(self.content_frame, padding=12)
        top.pack(fill=X)

        self.word_var = tb.StringVar()
        self.mean_var = tb.StringVar()

        tb.Label(top, text="Word").grid(row=0, column=0, padx=6, pady=6, sticky=W)
        tb.Entry(top, textvariable=self.word_var, width=28).grid(row=0, column=1, padx=6, pady=6)

        tb.Label(top, text="Meaning").grid(row=0, column=2, padx=6, pady=6, sticky=W)
        tb.Entry(top, textvariable=self.mean_var, width=38).grid(row=0, column=3, padx=6, pady=6)

        tb.Button(top, text="➕ Add", bootstyle=SUCCESS, command=self.add_word).grid(row=0, column=4, padx=6, pady=6)

        mid = tb.Frame(self.content_frame, padding=12)
        mid.pack(fill=BOTH, expand=True)

        # Explicitly using tk.Listbox with high contrast colors
        self.listbox = tk.Listbox(mid, height=14, font=("Segoe UI", 11), bg="white", fg="black")
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)

        btns = tb.Frame(mid)
        btns.pack(side=LEFT, fill=Y, padx=10)

        tb.Button(btns, text="🗑 Delete", bootstyle=DANGER, command=self.delete_selected).pack(pady=6, fill=X)
        
        # Load initial data
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, END)
        self.index_map = []
        words = Database.get_words()
        for item in words:
            self.listbox.insert(END, f"{item['word']}  —  {item['meaning']}")
            self.index_map.append(item['id'])

    def add_word(self):
        w = self.word_var.get().strip()
        m = self.mean_var.get().strip()
        if not w or not m:
            tb.Messagebox.showwarning("Missing", "Type word + meaning.")
            return
        
        Database.add_word(w, m)
        
        self.word_var.set("")
        self.mean_var.set("")
        self.refresh()
        tb.Messagebox.showinfo("Saved", "✅ Word saved to Database!")

    def delete_selected(self):
        idx = self.listbox.curselection()
        if not idx:
            return
        
        index = idx[0]
        if index < len(self.index_map):
            word_id = self.index_map[index]
            Database.delete_word(word_id)
            self.refresh()
