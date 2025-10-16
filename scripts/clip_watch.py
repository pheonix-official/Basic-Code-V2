#!/usr/bin/env python3
"""
Monitor the system clipboard and log unique text changes to a file.

Dependencies:
    pip install pyperclip

Usage Examples:
    # Log clipboard changes to default file 'cliplog.txt' every 1 second
    python clip_watch.py

    # Log to a custom file with minimum entry length 5
    python clip_watch.py --out my_clip_log.txt --minlen 5

    # Poll clipboard every 2 seconds
    python clip_watch.py --interval 2

CLI Arguments:
    --out      : Output log file name (default: cliplog.txt)
    --minlen   : Ignore entries shorter than this length (default: 1)
    --interval : Polling interval in seconds (default: 1)
"""

import argparse
import time
from datetime import datetime
import pyperclip
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Monitor clipboard and log unique text changes.")
    parser.add_argument('--out', type=str, default='cliplog.txt', help='Output log file')
    parser.add_argument('--minlen', type=int, default=1, help='Ignore entries shorter than this length')
    parser.add_argument('--interval', type=float, default=1, help='Polling interval in seconds')
    return parser.parse_args()

def main():
    args = parse_args()
    last_clip = None
    logged = set()
    try:
        with open(args.out, 'a') as logfile:
            while True:
                clip = pyperclip.paste()
                if (clip != last_clip and
                    isinstance(clip, str) and
                    len(clip) >= args.minlen and
                    clip not in logged):
                    timestamp = datetime.now().isoformat()
                    logfile.write(f"{timestamp}: {clip}\n")
                    logfile.flush()
                    logged.add(clip)
                    print(f"{timestamp}: {clip}")
                last_clip = clip
                time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
