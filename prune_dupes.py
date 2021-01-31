#!/usr/bin/env python3

import json
import argparse
import os

parser = argparse.ArgumentParser(description="Duplicate Prune Script")
parser.add_argument("--dupereport", help="Path to duplicates report", metavar="PATH", required=True)
parser.add_argument("--keep", help="Path to keep (can be specified multiple times)", metavar="PATH",
                    action="append", required=True)
parser.add_argument("--prune", help="Path to prune (can be specified multiple times)", metavar="PATH",
                    action="append", required=True)
parser.add_argument('--delete', help="Proceed with deleting duplicates", action='store_true')

args = parser.parse_args()

def main():
    with open(args.dupereport) as f:
        duplicates = json.load(f)
    process_duplicates(duplicates)

def process_duplicates(duplicates_list):
    for key, duplicates in duplicates_list.items():
        remove_duplicates(duplicates)

def remove_duplicates(duplicates):
    if not duplicates_includes_a_keep_path(duplicates):
        print("Skipping duplicates batch, no copies in keep paths")
        return
    for path in duplicates:
        if should_delete_file(path):
            print(path)
            os.remove(path)


def should_delete_file(path):
    if path_is_a_keep_path(path):
        print(f"Skipping file (File is in keep paths): {path}")
        return False
    if not path_is_a_prune_path(path):
        print(f"Skipping file (File not in prune paths): {path}")
        return False
    if not args.delete:
        print(f"Delete disabled, skipping {path}")
        return False
    if not os.path.isfile(path):
        print(f"Skipping file (File not found): {path}")
        return False
    return True


def path_is_a_prune_path(path):
    return path_contains_prefix(path, args.prune)

def path_is_a_keep_path(path):
    return path_contains_prefix(path, args.keep)

def path_contains_prefix(path, prefixes):
    for prefix in prefixes:
        if path.startswith(prefix):
            return True
    return False

def duplicates_includes_a_keep_path(duplicates):
    for path in duplicates:
        if path_is_a_keep_path(path):
            return True
    return False

if __name__ == '__main__':
    main()
