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
from tkinter import filedialog
from tkinter import messagebox
from autocombo import AutocompleteCombobox
from pathlib import Path
from models import *
import decimal
from config import *
from controller import *
from tests import TestTransaction


decimal.getcontext().rounding = decimal.ROUND_HALF_UP

CurrentJournal = Journal(varJournalFile)
CurrentJournal.get_hledger_trans(varJournalFile)

if varAccountsSource == 'file':
    pass

else:
    accounts = CurrentJournal.GetJournalAccounts()

class LedgerAssistant:

    def __init__(self,root):
        root.title("LedgerAssistant")
        mnuMain = MainMenu(root)
        root.config(menu=mnuMain)
        EnterTransaction = TransactionEntry(root)

class MainMenu(Menu):
    def __init__(self,root):
        Menu.__init__ (self,root)

        def SelectJournal():
            JournalFile = filedialog.askopenfilename(title = "Select a Journal File")
            config['transactions']['journal'] = JournalFile
            with open('config.ini','w') as f:
                config.write(f)

        # TODO Generic message box function "Sorry, this option has not yet been implemented."
        mnuFile = Menu(self,tearoff=0)
        self.add_cascade(label="File",menu=mnuFile)
        mnuFile.add_command(label="Select Journal",command=SelectJournal)
        mnuFile.add_command(label="Quit",command=root.quit)

        mnuEdit = Menu(self,tearoff=0)
        self.add_cascade(label="Edit",menu=mnuEdit)
        mnuEdit.add_command(label="Preferences")
        # TODO Preferences window - include select journal
        # TODO Status bar at bottom to show current journal file path

        mnuHelp = Menu(self,tearoff=0)
        self.add_cascade(label="Help",menu=mnuHelp)
        mnuHelp.add_command(label="About")
        # TODO Help --> About
        # TODO Help --> Documentation

class TransactionEntry(Frame):
    def __init__(self,parent):
        Frame.__init__ (self,parent)
        
        def post():
            # Don't allow posting unless balance is zero.
            CurrentTransaction = Transaction(varDate.get(),varDescription.get())
            lines = tblSplits.get_children()
            for line in lines:
                CurrentTransaction.add_split(tblSplits.item(line)['values'][2],
                                             tblSplits.item(line)['values'][0],
                                             tblSplits.item(line)['values'][1])
            CurrentJournal.transactions.append(CurrentTransaction)
            CurrentJournal.export_hledger(varJournalFile)
          
            ClearTrasactionEntry()
            ClearSplitEntry()
            ClearSplits()
            messagebox.showinfo("Ledger Assistant","Transaction has been posted.")

           
        def AddSplit():
            UpdateSplitTotal()
            tblSplits.insert(parent='',index='end',iid=None,text='',
                             values=(cboAccount.get(),varTotalAmount.get(),varMemo.get()))
            ClearSplitEntry()
            UpdateDistAmt()

        def UpdateDistAmt():
            items = tblSplits.get_children()
            splits_total = decimal.Decimal('0.00')

            for item in items:
                splits_total += decimal.Decimal(tblSplits.item(item)['values'][1])

            varDistAmount.set(decimal.Decimal(splits_total))

        def CalculateTax():
            if varApplyTax.get() == 1:
                tax_amt = decimal.Decimal(varSplitAmount.get()) * varTaxPct

                # Round to nearest cent
                tax_amt = decimal.Decimal(tax_amt).quantize(decimal.Decimal('.01'),
                       rounding=decimal.ROUND_HALF_UP)

                varTaxAmount.set(str(tax_amt))
                
            else:
                varTaxAmount.set("0.00")
                varTotalAmount.set(varSplitAmount.get())
            UpdateSplitTotal()               
            UpdateDistAmt()

        def UpdateSplitTotal():
            varTotalAmount.set(decimal.Decimal(varSplitAmount.get())+decimal.Decimal(varTaxAmount.get()))

        def ClearTrasactionEntry():
            varDescription.set("")
            varDistAmount.set("0.00")

        def ClearSplitEntry():
            varSplitAmount.set("0.00")
            varTaxAmount.set("0.00")
            varTotalAmount.set("0.00")
            varMemo.set("")
            UpdateDistAmt()

        def ClearSplits():
            for record in tblSplits.get_children():
            	tblSplits.delete(record)

        def DeleteSplit():
            x = tblSplits.selection()[0]
            tblSplits.delete(x)
            UpdateDistAmt()
        
        def OnDateFocusOut(e):
            varDate.set(ValidateDate(varDate.get()))

        def OnAmtFocusOut(e):
            strSplitAmount = varSplitAmount.get()
            varSplitAmount.set(ValidateAmount(strSplitAmount))
            

        ## Create Transaction Widgets
        fraTransaction = Frame(self,bd=2,relief="raised")

        varDate = StringVar()
        lblDate = Label(fraTransaction,text="Date",font=("Helvetica",12),width=10,anchor=E)
        txtDate = Entry(fraTransaction,textvariable=varDate, font=("Helvetica",12))
        txtDate.bind("<FocusOut>",OnDateFocusOut)

        varDescription = StringVar()
        lblDescription = Label(fraTransaction,text="Description",font=("Helvetica",12),anchor=E)
        txtDescription = Entry(fraTransaction,textvariable=varDescription, font=("Helvetica",12))
        
        varDistAmount = StringVar()
        lblDistAmt = Label(fraTransaction,text="Amt. to Distribute",font=("Helvetica",12),anchor=E)
        txtDistAmt = Entry(fraTransaction, state=DISABLED,textvariable=varDistAmount,font=("Helvetica",12))

        btnPost = Button(fraTransaction,text="Post",width=10,command=post)

        ## Grid Transaction Widgets
        lblDate.grid(row=0,column=0,sticky=(W,E),padx=5,pady=5)
        txtDate.grid(row=0,column=1,sticky=(W,E), columnspan=2,padx=5,pady=5)
        
        lblDescription.grid(row=1,column=0,sticky=(W,E),padx=5,pady=5)
        txtDescription.grid(row=1,column=1,sticky=(W,E),columnspan=2, padx=5,pady=5)

        lblDistAmt.grid(row=2,column=0,sticky=(W,E),padx=5,pady=5)
        txtDistAmt.grid(row=2,column=1,sticky=(W,E),padx=5,pady=5)

        btnPost.grid(row=2,column=2,sticky=(W,E),padx=5,pady=5)

        # Split Entry Frame

        ## Create Split Entry Widgets
        fraEnterSplits = Frame(self,bd=2,relief="raised")

        ### lblAccount : anchor seems to make no difference
        varAccount = StringVar()
        lblAccount = Label(fraEnterSplits,text="Account",font=("Helvetica",12),anchor=E)

        # TODO Account combo box limit to list

        cboAccount = AutocompleteCombobox(fraEnterSplits)
        cboAccount.set_completion_list(accounts)

        varSplitAmount = StringVar()
        lblSplitAmount = Label(fraEnterSplits,text="Amount",font=("Helvetica",12),anchor=E)
        txtSplitAmount = Entry(fraEnterSplits,textvariable=varSplitAmount,font=("Helvetica",12))
        varSplitAmount.set("0.0")
        txtSplitAmount.bind("<FocusOut>",OnAmtFocusOut)


        varTaxAmount = StringVar()
        lblTaxAmount = Label(fraEnterSplits,text="Tax Amt.",font=("Helvetica",12),anchor=E)
        txtTaxAmount = Entry(fraEnterSplits,state=DISABLED,  textvariable=varTaxAmount,font=("Helvetica",12),)
        varTaxAmount.set("0.0")

        # TODO Fix inconsisent behavior of apply tax
        varApplyTax = IntVar()
        chkApplyTax = Checkbutton(fraEnterSplits,text="Tax %",variable=varApplyTax,onvalue=1,offvalue=0,command=CalculateTax)
        chkApplyTax.deselect()

        lblTaxPct = Label(fraEnterSplits,text="7.0",font=("Helvetica",10))

        varTotalAmount = StringVar()
        lblTotalAmount = Label(fraEnterSplits,text="Total Amt.",font=("Helvetica",12),anchor=E)
        txtTotalAmount = Entry(fraEnterSplits,state=DISABLED, textvariable=varTotalAmount,font=("Helvetica",12))
        varTotalAmount.set("0.0")

        varMemo = StringVar()
        lblMemo = Label(fraEnterSplits,text="Memo",font=("Helvetica",12),anchor=E)
        txtMemo = Entry(fraEnterSplits,textvariable=varMemo,font=("Helvetica",12))
        varMemo.set("")

        ## Grid Split Entry Widgets
        lblAccount.grid(row=0,column=0,padx=5,pady=5,sticky=(E,W))
        cboAccount.grid(row=0,column=1,columnspan=3,padx=5,pady=5,sticky=(E,W))

        lblSplitAmount.grid(row=1,column=0,padx=5,pady=5,sticky=(E,W))
        txtSplitAmount.grid(row=1,column=1,padx=5,pady=5,sticky=(E,W))

        lblTaxAmount.grid(row=2,column=0,padx=5,pady=5,sticky=(E,W))
        txtTaxAmount.grid(row=2,column=1,padx=5,pady=5,sticky=(E,W))

        chkApplyTax.grid(row=2,column=2,padx=5,pady=5,sticky=(E,W))
        lblTaxPct.grid(row=2,column=3,padx=5,pady=5,sticky=(E,W))

        lblTotalAmount.grid(row=3,column=0,padx=5,pady=5,sticky=(E,W))
        txtTotalAmount.grid(row=3,column=1,padx=5,pady=5,sticky=(E,W))

        lblMemo.grid(row=4,column=0,padx=(80,5),pady=5,sticky=(E,W))
        txtMemo.grid(row=4,column= 1,columnspan=3,padx=5,pady=5,sticky=(E,W))

        ## Split Entry Button Row
        fraButtonRow = Frame(fraEnterSplits)

        # btnAdd = Button(fraButtonRow,text="Add",width=10,command=add_split)
        btnAdd = Button(fraButtonRow,text="Add",width=10,command=AddSplit)
        btnUpdate = Button(fraButtonRow,text="Update",width=10)
        btnDelete = Button(fraButtonRow,text="Delete",width=10,command=DeleteSplit)

        ## Grid Split Entry Buttons
        btnAdd.grid(row=0,column=0,padx=5,pady=5)
        btnUpdate.grid(row=0,column=1,padx=5,pady=5)
        btnDelete.grid(row=0,column=2,padx=5,pady=5)
        fraButtonRow.grid(row=5,column=0,columnspan=4)

        # Split Details Frame
        fraSplitDetails = Frame(self,bd=2,relief="raised")

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
        tblSplits.column("amount",anchor=E,width=75)
        tblSplits.column("memo",anchor=W,width=200)

        # Create Headings
        tblSplits.heading("#0",text="",anchor=W)
        tblSplits.heading("account",text="Account",anchor=CENTER)
        tblSplits.heading("amount",text="Amount",anchor=CENTER)
        tblSplits.heading("memo",text="Memo",anchor=CENTER)

        # Grid this
        self.grid(row=0,column=0,padx=5,pady=5)
        fraTransaction.grid(row=0,column=0,padx=5,pady=5,sticky=(E,W))
        fraEnterSplits.grid(row=1,column=0,padx=5,pady=5,sticky=(E,W))
        fraSplitDetails.grid(row=2,column=0,padx=5,pady=5)

        # ClearSplitEntry()
        
        # varDate.set(TestTransaction.date)
        # varDescription.set(TestTransaction.description)
        # for split in TestTransaction.splits:
        #     tblSplits.insert(parent='',index='end',iid=None,text='',values=(split.account,split.amount,split.memo))

        ClearSplitEntry()
        UpdateDistAmt()