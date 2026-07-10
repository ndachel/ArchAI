#!/usr/bin/env python3

import json
import subprocess


def main():
    try:
        result = subprocess.run(
            ["pacman", "-Q"],
            capture_output=True,
            text=True,
            check=True,
        )

        packages = result.stdout.strip().splitlines()

    except Exception as e:
        packages = [f"error: {e}"]

    print(json.dumps({
        "package_count": len(packages),
        "packages": packages[:20],
        "truncated": len(packages) > 20
    }, indent=2))


if __name__ == "__main__":
    main()
