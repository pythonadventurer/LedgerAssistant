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

import configparser
from pathlib import Path
import decimal

# Read config values into variables
config = configparser.ConfigParser()
config.read('config.ini')
varAccountsSource = config['accounts']['source']
varAccountsFile = config['accounts']['file']
varJournalFile = Path(config['transactions']['journal'])
varTaxPct = decimal.Decimal(config['transactions']['tax_pct'])/100

