import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database_ref as db
import os

# Matplotlib for charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class GradeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grade Tracker")
        self.root.geometry("900x600")

        # Notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Buttons under notebook
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        add_subject_btn = tk.Button(button_frame, text="Add New Subject", command=self.add_subject)
        add_subject_btn.pack(side="left", padx=5)

        clear_btn = tk.Button(button_frame, text="Clear All Data", command=self.clear_all_data)
        clear_btn.pack(side="left", padx=5)

        # Load existing subjects
        self.load_subject_tabs()

    def load_subject_tabs(self):
        """Load all subjects and create a tab for each."""
        subjects = db.load_subjects()
        for subject in subjects:
            self.create_subject_tab(subject)

    def create_subject_tab(self, subject):
        """Create a tab for a specific subject."""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=subject)

        # Layout: left (form + text), right (chart)
        left_frame = tk.Frame(frame)
        left_frame.pack(side="left", fill="y", padx=10)

        right_frame = tk.Frame(frame)
        right_frame.pack(side="right", fill="both", expand=True)

        # Entry fields
        tk.Label(left_frame, text="Assignment / Test:").pack()
        assignment_entry = tk.Entry(left_frame, width=30)
        assignment_entry.pack()

        tk.Label(left_frame, text="Grade / Score:").pack()
        grade_entry = tk.Entry(left_frame, width=30)
        grade_entry.pack()

        # Text display
        text_box = tk.Text(left_frame, height=15, width=40)
        text_box.pack(pady=5)

        def add_grade():
            assignment = assignment_entry.get().strip()
            try:
                grade = float(grade_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Please enter a number for grade.")
                return

            if assignment == "":
                messagebox.showerror("Error", "Please enter an assignment.")
                return

            db.add_grade(subject, assignment, grade)
            assignment_entry.delete(0, tk.END)
            grade_entry.delete(0, tk.END)
            update_display()

        def update_display():
            # Update text
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, db.get_stats(subject))

            # Update chart
            for widget in right_frame.winfo_children():
                widget.destroy()

            grades = db.load_grades(subject)
            if grades:
                assignments = list(grades.keys())
                marks = list(grades.values())

                fig, ax = plt.subplots(figsize=(4, 3))
                ax.plot(assignments, marks, marker="o", linestyle="-", color="blue")
                ax.set_title(f"{subject} Grades")
                ax.set_xlabel("Assignments")
                ax.set_ylabel("Grade")
                ax.grid(True)

                canvas = FigureCanvasTkAgg(fig, master=right_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
                plt.close(fig)  # prevent duplicate figures

        # Buttons
        tk.Button(left_frame, text="Add Grade", command=add_grade).pack(pady=5)

        update_display()

    def add_subject(self):
        """Ask user for a subject name and create a new tab."""
        subject = simpledialog.askstring("New Subject", "Enter subject name:")
        if subject:
            db.add_subject(subject)
            self.create_subject_tab(subject)

    def clear_all_data(self):
        """Clear all JSON files and reset notebook."""
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to clear all data? This cannot be undone.")
        if confirm:
            db.clear_all()
            for tab in self.notebook.tabs():
                self.notebook.forget(tab)
            messagebox.showinfo("Cleared", "All data has been cleared.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GradeTrackerApp(root)
    root.mainloop()
