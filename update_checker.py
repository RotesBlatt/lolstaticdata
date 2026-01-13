#!/usr/bin/env python3
"""
Standalone script to check version and update if needed.
Can be run manually or scheduled via cron/Windows Task Scheduler.
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lolstaticdata.check_and_update import main

if __name__ == "__main__":
    sys.exit(main())
