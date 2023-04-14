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

import configparser
from models import *
import decimal
# decimal.getcontext().rounding = decimal.ROUND_HALF_UP


config = configparser.ConfigParser()
config.read('config.ini')
varTaxPct = decimal.Decimal(config['transactions']['tax_pct'])/100
# Amounts are provided as numbers with two decimal places.
# Stored as integers in which the last two digits represent cents.

# test_transaction = Transaction('2023-04-12','Amazon 112-0088785-1211437 ')
# test_transaction.add_split('','Liabilities:AAA Credit Card',-85.38)
# test_transaction.add_split('Travelon Small Backpack Peacock One Size', 'Expenses:Travel:Misc', 42.59)
# test_transaction.add_split('Beraliy Travel Backpack', 'Expenses:Travel:Misc', 42.79)
# print(test_transaction.hledger_format())


def calc_tax(num_string):
    result = decimal.Decimal(num_string) * varTaxPct
    return decimal.Decimal(result).quantize(decimal.Decimal('.01'),
           rounding=decimal.ROUND_HALF_UP)


print(calc_tax('4.56'))
