import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import os

#  Database Connection and Setup 
def create_tables():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create product table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL,
                        price REAL NOT NULL,
                        category TEXT NOT NULL
                    )''')

    # Create sales table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER,
                        quantity INTEGER,
                        sale_price REAL,
                        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')

    conn.commit()
    conn.close()

# User Authentication
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "admin123":
        messagebox.showinfo("Login Success", "Welcome to the Inventory Management System!")
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_window():
    main_window = tk.Tk()
    main_window.title("Inventory Management System")

    #  Menu Buttons
    button_frame = tk.Frame(main_window)
    button_frame.pack()

    add_product_btn = tk.Button(button_frame, text="Add Product", command=add_product_window)
    update_product_btn = tk.Button(button_frame, text="Update Product", command=update_product_window)
    delete_product_btn = tk.Button(button_frame, text="Delete Product", command=delete_product_window)
    search_product_btn = tk.Button(button_frame, text="Search Products", command=search_product_window)
    record_purchase_btn = tk.Button(button_frame, text="Record Purchase", command=record_purchase_window)
    record_return_btn = tk.Button(button_frame, text="Record Return", command=record_return_window)
    sales_report_btn = tk.Button(button_frame, text="Sales & Reporting", command=sales_reporting_window)
    backup_db_btn = tk.Button(button_frame, text="Backup Database", command=backup_database)
    restore_db_btn = tk.Button(button_frame, text="Restore Database", command=restore_database)
    low_stock_alert_btn = tk.Button(button_frame, text="Low Stock Alerts", command=check_low_stock)
    logout_btn = tk.Button(button_frame, text="Logout", command=lambda: main_window.destroy())

    # Pack buttons into window
    add_product_btn.pack(side=tk.LEFT, padx=5, pady=5)
    update_product_btn.pack(side=tk.LEFT, padx=5, pady=5)
    delete_product_btn.pack(side=tk.LEFT, padx=5, pady=5)
    search_product_btn.pack(side=tk.LEFT, padx=5, pady=5)
    record_purchase_btn.pack(side=tk.LEFT, padx=5, pady=5)
    record_return_btn.pack(side=tk.LEFT, padx=5, pady=5)
    sales_report_btn.pack(side=tk.LEFT, padx=5, pady=5)
    backup_db_btn.pack(side=tk.LEFT, padx=5, pady=5)
    restore_db_btn.pack(side=tk.LEFT, padx=5, pady=5)
    low_stock_alert_btn.pack(side=tk.LEFT, padx=5, pady=5)
    logout_btn.pack(side=tk.LEFT, padx=5, pady=5)

    main_window.mainloop()

#  Product Management 
def add_product_window():
    def add_product():
        name = name_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
        category = category_entry.get()

        if name and quantity and price and category:
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, quantity, price, category) VALUES (?, ?, ?, ?)',
                           (name, quantity, price, category))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Product added successfully")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill all fields")

    add_window = tk.Toplevel()
    add_window.title("Add Product")

    tk.Label(add_window, text="Product Name").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="Quantity").pack()
    quantity_entry = tk.Entry(add_window)
    quantity_entry.pack()

    tk.Label(add_window, text="Price").pack()
    price_entry = tk.Entry(add_window)
    price_entry.pack()

    tk.Label(add_window, text="Category").pack()
    category_entry = tk.Entry(add_window)
    category_entry.pack()

    tk.Button(add_window, text="Add Product", command=add_product).pack()

def update_product_window():
    def update_product():
        product_id = int(product_id_entry.get())
        name = name_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
        category = category_entry.get()

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET name=?, quantity=?, price=?, category=? WHERE id=?',
                       (name, quantity, price, category, product_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product updated successfully")
        update_window.destroy()

    update_window = tk.Toplevel()
    update_window.title("Update Product")

    tk.Label(update_window, text="Product ID").pack()
    product_id_entry = tk.Entry(update_window)
    product_id_entry.pack()

    tk.Label(update_window, text="Product Name").pack()
    name_entry = tk.Entry(update_window)
    name_entry.pack()

    tk.Label(update_window, text="Quantity").pack()
    quantity_entry = tk.Entry(update_window)
    quantity_entry.pack()

    tk.Label(update_window, text="Price").pack()
    price_entry = tk.Entry(update_window)
    price_entry.pack()

    tk.Label(update_window, text="Category").pack()
    category_entry = tk.Entry(update_window)
    category_entry.pack()

    tk.Button(update_window, text="Update Product", command=update_product).pack()

def delete_product_window():
    def delete_product():
        product_id = int(product_id_entry.get())

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id=?', (product_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Product deleted successfully")
        delete_window.destroy()

    delete_window = tk.Toplevel()
    delete_window.title("Delete Product")

    tk.Label(delete_window, text="Product ID").pack()
    product_id_entry = tk.Entry(delete_window)
    product_id_entry.pack()

    tk.Button(delete_window, text="Delete Product", command=delete_product).pack()

# Stock Tracking 
def record_purchase_window():
    def record_purchase():
        product_id = int(product_id_entry.get())
        quantity_purchased = int(quantity_entry.get())

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET quantity = quantity + ? WHERE id=?', 
                       (quantity_purchased, product_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Purchase recorded successfully")
        purchase_window.destroy()

    purchase_window = tk.Toplevel()
    purchase_window.title("Record Purchase")

    tk.Label(purchase_window, text="Product ID").pack()
    product_id_entry = tk.Entry(purchase_window)
    product_id_entry.pack()

    tk.Label(purchase_window, text="Quantity Purchased").pack()
    quantity_entry = tk.Entry(purchase_window)
    quantity_entry.pack()

    tk.Button(purchase_window, text="Record Purchase", command=record_purchase).pack()

def record_return_window():
    def record_return():
        product_id = int(product_id_entry.get())
        quantity_returned = int(quantity_entry.get())

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE products SET quantity = quantity - ? WHERE id=?', 
                       (quantity_returned, product_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Return recorded successfully")
        return_window.destroy()

    return_window = tk.Toplevel()
    return_window.title("Record Return")

    tk.Label(return_window, text="Product ID").pack()
    product_id_entry = tk.Entry(return_window)
    product_id_entry.pack()

    tk.Label(return_window, text="Quantity Returned").pack()
    quantity_entry = tk.Entry(return_window)
    quantity_entry.pack()

    tk.Button(return_window, text="Record Return", command=record_return).pack()

# Search Products 
def search_product_window():
    def search_product():
        search_query = search_entry.get()
        
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name LIKE ? OR category LIKE ?", 
                       ('%' + search_query + '%', '%' + search_query + '%'))
        results = cursor.fetchall()
        conn.close()

        search_results.delete(0, tk.END)
        for result in results:
            search_results.insert(tk.END, result)

    search_window = tk.Toplevel()
    search_window.title("Search Products")

    tk.Label(search_window, text="Search by Name or Category").pack()
    search_entry = tk.Entry(search_window)
    search_entry.pack()

    tk.Button(search_window, text="Search", command=search_product).pack()

    search_results = tk.Listbox(search_window)
    search_results.pack()

# Sales and Reporting 
def sales_reporting_window():
    def record_sale():
        product_id = int(product_id_entry.get())
        quantity_sold = int(quantity_entry.get())
        sale_price = float(price_entry.get())

        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sales (product_id, quantity, sale_price) VALUES (?, ?, ?)',
                       (product_id, quantity_sold, sale_price))
        cursor.execute('UPDATE products SET quantity = quantity - ? WHERE id=?',
                       (quantity_sold, product_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Sale recorded successfully")
        sales_window.destroy()

    sales_window = tk.Toplevel()
    sales_window.title("Record Sale")

    tk.Label(sales_window, text="Product ID").pack()
    product_id_entry = tk.Entry(sales_window)
    product_id_entry.pack()

    tk.Label(sales_window, text="Quantity Sold").pack()
    quantity_entry = tk.Entry(sales_window)
    quantity_entry.pack()

    tk.Label(sales_window, text="Sale Price").pack()
    price_entry = tk.Entry(sales_window)
    price_entry.pack()

    tk.Button(sales_window, text="Record Sale", command=record_sale).pack()

    def generate_report():
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT p.name, SUM(s.quantity) AS total_sold, SUM(s.sale_price) AS total_revenue
                          FROM sales s
                          JOIN products p ON p.id = s.product_id
                          GROUP BY p.name
                          ORDER BY total_sold DESC''')
        report = cursor.fetchall()
        conn.close()

        report_listbox.delete(0, tk.END)
        for row in report:
            report_listbox.insert(tk.END, row)

    report_listbox = tk.Listbox(sales_window)
    report_listbox.pack()

    tk.Button(sales_window, text="Generate Sales Report", command=generate_report).pack()

#  Backup and Restore 
def backup_database():
    backup_file = filedialog.asksaveasfilename(defaultextension=".db", 
                                               filetypes=[("SQLite Database", "*.db")])
    if backup_file:
        conn = sqlite3.connect('inventory.db')
        with open(backup_file, 'wb') as backup:
            for line in conn.iterdump():
                backup.write(('%s\n' % line).encode('utf-8'))
        conn.close()
        messagebox.showinfo("Backup", "Database backup created successfully")

def restore_database():
    restore_file = filedialog.askopenfilename(filetypes=[("SQLite Database", "*.db")])
    if restore_file:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS products')
        cursor.execute('DROP TABLE IF EXISTS sales')
        with open(restore_file, 'rb') as restore:
            for line in restore:
                cursor.executescript(line.decode('utf-8'))
        conn.commit()
        conn.close()
        messagebox.showinfo("Restore", "Database restored successfully")

#  Low Stock Alerts 
def check_low_stock():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < 5")  # Alert when quantity < 5
    low_stock_items = cursor.fetchall()
    conn.close()

    if low_stock_items:
        alert_message = "\n".join([f"Product {item[1]} is low on stock ({item[2]} left)" for item in low_stock_items])
        messagebox.showwarning("Low Stock Alert", alert_message)
    else:
        messagebox.showinfo("Stock Check", "All items are sufficiently stocked")

#  Login Window 
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=login).pack()

create_tables()
login_window.mainloop()
