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
from decimal import Decimal

from datetime import datetime
from dateutil.parser import *

decimal.getcontext().rounding = decimal.ROUND_HALF_UP


config = configparser.ConfigParser()
config.read('config.ini')

# Amounts are provided as numbers with two decimal places.
# Stored as integers in which the last two digits represent cents.

def ValidateDate(DateString):
    # convert date string to YYYY-MM-DD
    return parse(DateString).strftime("%Y-%m-%d")

def ValidateAmount(AmountString):
    # ensure amount has 2 decimal places, rounded to nearest 100th.
    return str(Decimal(AmountString).quantize(Decimal('.01')))


print(ValidateDate('4/15/23'))
print(ValidateDate('4/15'))
print(ValidateAmount('1'))
print(ValidateAmount('1.2435'))
