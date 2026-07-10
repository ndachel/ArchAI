#!/usr/bin/env python3

import json
import platform
import subprocess


def get_gpu():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    return "unknown"


def get_os():
    try:
        with open("/etc/os-release") as f:
            data = {}
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    data[key] = value.strip('"')
            return data.get("PRETTY_NAME", "unknown")
    except Exception:
        return "unknown"

def get_cpu():
    try:
        result = subprocess.run(
            ["lscpu"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        for line in result.stdout.splitlines():
            if line.startswith("Model name:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass

    return "unknown"

info = {
    "os": get_os(),
    "kernel": platform.release(),
    "architecture": platform.machine(),
    "cpu": get_cpu(),
    "gpu": get_gpu(),
}

print(json.dumps(info, indent=2))
