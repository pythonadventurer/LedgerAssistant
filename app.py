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
from gui import *
from models import *


class LedgerAssistant:

    def __init__(self,root):
        root.title("LedgerAssistant")
        mnuMain = MainMenu(root)
        root.config(menu=mnuMain)
        EnterTransaction = TransactionEntry(root)



root = Tk()
LedgerAssistant(root)
root.mainloop()
