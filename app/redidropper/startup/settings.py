"""
This file is used to store settings which can be over-ruled
using environment variables.

"""

import os


DB_USER = os.getenv('REDI_DROPPER_DB_USER', 'redidropper')
DB_PASS = os.getenv('REDI_DROPPER_DB_PASS', 'securepass')
