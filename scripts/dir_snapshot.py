#!/usr/bin/env python3
"""
Take periodic snapshots of a directory and log changes to a file.

Usage Examples:
    # Monitor /my/folder every 60 seconds and log changes to snapshot_log.json
    python dir_snapshot.py --path /my/folder

    # Monitor /home/user/docs every 30 seconds and log to custom file
    python dir_snapshot.py --path /home/user/docs --interval 30 --out my_snapshots.json

CLI Arguments:
    --path     : Directory to monitor (required)
    --interval : Interval in seconds between snapshots (default: 60)
    --out      : Output log file (default: snapshot_log.json)
"""

import argparse
import os
import time
import hashlib
import json
from datetime import datetime

def file_hash(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def snapshot_dir(root):
    snapshot = {}
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                stat = os.stat(fpath)
                snapshot[fpath] = {
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                    "hash": file_hash(fpath)
                }
            except Exception:
                continue
    return snapshot

def compare_snapshots(old, new):
    changes = {"new": [], "deleted": [], "modified": [], "renamed": []}
    old_files = set(old.keys())
    new_files = set(new.keys())

    changes["new"] = list(new_files - old_files)
    changes["deleted"] = list(old_files - new_files)

    # Detect modified files
    for f in old_files & new_files:
        if old[f]["hash"] != new[f]["hash"] or old[f]["size"] != new[f]["size"]:
            changes["modified"].append(f)

    # Simple rename detection: files with same hash but different path
    old_hash_map = {v["hash"]: k for k, v in old.items()}
    for f in changes["new"]:
        h = new[f]["hash"]
        if h in old_hash_map and old_hash_map[h] not in changes["deleted"]:
            changes["renamed"].append((old_hash_map[h], f))

    return changes

def main():
    parser = argparse.ArgumentParser(description="Take periodic snapshots of a directory and log changes.")
    parser.add_argument('--path', type=str, required=True, help='Directory to monitor')
    parser.add_argument('--interval', type=int, default=60, help='Interval in seconds between snapshots')
    parser.add_argument('--out', type=str, default='snapshot_log.json', help='Output log file')
    args = parser.parse_args()

    prev_snapshot = snapshot_dir(args.path)
    while True:
        time.sleep(args.interval)
        curr_snapshot = snapshot_dir(args.path)
        changes = compare_snapshots(prev_snapshot, curr_snapshot)
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "changes": changes
        }
        with open(args.out, "a") as logfile:
            logfile.write(json.dumps(log_entry) + "\n")
        print(f"{log_entry['timestamp']}: Changes detected: {changes}")
        prev_snapshot = curr_snapshot

if __name__ == "__main__":
    main()
