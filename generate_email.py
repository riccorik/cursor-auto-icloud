#!/usr/bin/env python3
"""
Wrapper for iCloud Email Generator
This provides an easy way to import and use the iCloud Hide My Email generator.
"""

import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from the new location
try:
    from src.icloud.generateEmail import generateIcloudEmail
except ImportError:
    # If that fails, try relative imports
    try:
        from src.icloud.generateEmail import generateIcloudEmail
    except ImportError:
        raise ImportError("Failed to import iCloud email generator. Make sure all dependencies are installed.")

# Export the function for backward compatibility
__all__ = ['generateIcloudEmail']

# If run directly, generate emails
if __name__ == "__main__":
    import sys
    
    count = 5  # Default count
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print(f"Invalid count: {sys.argv[1]}")
            sys.exit(1)
    
    print(f"Generating {count} iCloud Hide My Email addresses...")
    emails = generateIcloudEmail(count)
    
    if emails:
        print(f"Successfully generated {len(emails)} email addresses:")
        for email in emails:
            print(email)
    else:
        print("Failed to generate any email addresses.") 