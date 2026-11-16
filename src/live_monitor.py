"""Milestone 6A: follow newly appended synthetic authentication events."""
import os
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "sample_logs" / "live_test.log"
POLL_INTERVAL = 0.5


def open_shared_log(file_path):
    """Open read-only with explicit sharing on Windows."""
    if sys.platform == "win32":
        import ctypes
        import msvcrt
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        create_file = kernel32.CreateFileW
        create_file.argtypes = [
            wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
            wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD,
            wintypes.HANDLE,
        ]
        create_file.restype = wintypes.HANDLE
        handle = create_file(
            str(Path(file_path).resolve()), 0x80000000,
            0x1 | 0x2 | 0x4, None, 3, 0x80, None,
        )
        if handle == ctypes.c_void_p(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            fd = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
        except Exception:
            kernel32.CloseHandle(handle)
            raise
        return os.fdopen(fd, "r", encoding="utf-8", errors="replace")
    return open(file_path, "r", encoding="utf-8", errors="replace")


def follow_log(file_path, poll_interval=POLL_INTERVAL):
    """Yield new nonempty log lines, starting at EOF."""
    if poll_interval <= 0:
        raise ValueError("Polling interval must be greater than zero.")
    log_path = Path(file_path)
    with open_shared_log(log_path) as log_file:
        log_file.seek(0, os.SEEK_END)
        print(f"[INFO] Monitoring: {log_path}", flush=True)
        while True:
            line = log_file.readline()
            if line:
                event = line.rstrip("\r\n")
                if event:
                    yield event
            else:
                time.sleep(poll_interval)


def main():
    print("=" * 50)
    print("          MEDSECURE LIVE SECURITY MONITOR")
    print("=" * 50)
    print("[INFO] Starting MedSecure monitoring engine...", flush=True)
    print("[INFO] Press Ctrl+C to stop monitoring.", flush=True)
    try:
        for event in follow_log(LOG_FILE):
            print(f"[NEW EVENT] {event}", flush=True)
    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped by user.")
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {LOG_FILE}")
        print("[INFO] Create the test log before starting.")
    except PermissionError:
        print(f"[ERROR] Permission denied: {LOG_FILE}")
    except OSError as error:
        print(f"[ERROR] File monitoring failed: {error}")


if __name__ == "__main__":
    main()
