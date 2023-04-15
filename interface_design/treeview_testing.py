from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser
from pathlib import Path
root = Tk()
root.title('Treeview Testing')
root.geometry("1000x550")


# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3")

# Create a Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("first", "last", "ID", "address", "city", "state", "zip")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("first", anchor=W, width=140)
my_tree.column("last", anchor=W, width=140)
my_tree.column("ID", anchor=CENTER, width=100)
my_tree.column("address", anchor=CENTER, width=140)
my_tree.column("city", anchor=CENTER, width=140)
my_tree.column("state", anchor=CENTER, width=140)
my_tree.column("zip", anchor=CENTER, width=140)


# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("first", text="First Name", anchor=W)
my_tree.heading("last", text="Last Name", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("address", text="Address", anchor=CENTER)
my_tree.heading("city", text="City", anchor=CENTER)
my_tree.heading("state", text="State", anchor=CENTER)
my_tree.heading("zip", text="Zipcode", anchor=CENTER)

data = [
	["John", "Elder", 1, "123 Elder St.", "Las Vegas", "NV", "89137"],
	["Mary", "Smith", 2, "435 West Lookout", "Chicago", "IL", "60610"],
	["Tim", "Tanaka", 3, "246 Main St.", "New York", "NY", "12345"],
	["Erin", "Erinton", 4, "333 Top Way.", "Los Angeles", "CA", "90210"],
	["Bob", "Bobberly", 5, "876 Left St.", "Memphis", "TN", "34321"],
	["Steve", "Smith", 6, "1234 Main St.", "Miami", "FL", "12321"],
	["Tina", "Browne", 7, "654 Street Ave.", "Chicago", "IL", "60611"],
	["Mark", "Lane", 8, "12 East St.", "Nashville", "TN", "54345"],
	["John", "Smith", 9, "678 North Ave.", "St. Louis", "MO", "67821"],
	["Mary", "Todd", 10, "9 Elder Way.", "Dallas", "TX", "88948"],
	["John", "Lincoln", 11, "123 Elder St.", "Las Vegas", "NV", "89137"],
	["Mary", "Bush", 12, "435 West Lookout", "Chicago", "IL", "60610"],
	["Tim", "Reagan", 13, "246 Main St.", "New York", "NY", "12345"],
	["Erin", "Smith", 14, "333 Top Way.", "Los Angeles", "CA", "90210"],
	["Bob", "Field", 15, "876 Left St.", "Memphis", "TN", "34321"],
	["Steve", "Target", 16, "1234 Main St.", "Miami", "FL", "12321"],
	["Tina", "Walton", 17, "654 Street Ave.", "Chicago", "IL", "60611"],
	["Mark", "Erendale", 18, "12 East St.", "Nashville", "TN", "54345"],
	["John", "Nowerton", 19, "678 North Ave.", "St. Louis", "MO", "67821"],
	["Mary", "Hornblower", 20, "9 Elder Way.", "Dallas", "TX", "88948"]]

count = 0
for record in data:
    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5],record[6]))
    count += 1

def delete_records():
    for record in my_tree.get_children():
    	my_tree.delete(record)

# delete_records()
items = my_tree.get_children()
for item in items:
    print(my_tree.item(item))

root.mainloop()
