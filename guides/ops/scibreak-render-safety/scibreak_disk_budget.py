"""Shared collection floor; cached streaming and historical archives stay intact."""
import argparse
import fcntl
from functools import wraps
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
MIN_FREE_BYTES = 11 * 1024 ** 3 // 2  # 5.5 GiB, above emergency reserve.


def collection_allowed(root=ROOT):
    return shutil.disk_usage(root).free >= MIN_FREE_BYTES


def acquire_lock(name, root=ROOT):
    handle = (Path(root) / ('.collector-' + name + '.lock')).open('a')
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        return None
    return handle


def single_collector(name):
    def decorate(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            handle = acquire_lock(name)
            if handle is None:
                return None
            try:
                return function(*args, **kwargs)
            finally:
                handle.close()
        return wrapped
    return decorate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.parse_args()
    free = shutil.disk_usage(ROOT).free
    print(json.dumps({'collection_allowed': free >= MIN_FREE_BYTES,
                      'free_bytes': free, 'minimum_bytes': MIN_FREE_BYTES}))
    return 0 if free >= MIN_FREE_BYTES else 75


if __name__ == '__main__':
    sys.exit(main())
