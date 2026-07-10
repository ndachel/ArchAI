#!/usr/bin/env python3

import json
import subprocess


def main():
    try:
        result = subprocess.run(
            ["lspci"],
            capture_output=True,
            text=True,
            check=True,
        )

        devices = result.stdout.strip().splitlines()

    except Exception as e:
        devices = [f"error: {e}"]

    print(json.dumps({
        "devices": devices
    }, indent=2))


if __name__ == "__main__":
    main()
