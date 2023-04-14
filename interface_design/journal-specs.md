2023-04-08 Walgreens                                   
    Liabilities:AAA Credit Card                           -30.00
    Expenses:Medical:Prescriptions & OTC Meds       -11111111.00 ; memo: Candesartan                                                                                                                             


"""
# Journal Specs
- Fixed width text lines
- Each column is separated by a space.

# Transaction Header
Column 0 : Date
start: 0
length: 10

Column 1 : Description
start: 11
length: 40

# Splits
Column 0 : Indent
start: 0
length: 4

Column 1 : Account
start: 4
length: 47

Column 2 : Amount
start: 52
length: 12
* includes minus sign

Column 3 : Memo
start: 65
length: 250
* must start with "; "

"""