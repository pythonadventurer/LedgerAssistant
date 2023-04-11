from tkinter import *
from tkintertable import TableCanvas, TableModel

root = Tk()
root.title('TkTable Demo')
tframe = Frame(root)
tframe.pack(fill=BOTH,expand=1)

data = {'1':{'last_name':'Fowler',
             'first_name':'Rob',
             'phone':'954-593-5278'},
        '2':{'last_name':'Fowler',
             'first_name':'Donna',
             'phone':'954-790-4954'},
        '3':{'last_name':'Knighton',
             'first_name':'Zac',
             'phone':'404-123-4567'}}

# tblContacts = TableCanvas(tframe,
#                           data=data,
#                           cellwidth=60, 
#                           cellbackgr='#e3f698',
#                           thefont=('Arial',12),
#                           rowheight=18, 
#                           rowheaderwidth=30,
# 			              rowselectedcolor='yellow',
#                           read_only=False)

tblContacts = TableCanvas(tframe,rowheaderwidth=0)
tblContacts.importCSV("us-500.csv",sep=",")

                         

tblContacts.show()


root.mainloop()
