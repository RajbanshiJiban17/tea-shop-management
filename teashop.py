import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# Database setup
conn = sqlite3.connect("teashop.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    quantity INTEGER,
    price REAL,
    total REAL,
    date TEXT
)
""")
conn.commit()

# Main App
root = tk.Tk()
root.title("Tea Shop Management System")
root.geometry("700x500")
root.config(bg="#f5f5dc")

# --- Functions ---

def calculate_total():
    try:
        qty = int(quantity_entry.get())
        price = float(price_entry.get())
        total = qty * price
        total_var.set(f"{total:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers for quantity and price")

def save_sale():
    item = item_entry.get()
    qty = quantity_entry.get()
    price = price_entry.get()
    total = total_var.get()

    if not item or not qty or not price:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO sales (item_name, quantity, price, total, date) VALUES (?, ?, ?, ?, ?)",
                   (item, qty, price, total, date))
    conn.commit()
    messagebox.showinfo("Success", "Sale recorded successfully!")
    clear_fields()
    show_sales()

def clear_fields():
    item_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    total_var.set("")

def show_sales():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM sales ORDER BY id DESC")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def delete_record():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a record to delete")
        return
    data = tree.item(selected, "values")
    cursor.execute("DELETE FROM sales WHERE id=?", (data[0],))
    conn.commit()
    show_sales()
    messagebox.showinfo("Deleted", "Record deleted successfully!")

# --- UI Layout ---
tk.Label(root, text="Tea Shop Management", bg="#f5f5dc", fg="brown", font=("Arial", 22, "bold")).pack(pady=10)

frame = tk.Frame(root, bg="#f5f5dc")
frame.pack(pady=10)

tk.Label(frame, text="Item Name:", bg="#f5f5dc").grid(row=0, column=0, padx=5, pady=5)
item_entry = tk.Entry(frame)
item_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Quantity:", bg="#f5f5dc").grid(row=1, column=0, padx=5, pady=5)
quantity_entry = tk.Entry(frame)
quantity_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Price per item:", bg="#f5f5dc").grid(row=2, column=0, padx=5, pady=5)
price_entry = tk.Entry(frame)
price_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Total:", bg="#f5f5dc").grid(row=3, column=0, padx=5, pady=5)
total_var = tk.StringVar()
tk.Entry(frame, textvariable=total_var, state="readonly").grid(row=3, column=1, padx=5, pady=5)

tk.Button(frame, text="Calculate", command=calculate_total, bg="lightgreen").grid(row=4, column=0, padx=5, pady=10)
tk.Button(frame, text="Save", command=save_sale, bg="lightblue").grid(row=4, column=1, padx=5, pady=10)
tk.Button(frame, text="Clear", command=clear_fields, bg="lightyellow").grid(row=4, column=2, padx=5, pady=10)

# --- Sales Table ---
columns = ("ID", "Item", "Qty", "Price", "Total", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=10)

tk.Button(root, text="Delete Record", command=delete_record, bg="tomato").pack(pady=5)

show_sales()

root.mainloop()
