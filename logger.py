"""
This file is kept for backward compatibility.
The actual implementation has moved to src/utils/logger.py.
"""

import os
import sys

# Add the current directory to the path so we can import the src package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from the new location
from src.utils.logger import *

# No need to initialize anything here, as the src/utils/logger.py already initializes itself 