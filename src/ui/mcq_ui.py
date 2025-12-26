import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import os
from ui.utils import BackgroundManager
from database import Database

class MCQUI(tb.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("MCQ Generator & Quiz")
        self.geometry("800x600")
        
        # Background
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.join(base_dir, "images", "image2.jpg")
        self.bg_manager = BackgroundManager(self, img_path)
        self.content_frame = self.bg_manager.get_content_frame()
        
        # Title
        tb.Label(self.content_frame, text="MCQ Hub", font=("Segoe UI", 20, "bold"), bootstyle="primary").pack(pady=(10, 10))

        # Tabs
        self.notebook = tb.Notebook(self.content_frame, bootstyle="light")
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Generator
        self.tab_gen = tb.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_gen, text="Generator")
        self.setup_generator_tab()

        # Tab 2: Quiz
        self.tab_quiz = tb.Frame(self.notebook, padding=10) 
        self.notebook.add(self.tab_quiz, text="Take Quiz")
        self.setup_quiz_tab()

    def setup_generator_tab(self):
        form = tb.Frame(self.tab_gen)
        form.pack(fill=X)

        tb.Label(form, text="Question").grid(row=0, column=0, sticky=W, pady=6)
        self.q_var = tb.StringVar()
        tb.Entry(form, textvariable=self.q_var, width=50).grid(row=0, column=1, sticky=W, pady=6)

        self.opt_vars = [tb.StringVar() for _ in range(4)]
        for i in range(4):
            tb.Label(form, text=f"Option {i+1}").grid(row=i+1, column=0, sticky=W, pady=6)
            tb.Entry(form, textvariable=self.opt_vars[i], width=50).grid(row=i+1, column=1, sticky=W, pady=6)

        tb.Label(form, text="Correct (1-4)").grid(row=5, column=0, sticky=W, pady=6)
        self.correct_var = tb.StringVar(value="1")
        tb.Spinbox(form, from_=1, to=4, textvariable=self.correct_var, width=5).grid(row=5, column=1, sticky=W, pady=6)

        btns = tb.Frame(self.tab_gen)
        btns.pack(fill=X, pady=10)

        tb.Button(btns, text="💾 Save to DB", bootstyle=SUCCESS, command=self.save_mcq).pack(side=LEFT)
        tb.Button(btns, text="🧹 Clear", bootstyle=SECONDARY, command=self.clear_gen).pack(side=LEFT, padx=8)

    def save_mcq(self):
        q = self.q_var.get().strip()
        opts = [v.get().strip() for v in self.opt_vars]
        c = self.correct_var.get().strip()

        if not q or any(not o for o in opts):
            messagebox.showwarning("Missing", "Please fill question and all options.")
            return

        Database.add_mcq(q, opts, int(c))
        messagebox.showinfo("Success", "✅ MCQ Saved to Database!")
        self.clear_gen()

    def clear_gen(self):
        self.q_var.set("")
        for v in self.opt_vars: v.set("")
        self.correct_var.set("1")

    def setup_quiz_tab(self):
        # Current Question State
        self.current_mcq = None
        self.selected_opt = tb.IntVar(value=0)

        top = tb.Frame(self.tab_quiz)
        top.pack(fill=X, pady=10)
        tb.Button(top, text="🎲 Load Random Question", bootstyle=INFO, command=self.load_random_question).pack(anchor="center")

        self.q_label = tb.Label(self.tab_quiz, text="Press 'Load' to start...", font=("Segoe UI", 12, "italic"), wraplength=500)
        self.q_label.pack(pady=15)

        self.opts_frame = tb.Frame(self.tab_quiz)
        self.opts_frame.pack(fill=X, padx=20)
        
        self.radios = []
        for i in range(4):
            r = tb.Radiobutton(self.opts_frame, text=f"Option {i+1}", variable=self.selected_opt, value=i+1, bootstyle="info")
            r.pack(anchor="w", pady=4)
            self.radios.append(r)

        tb.Button(self.tab_quiz, text="✅ Submit Answer", bootstyle=PRIMARY, command=self.check_answer).pack(pady=20)

    def load_random_question(self):
        self.current_mcq = Database.get_random_mcq()
        if not self.current_mcq:
            messagebox.showinfo("Empty", "No MCQs in database yet. Go to 'Generator' tab to add some!")
            return
        
        self.q_label.config(text=f"Q: {self.current_mcq['question']}", font=("Segoe UI", 12, "bold"))
        self.selected_opt.set(0) # reset selection
        
        opts = self.current_mcq['options']
        for i, rad in enumerate(self.radios):
            rad.config(text=f"{i+1}. {opts[i]}")

    def check_answer(self):
        if not self.current_mcq:
            return
        
        user_ans = self.selected_opt.get()
        if user_ans == 0:
            messagebox.showwarning("Select", "Please select an option.")
            return

        correct = self.current_mcq['correct_index']
        if user_ans == correct:
            messagebox.showinfo("Correct!", "🎉 That is the correct answer!")
        else:
            messagebox.showerror("Wrong", f"❌ Wrong! Correct answer was option {correct}.")
