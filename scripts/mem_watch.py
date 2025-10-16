#!/usr/bin/env python3
"""
Monitor and log a process's memory usage over time.

Dependencies:
    pip install psutil

Usage Examples:
    # Monitor process with PID 1234, log every 2 seconds to mem.csv
    python memory_logger.py --pid 1234

    # Monitor with a custom interval of 1 second and output file memory_log.csv
    python memory_logger.py --pid 1234 --interval 1 --out memory_log.csv

    # Show live memory usage in the terminal while logging
    python memory_logger.py --pid 1234 --live

CLI Arguments:
    --pid       : Process ID to monitor (required)
    --interval  : Interval in seconds between samples (default: 2)
    --out       : Output CSV file name (default: mem.csv)
    --live      : Show live memory usage in terminal
"""

import argparse
import csv
import time
import psutil
import sys
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Monitor and log a process's memory usage over time.")
    parser.add_argument('--pid', type=int, required=True, help='Process ID to monitor')
    parser.add_argument('--interval', type=float, default=2, help='Interval in seconds between samples')
    parser.add_argument('--out', type=str, default='mem.csv', help='Output CSV file')
    parser.add_argument('--live', action='store_true', help='Show live memory usage in terminal')
    return parser.parse_args()

def main():
    args = parse_args()
    try:
        proc = psutil.Process(args.pid)
    except psutil.NoSuchProcess:
        print(f"Process with PID {args.pid} does not exist.")
        sys.exit(1)

    with open(args.out, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'rss', 'vms'])
        while True:
            try:
                mem_info = proc.memory_info()
                timestamp = datetime.now().isoformat()
                rss = mem_info.rss
                vms = mem_info.vms
                writer.writerow([timestamp, rss, vms])
                csvfile.flush()
                if args.live:
                    print(f"{timestamp} | RSS: {rss} | VMS: {vms}", end='\r')
                time.sleep(args.interval)
            except psutil.NoSuchProcess:
                print("\nProcess ended. Exiting.")
                break
            except KeyboardInterrupt:
                print("\nInterrupted by user. Exiting.")
                break

if __name__ == "__main__":
    main()
