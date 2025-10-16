#!/usr/bin/env python3
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
