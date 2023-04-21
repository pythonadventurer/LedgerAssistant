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
import decimal
from pathlib import Path
from datetime import datetime
from dateutil.parser import *

# TODO Ability to save transactions

# Rounding for normal people!
decimal.getcontext().rounding = decimal.ROUND_HALF_UP

def ValidateDate(DateString):
    """    
    Convert date string to YYYY-MM-DD
    """
    return parse(DateString).strftime("%Y-%m-%d")

def ValidateAmount(AmountString):
    """
    Ensure amount has 2 decimal places, rounded to nearest 100th.
    """
    return str(decimal.Decimal(AmountString).quantize(decimal.Decimal('.01')))


def AmtToDecimal(Amount):
    """
    Convert a float to a number string, rounded to 2 decimal places.
    """
    return str(decimal.Decimal(Amount).quantize(decimal.Decimal('.01')))

# TODO StringAdd

def StringAdd(String):
    """
    return the sum the numbers in string separated by plus signs:
    all numbers will be converted to decimals rounded to 2 decimal
    places:
        '2+10.5+5.43'
    """
    pass
# TODO StringMultiply

def StringMultiply(String):
    """
    return the product of numbers in a string separated by asterisks:
       '14*7*8*1.07'
    """
    pass




