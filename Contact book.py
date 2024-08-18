import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import time
from PIL import Image, ImageTk

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("400x600")
        self.root.configure(bg="#f7f7f7")

        self.contacts = {}

        # Load phone icon
        self.phone_icon = ImageTk.PhotoImage(Image.open("phone icon.png").resize((20, 20)))

        # Create main layout
        self.create_widgets()

    def create_widgets(self):
        # Clock
        self.clock_label = tk.Label(self.root, font=("Helvetica", 12), bg="#f7f7f7", fg="#333")
        self.clock_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.update_clock()

        # Contact form
        self.name_label = tk.Label(self.root, text="Name:", bg="#f7f7f7", font=("Helvetica", 12))
        self.name_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.name_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        self.phone_label = tk.Label(self.root, text="Phone Number:", bg="#f7f7f7", font=("Helvetica", 12))
        self.phone_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.phone_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.phone_entry.grid(row=2, column=1, padx=10, pady=10)

        self.email_label = tk.Label(self.root, text="Email:", bg="#f7f7f7", font=("Helvetica", 12))
        self.email_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.email_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.email_entry.grid(row=3, column=1, padx=10, pady=10)

        self.address_label = tk.Label(self.root, text="Address:", bg="#f7f7f7", font=("Helvetica", 12))
        self.address_label.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.address_entry = tk.Entry(self.root, font=("Helvetica", 12))
        self.address_entry.grid(row=4, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Contact list
        self.contact_listbox = tk.Listbox(self.root, font=("Helvetica", 12))
        self.contact_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)
        self.contact_listbox.bind('<Double-1>', self.view_contact)

        # Control buttons with phone icon
        self.update_button = tk.Button(self.root, text="Update Contact", command=self.update_contact, font=("Helvetica", 12), bg="#FF9800", fg="white")
        self.update_button.grid(row=7, column=0, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Contact", command=self.delete_contact, font=("Helvetica", 12), bg="#f44336", fg="white")
        self.delete_button.grid(row=7, column=1, pady=10)

        self.search_button = tk.Button(self.root, text="Search Contact", command=self.search_contact, font=("Helvetica", 12), bg="#2196F3", fg="white")
        self.search_button.grid(row=8, column=0, columnspan=2, pady=10)

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=f"Current Time: {now}")
        self.root.after(1000, self.update_clock)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            self.contacts[phone] = {"name": name, "email": email, "address": address}
            self.update_contact_list()
            self.clear_form()
        else:
            messagebox.showwarning("Input Error", "Name and Phone Number are required")

    def update_contact_list(self):
        self.contact_listbox.delete(0, tk.END)
        for phone, details in self.contacts.items():
            self.contact_listbox.insert(tk.END, f"{details['name']} ({phone})")
            self.contact_listbox.itemconfig(tk.END, {'bg':'#e0e0e0', 'font':('Helvetica', 12)})

    def view_contact(self, event):
        selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
        phone = selected_contact.split("(")[-1].strip(")")
        details = self.contacts[phone]

        messagebox.showinfo("Contact Details", f"Name: {details['name']}\nPhone: {phone}\nEmail: {details['email']}\nAddress: {details['address']}")

    def update_contact(self):
        selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
        phone = selected_contact.split("(")[-1].strip(")")

        name = self.contacts[phone]['name']
        email = self.contacts[phone]['email']
        address = self.contacts[phone]['address']

        new_name = simpledialog.askstring("Update Name", "Enter new name:", initialvalue=name)
        new_phone = simpledialog.askstring("Update Phone", "Enter new phone number:", initialvalue=phone)
        new_email = simpledialog.askstring("Update Email", "Enter new email:", initialvalue=email)
        new_address = simpledialog.askstring("Update Address", "Enter new address:", initialvalue=address)

        if new_name and new_phone:
            del self.contacts[phone]
            self.contacts[new_phone] = {"name": new_name, "email": new_email, "address": new_address}
            self.update_contact_list()
        else:
            messagebox.showwarning("Update Error", "Name and Phone Number are required")

    def delete_contact(self):
        selected_contact = self.contact_listbox.get(self.contact_listbox.curselection())
        phone = selected_contact.split("(")[-1].strip(")")

        del self.contacts[phone]
        self.update_contact_list()

    def search_contact(self):
        search_term = simpledialog.askstring("Search Contact", "Enter name or phone number:")
        if search_term:
            for phone, details in self.contacts.items():
                if search_term.lower() in details['name'].lower() or search_term == phone:
                    messagebox.showinfo("Contact Found", f"Name: {details['name']}\nPhone: {phone}\nEmail: {details['email']}\nAddress: {details['address']}")
                    return
            messagebox.showinfo("Contact Not Found", "No contact found with the given name or phone number")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
