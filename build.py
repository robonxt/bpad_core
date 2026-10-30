#!/usr/bin/env python3
"""
Build script for bpad_core.
Creates release zips for distribution via Arduino Board Manager.

Usage:
    python build.py
"""

import os
import sys
import hashlib
import zipfile

VERSIONS = ["2.0.17", "3.3.5"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RELEASE_DIR = os.path.join(SCRIPT_DIR, "release")


def compute_sha256(filepath):
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def create_zip(source_dir, zip_path):
    """Create a zip file from a directory."""
    print(f"Creating zip: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, os.path.dirname(source_dir))
                zf.write(file_path, arc_name)
    print(f"  Created: {zip_path}")


def build_version(version):
    print("=" * 60)
    print(f"Building bpad core for ESP32 v{version}")
    print("=" * 60)

    esp32_dir = os.path.join(SCRIPT_DIR, f"esp32_v{version.replace('.', '_')}")
    if not os.path.exists(esp32_dir):
        print(f"ERROR: {esp32_dir} not found!")
        print("Run 'python setup.py' first.")
        sys.exit(1)

    zip_filename = f"bpad_core-{version}.zip"
    zip_path = os.path.join(RELEASE_DIR, zip_filename)

    create_zip(esp32_dir, zip_path)

    file_sha = compute_sha256(zip_path)
    file_size = os.path.getsize(zip_path)
    file_size_mb = file_size / (1024 * 1024)

    print()
    print(f"  File:     {zip_filename}")
    print(f"  Size:     {file_size} bytes ({file_size_mb:.1f} MB)")
    print(f"  Checksum: SHA-256:{file_sha}")
    print()
    return zip_filename, file_sha, file_size


def main():
    target_versions = [v for v in sys.argv[1:] if not v.startswith("-")]
    if not target_versions:
        target_versions = ["3.3.5"]
    elif "all" in target_versions:
        target_versions = VERSIONS

    print("=" * 60)
    print(f"bpad core - Build Script (Target: {', '.join(target_versions)})")
    print("=" * 60)
    print()

    os.makedirs(RELEASE_DIR, exist_ok=True)
    
    results = []
    for v in target_versions:
        if v not in VERSIONS:
            print(f"WARNING: Unknown version '{v}'. Known versions: {VERSIONS}")
            continue
        res = build_version(v)
        results.append((v, res))

    print("=" * 60)
    print("Build complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Update package_bpad_index.json with the following values:")
    for v, (zip_filename, file_sha, file_size) in results:
        print(f"  --- Version {v} ---")
        print(f'      "version": "{v}"')
        print(f'      "url": "<your-github-release-url>/{zip_filename}"')
        print(f'      "archiveFileName": "{zip_filename}"')
        print(f'      "checksum": "SHA-256:{file_sha}"')
        print(f'      "size": "{file_size}"')
        print()


if __name__ == "__main__":
    main()
