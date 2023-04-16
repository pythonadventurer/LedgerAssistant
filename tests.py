"""
Ledger Assistant - a GUI front end for entering Ledger-compatible transactions.
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
from models import *
from config import *


TestTransaction = Transaction("2023-04-16","Amazon 111-3748552-0949834")
splits = [["Liabilities:AAA Credit Card","-183.39",""],
          ["Expenses:Home:Improvements","138.99","5 of: WYZE Cam OG Security Camera, Indoor/Outdoor, 1080p HD Wi-Fi"],
          ["Expenses:Home:Improvements","44.40","5 of: NY 32GB Elite Class 10 U1 microSDHC Flash Memory Card"],
]
for line in splits:
    NewSplit = TransactionSplit(line[2], line[0], line[1])
    TestTransaction.splits.append(NewSplit)


MyJournal = Journal(varJournalFile)
MyJournal.get_hledger_trans(varJournalFile)
# print(MyJournal.transactions[-1].date)
# print(MyJournal.transactions[-1].description)



