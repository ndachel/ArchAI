#!/usr/bin/env python3

import json
import shutil
import psutil

def main():
    drives_usage = []

    # Iterate over all mounted partitions
    for partition in psutil.disk_partitions():
        # Skip loop devices and mock file systems common in Linux (optional)
        if "loop" in partition.device:
            continue
            
        try:
            # Fetch usage statistics for the drive's mount point
            usage = shutil.disk_usage(partition.mountpoint)
            
            drives_usage.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total_bytes": usage.total,
                "used_bytes": usage.used,
                "free_bytes": usage.free,
                "status": "accessible"
            })
        except (PermissionError, FileNotFoundError) as e:
            # Capture drives that are restricted or currently unmounted
            drives_usage.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "status": f"error: {type(e).__name__}"
            })

    # Print the combined data as a single JSON string
    print(json.dumps(drives_usage, indent=2))


if __name__ == "__main__":
    main()

