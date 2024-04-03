import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from data import DatabaseManager

class StudentsPlacedWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Students Placed")
        self.geometry("1500x500")  # Set a fixed window size
        self.create_widgets()

        # Bind the event handler to window resize event
        self.bind("<Configure>", self.on_window_resize)

    def create_widgets(self):
        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("ID", "Name", "Age", "CGPI", "Skills", "Company", "Edit")
        self.tree.heading("#0", text="Index")
        self.tree.column("#0", minwidth=0, width=50)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("CGPI", text="CGPI")
        self.tree.heading("Skills", text="Skills")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Edit", text="Edit")

        db_manager = DatabaseManager('placed.db')
        self.records = db_manager.fetch_students_placed()

        for i, record in enumerate(self.records, start=1):
            self.tree.insert("", "end", text=str(i), values=(*record, "Edit"), tags=str(i))

        self.tree.tag_configure("oddrow", background="white")
        self.tree.tag_configure("evenrow", background="#f0f0f0")

        self.tree.pack(expand=True, fill="both")

        # Add Exit button
        exit_button = tk.Button(self, text="Exit", command=self.destroy, bg='#FF9999')
        exit_button.pack(side="bottom", padx=10, pady=10)

        # Bind double click on row event to edit
        self.tree.bind("<Double-1>", self.edit_selected)

    def on_window_resize(self, event):
        # Adjust the size of the Treeview widget when the window is resized
        self.tree.pack_configure(expand=True, fill="both")

    def edit_selected(self, event):
        item_id = self.tree.selection()[0]
        if item_id:
            student_details = self.tree.item(item_id, "values")
            edit_window = EditStudentWindow(student_details)

class EditStudentWindow(tk.Toplevel):
    def __init__(self, student_details, master=None):
        super().__init__(master)
        self.title("Edit Student")
        self.student_details = student_details
        self.create_widgets()

    def create_widgets(self):
        labels = ["ID:", "Name:", "Age:", "CGPI:", "Skills:", "Company:"]
        for i, label_text in enumerate(labels):
            tk.Label(self, text=label_text).grid(row=i, column=0, padx=8, pady=5, sticky="w")

        self.entries = []
        for i, value in enumerate(self.student_details):
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entry.insert(tk.END, value)
            self.entries.append(entry)

        # Add Save button
        save_button = tk.Button(self, text="Save", command=self.save_changes, bg='#4CAF50')
        save_button.grid(row=len(labels), columnspan=2, padx=10, pady=10, sticky="ew")

    def save_changes(self):
        updated_values = [entry.get() for entry in self.entries]
        # Update student details in the database
        db_manager = DatabaseManager('placed.db')
        db_manager.update_student(updated_values[0], *updated_values[1:6])
        messagebox.showinfo("Success", "Student details updated successfully!")
        self.destroy()

if __name__ == "__main__":
    window = StudentsPlacedWindow()

