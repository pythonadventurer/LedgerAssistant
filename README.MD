# Ledger Assistant
*Update: 2023-04-09-1526-11*

## Introduction

**LedgerAssistant** is a GUI for entering transactions into an [hledger-style](https://hledger.org) journal.
Easily handles transactions with multiple splits to different accounts. Includes calcuation of sales tax.  
A single transaction can have a combination of taxable and non-taxable splits.
Automatically calculates split amounts and ensures transactions is balanced before posting.

## License
 GNU General Public License 3. See the LICENSE file for details.
                       
## Planned Features and Usage
- Enter date, transaction description and amount at top.
- Enter transaction splits in the **Enter Splits** secion
- For each account distribution:
    - Select account from combo box
    - Enter amount to distribute
    - Click the Tax checkbox if the amount is to have sales tax added.
    - Enter a memo (optional)
    - Click the Add button
    - The line amount is subtracted from the distribution amount, and the remaining amount to distribute is displayed.
- When finished, Amount to Distribute should be zero. 
- Click the **Post** button to add the transaction to the journal file.
 
## Confguration
- See the file `config.ini`.

## Installation
- Written in Python 3.11.3. 
- Download as a *.zip file and extract.
- Install the requirements (``requirements.txt``)
- run ``gui_mockup.py`` to get an idea of what the app will look like.
 

