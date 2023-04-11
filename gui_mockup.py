"""
LedgerAssistant - a GUI front end for entering Ledger-compatible transactions.
Copyright (C) 2023  Robert T. Fowler IV

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""
from tkinter import *
from tkinter import ttk
from tkintertable import TableCanvas, TableModel
from config import *

root = Tk()
root.title('Ledger Assistant')
fraMain = Frame(root)

def AddRow(table):
    table.addRow()




# Menu
mnuMainMenu = Menu(root)
root.config(menu=mnuMainMenu)

mnuFile = Menu(mnuMainMenu,tearoff=0)
mnuMainMenu.add_cascade(label="File",menu=mnuFile)
mnuFile.add_command(label="Quit",command=root.quit)

mnuEdit = Menu(mnuMainMenu,tearoff=0)
mnuMainMenu.add_cascade(label="Edit",menu=mnuEdit)
mnuEdit.add_command(label="Preferences")

mnuHelp = Menu(mnuMainMenu,tearoff=0)
mnuMainMenu.add_cascade(label="Help",menu=mnuHelp)
mnuHelp.add_command(label="About")

# Transaction Frame

## Create Transaction Widgets
fraTransaction = Frame(fraMain,bd=2,relief="raised")

lblDate = Label(fraTransaction,text="Date",font=("Helvetica",12),width=10,anchor=E)
txtDate = Entry(fraTransaction,font=("Helvetica",12))

lblDescription = Label(fraTransaction,text="Description",font=("Helvetica",12),anchor=E)
txtDescription = Entry(fraTransaction,font=("Helvetica",12))

lblDistAmt = Label(fraTransaction,text="Amt. to Distribute",font=("Helvetica",12),anchor=E)
txtDistAmt = Entry(fraTransaction, font=("Helvetica",12))

btnPost = Button(fraTransaction,text="Post",width=10)

## Grid Transaction Widgets
lblDate.grid(row=0,column=0,sticky=(W,E),padx=5,pady=5)
txtDate.grid(row=0,column=1,sticky=(W,E),columnspan=2,padx=5,pady=5)

lblDescription.grid(row=1,column=0,sticky=(W,E),padx=5,pady=5)
txtDescription.grid(row=1,column=1,sticky=(W,E),columnspan=2, padx=5,pady=5)

lblDistAmt.grid(row=2,column=0,sticky=(W,E),padx=5,pady=5)
txtDistAmt.grid(row=2,column=1,sticky=(W,E),padx=5,pady=5)

btnPost.grid(row=2,column=2,sticky=(W,E),padx=5,pady=5)

# Split Entry Frame

## Create Split Entry Widgets
fraEnterSplits = Frame(fraMain,bd=2,relief="raised")

### lblAccount : anchor seems to make no difference
varAccount = StringVar()
lblAccount = Label(fraEnterSplits,text="Account",font=("Helvetica",12),anchor=E)
cboAccount = ttk.Combobox(fraEnterSplits,textvariable=varAccount,font=("Helvetica",12))
cboAccount['values'] = accounts

lblSplitAmount = Label(fraEnterSplits,text="Amount",font=("Helvetica",12),anchor=E)
txtSplitAmt = Entry(fraEnterSplits,font=("Helvetica",12))

lblTaxAmount = Label(fraEnterSplits,text="Tax Amt.",font=("Helvetica",12),anchor=E)
txtTaxAmount = Entry(fraEnterSplits,font=("Helvetica",12))

varApplyTax = IntVar()
chkApplyTax = ttk.Checkbutton(fraEnterSplits,text="Tax %",variable=varApplyTax,onvalue=1,offvalue=0)
lblTaxPct = Label(fraEnterSplits,text="7.0",font=("Helvetica",10))

varTotalAmount = StringVar()
lblTotalAmount = Label(fraEnterSplits,text="Total Amt.",font=("Helvetica",12),anchor=E)
txtTotalAmount = Entry(fraEnterSplits,textvariable=varTotalAmount,font=("Helvetica",12))

varMemo = StringVar()
lblMemo = Label(fraEnterSplits,text="Memo",font=("Helvetica",12),anchor=E)
txtMemo = Entry(fraEnterSplits,textvariable=varMemo,font=("Helvetica",12))

## Grid Split Entry Widgets
lblAccount.grid(row=0,column=0,padx=5,pady=5,sticky=(E,W))
cboAccount.grid(row=0,column=1,columnspan=3,padx=5,pady=5,sticky=(E,W))

lblSplitAmount.grid(row=1,column=0,padx=5,pady=5,sticky=(E,W))
txtSplitAmt.grid(row=1,column=1,padx=5,pady=5,sticky=(E,W))

lblTaxAmount.grid(row=2,column=0,padx=5,pady=5,sticky=(E,W))
txtTaxAmount.grid(row=2,column=1,padx=5,pady=5,sticky=(E,W))

chkApplyTax.grid(row=2,column=2,padx=5,pady=5,sticky=(E,W))
lblTaxPct.grid(row=2,column=3,padx=5,pady=5,sticky=(E,W))

lblTotalAmount.grid(row=3,column=0,padx=5,pady=5,sticky=(E,W))
txtTotalAmount.grid(row=3,column=1,padx=5,pady=5,sticky=(E,W))

lblMemo.grid(row=4,column=0,padx=(80,5),pady=5,sticky=(E,W))
txtMemo.grid(row=4,column= 1,columnspan=3,padx=5,pady=5,sticky=(E,W))

## Split Entry Button Row
global mdlModel
mdlModel = TableModel()
mdlModel.addRow(Account='',Amount='',Memo='')

def add_split():
    # mdlModel.addRow(Account=varAccount,Amount=varTotalAmount,Memo=varMemo)
    print(varAccount.get())

fraButtonRow = Frame(fraEnterSplits)
btnAdd = Button(fraButtonRow,text="Add",width=10,command=add_split)
btnUpdate = Button(fraButtonRow,text="Update",width=10)
btnDelete = Button(fraButtonRow,text="Delete",width=10)

## Grid Split Entry Buttons
btnAdd.grid(row=0,column=0,padx=5,pady=5)
btnUpdate.grid(row=0,column=1,padx=5,pady=5)
btnDelete.grid(row=0,column=2,padx=5,pady=5)
fraButtonRow.grid(row=5,column=0,columnspan=4)

# Split Details Frame
fraSplitDetails = Frame(fraMain,bd=2,relief="raised")


# Split Details Scrollbar
scrSplitsScroll = Scrollbar(fraSplitDetails)
scrSplitsScroll.pack(side=RIGHT,fill=Y)

# Split Details Treeview Table
tblSplits = ttk.Treeview(fraSplitDetails,yscrollcommand=scrSplitsScroll.set,selectmode="extended")
tblSplits.pack()

# Configure the scrollbar
scrSplitsScroll.config(command=tblSplits.yview())


# Define Columns
tblSplits["columns"] = ("account","amount","memo")

# Format Columns
tblSplits.column("#0",width=0,stretch=NO)
tblSplits.column("account",anchor=W,width=150)
tblSplits.column("amount",anchor=W,width=75)
tblSplits.column("memo",anchor=W,width=200)

# Create Headings
tblSplits.heading("#0",text="",anchor=W)
tblSplits.heading("account",text="Account",anchor=W)
tblSplits.heading("amount",text="Amount",anchor=W)
tblSplits.heading("memo",text="Memo",anchor=W)




fraMain.grid(row=0,column=0,padx=5,pady=5)
fraTransaction.grid(row=0,column=0,padx=5,pady=5,sticky=(E,W))
fraEnterSplits.grid(row=1,column=0,padx=5,pady=5,sticky=(E,W))
fraSplitDetails.grid(row=2,column=0,padx=5,pady=5)



root.mainloop()

