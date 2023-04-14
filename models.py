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


class Transaction:
    def __init__(self,date,description):
        """
        date = YYYY-MM-DD
        """
        self.date = date
        self.description = description
        self.memo = ""
        self.splits = []

    def add_split(self,memo,account,amount):
        split = TransactionSplit(memo, account, amount)
        self.splits.append(split)

    def balance(self):
        bal = 0
        for split in self.splits:
            bal += split.amount
        return bal

    def printout(self):
        print(self.date, self.description)
        for split in self.splits:
            print(f"    {split.account} {split.amount} {split.memo}")
        print(f"Balance: {self.balance()}")


class TransactionSplit:
    def __init__(self,memo,account,amount):
        self.memo = memo
        self.account = account
        self.amount = amount

class Journal:
    def __init__(self):
        self.transactions = []

    def balance(self):
        bal = 0
        for transaction in self.transactions:
            bal += transaction.balance()
        return bal

    def get_hledger_trans(self,ledger_file):
        """
        Get transactions from an hledger formatted file.
        """
        journal = []
        with open(ledger_file,"r",encoding="utf-8") as f:
            lines = f.read().split("\n")
        for n in range(len(lines)):
            if lines[n].startswith("account") or lines[n].startswith("commodity") or lines[n] == "" or lines[n] == "\n":
                continue
            else:
                if re.match("^\d\d\d\d-\d\d-\d\d",lines[n]):
                    trans_date = re.match("^\d\d\d\d-\d\d-\d\d",lines[n])[0]
                    trans_description = lines[n][11:]
                    new_trans = Transaction(trans_date,trans_description)
 
                else:
                    # split_line includes account, amount and memo.
                    split_line = lines[n]
                    split_account = split_line[4:split_line.find("  ",4)]
                    if ";" in lines[n]:
                        split_memo = split_line[split_line.find(";"):]
                        split_amount = split_line[len(split_account)+5:split_line.find(";")].strip()
                    else:
                        split_memo = ""
                        split_amount = split_line[len(split_account)+5:].strip()
                    try:
                        split_amount = Decimal(split_amount)*100
                        split_amount = int(split_amount)
                        new_trans.add_split(split_memo,split_account,split_amount)
                    except (ValueError, DecimalException):
                        break
                    try:
                        if re.match("^\d\d\d\d-\d\d-\d\d",lines[n+1]) or lines[n+1] == "\n" or lines[n+1] == "":
                            journal.append(new_trans)

                    except IndexError:
                        continue
       
        self.transactions = journal

    def hledger_journal_text(self):
        """
        return raw hledger formatted text from transactions.
        """
        self.transactions.sort(key=lambda x: x.date) 
        hledger_text = ""
        for transaction in self.transactions:
            hledger_text += f"{transaction.date} {transaction.description}\n"
            for split in transaction.splits:
                amount = str("{:.2f}".format(Decimal(split.amount)/100))
                num_spaces = (60-len(split.account)-len(amount))
                spacing = num_spaces * " "
                hledger_text += f"    {split.account}{spacing}{amount}"
                if split.memo != "":
                    # sanitize memo field
                    memo = split.memo
                    memo = memo.replace(","," ")
                    memo = memo.replace(".","_")
                    memo = memo.replace("  "," ")
                    memo = memo.replace(":"," ")
                    memo = memo.replace("\n"," ")
                    memo = memo.strip()
                    hledger_text += f" {memo}"
                hledger_text +="\n"
            hledger_text +="\n"
        return hledger_text

    def export_hledger(self,accounts_file,file_path):
        """
        Export to hledger format. Accounts file : list of account and
        commodity declarations to put at beginning of ledger.
        """
        # sort transactions by date
        self.transactions.sort(key=lambda x: x.date) 

        # add account declarations
        hledger_text = ""
        if accounts_file != None:
            with open(accounts_file,"r",encoding="utf-8") as accounts:
                hledger_text += accounts.read()

        # convert the transactions to hledger format
        hledger_text += self.hledger_journal_text()

        with open(file_path,"w",encoding="utf-8") as file:
            file.write(hledger_text)


    def get_ebay_trans(self,ebay_file):
        with open(ebay_file,"r",encoding="utf-8") as file:
            ebay_text = file.read()

        # deal with files that have double quotes on all fields
        ebay_text = ebay_text[ebay_text.find("Transaction creation date")-1:]
        if ebay_text.startswith("\n"):
            ebay_text = ebay_text[1:]

        ebay_dict_text = csv.DictReader(ebay_text.splitlines())
        rows = [row for row in ebay_dict_text]

        payout_journal = []
        payout_trans = None
        prev_payout_id = ""

        for row in rows:
            if row["Type"] == "Payout":
                continue

            if row["Payout ID"] != prev_payout_id:
                if payout_trans != None:
                    payment_account = "Assets:BrightStar Checking"
                    payment_amount = abs(payout_trans.balance())
                    split = TransactionSplit("", payment_account, payment_amount)
                    payout_trans.splits.insert(0,split)
                    payout_journal.append(payout_trans)

                prev_payout_id = row["Payout ID"]
                payout_id = row["Payout ID"]
                payout_date = date_fixer(row["Payout date"])
                payout_description = "Ebay payout ID " + payout_id
                payout_trans = Transaction(payout_date,payout_description)

            if row["Type"] == "Shipping label":
                split_memo = " ; memo: Shipping label - " + row["Description"]
                split_account = "Expenses:Cost of Sales:Shipping Costs"
                split_amount = -int(Decimal(row["Net amount"])*100)
                split = TransactionSplit(split_memo, split_account, split_amount)
                payout_trans.splits.append(split)    

            if row["Type"] == "Other fee":
                split_memo = " ; memo: " + row["Description"]
                split_account = "Expenses:Cost of Sales:Ebay Fees"
                split_amount = abs(int(Decimal(row["Net amount"])*100))
                split = TransactionSplit(split_memo, split_account, split_amount)
                payout_trans.splits.append(split) 

            if row["Type"] == "Order":       
                # record the sale as a credit (-)
                split_memo = " ; memo: " + row["Custom label"] + " " + row["Item title"]
                split_account = "Income:Current Income:Sales"
                split_amount = -abs(int(Decimal(row["Item subtotal"])*100))
                split = TransactionSplit(split_memo, split_account, split_amount)
                payout_trans.splits.append(split) 

                # record buyer paid shipping amount as a credit to shipping costs
                split_memo = " ; memo: Buyer paid shipping"
                split_account = "Expenses:Cost of Sales:Shipping Costs"
                split_amount = -abs(int(Decimal(row["Shipping and handling"])*100))
                split = TransactionSplit(split_memo, split_account, split_amount)
                payout_trans.splits.append(split) 

                # record final value fees
                split_memo = ""
                split_account = "Expenses:Cost of Sales:Ebay Fees"
                split_amount = abs(int(Decimal(row["Final Value Fee - fixed"])*100))
                split = TransactionSplit(split_memo, split_account, split_amount)
                payout_trans.splits.append(split) 

                split_memo = ""
                split_account = "Expenses:Cost of Sales:Ebay Fees"
                split_amount = abs(int(Decimal(row["Final Value Fee - variable"])*100))
                split = TransactionSplit(split_memo, split_account, split_amount)
                payout_trans.splits.append(split)

            if row["Type"] ==  "Hold" or row["Type"] == "Claim" or row["Type"] == "Refund":    
                # these are too freaking complicated to deal with.  Just charge them off
                # to sales.
                split_memo = f" ; memo: {row['Type']} - " + row["Custom label"] + " " + row["Item title"]
                split_account = "Income:Current Income:Sales"
                split_amount = row["Net amount"]                
                if split_amount == "0" or split_amount == "--":
                    split_amount = 0
                else:
                    split_amount = -int(Decimal(split_amount)*100)
                split = TransactionSplit(split_memo, split_account, split_amount)
                payout_trans.splits.append(split) 

            if rows.index(row) == len(rows) - 1:
                payment_account = "Assets:BrightStar Checking"
                payment_amount = abs(payout_trans.balance())
                split = TransactionSplit("", payment_account, payment_amount)
                payout_trans.splits.insert(0,split)
                payout_journal.append(payout_trans)

        self.transactions = payout_journal  