#!/usr/bin/env python3
"""
Setup script for bpad_core.
Downloads ESP32 Arduino Core versions, extracts them, and applies custom boards and variants.

Usage:
    python setup.py
"""

import os
import sys
import shutil
import urllib.request
import zipfile

VERSIONS = ["2.0.17", "3.3.5"]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CUSTOM_FILES_DIR = os.path.join(SCRIPT_DIR, "custom_files")


def download_file(url, dest):
    """Download a file with progress reporting."""
    print(f"Downloading {url}...")
    print(f"  -> {dest}")

    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(100, downloaded * 100 / total_size)
            mb_down = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            sys.stdout.write(f"\r  Progress: {pct:.1f}% ({mb_down:.1f}/{mb_total:.1f} MB)")
            sys.stdout.flush()

    urllib.request.urlretrieve(url, dest, reporthook=reporthook)
    print("\n  Download complete!")


def setup_version(version):
    print("=" * 60)
    print(f"Setting up bpad core for ESP32 v{version}")
    print("=" * 60)

    zip_url = f"https://github.com/espressif/arduino-esp32/releases/download/{version}/esp32-{version}.zip"
    zip_file = f"esp32-{version}.zip"
    zip_path = os.path.join(SCRIPT_DIR, zip_file)
    esp32_dir = os.path.join(SCRIPT_DIR, f"esp32_v{version.replace('.', '_')}")

    # Step 1: Download
    if not os.path.exists(zip_path):
        download_file(zip_url, zip_path)
    else:
        print(f"Found existing {zip_file}, skipping download.")

    # Step 2: Extract
    print(f"\nExtracting {zip_file}...")
    temp_extract = os.path.join(SCRIPT_DIR, f"_temp_{version}")
    if os.path.exists(temp_extract):
        shutil.rmtree(temp_extract)
        
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(temp_extract)

    # Move extracted files to target directory
    extracted_dir = None
    for d in os.listdir(temp_extract):
        candidate = os.path.join(temp_extract, d)
        if os.path.isdir(candidate):
            extracted_dir = candidate
            break

    if extracted_dir is None:
        print(f"ERROR: Could not find extracted directory for {version}!")
        sys.exit(1)

    if os.path.exists(esp32_dir):
        shutil.rmtree(esp32_dir)

    shutil.move(extracted_dir, esp32_dir)
    shutil.rmtree(temp_extract)
    print(f"  Extracted to: {esp32_dir}")

    # Step 3: Inject custom boards.txt
    print("\nInjecting custom boards.txt...")
    src_boards = os.path.join(CUSTOM_FILES_DIR, "boards.txt")
    dst_boards = os.path.join(esp32_dir, "boards.txt")
    shutil.copy2(src_boards, dst_boards)

    # Step 4: Inject custom variants
    print("Injecting custom variants...")
    src_variants = os.path.join(CUSTOM_FILES_DIR, "variants")
    dst_variants = os.path.join(esp32_dir, "variants")
    for variant in os.listdir(src_variants):
        v_src = os.path.join(src_variants, variant)
        v_dst = os.path.join(dst_variants, variant)
        if os.path.exists(v_dst):
            shutil.rmtree(v_dst)
        shutil.copytree(v_src, v_dst)
        print(f"  Added variant: {variant}")

    # Step 5: Inject custom partitions
    print("Injecting custom partitions...")
    src_partitions = os.path.join(CUSTOM_FILES_DIR, "partitions")
    dst_partitions = os.path.join(esp32_dir, "tools", "partitions")
    if os.path.exists(src_partitions):
        for part in os.listdir(src_partitions):
            p_src = os.path.join(src_partitions, part)
            p_dst = os.path.join(dst_partitions, part)
            shutil.copy2(p_src, p_dst)
            print(f"  Added partition: {part}")

    # Step 6: Patch platform.txt
    print("\nPatching platform.txt...")
    platform_txt = os.path.join(esp32_dir, "platform.txt")
    if os.path.exists(platform_txt):
        with open(platform_txt, 'r') as f:
            content = f.read()
        
        # We rename it and keep the version
        content = content.replace(
            "name=ESP32 Arduino",
            "name=bpad core"
        )
        
        with open(platform_txt, 'w') as f:
            f.write(content)
        print("  Patched name in platform.txt")
    else:
        print("  WARNING: platform.txt not found!")

    print(f"\nSetup for v{version} complete!\n")


def main():
    print("=" * 60)
    print("bpad core - Multi-Version Setup Script")
    print("=" * 60)
    print()

    for v in VERSIONS:
        setup_version(v)

    print("=" * 60)
    print("All setups complete!")
    print("You can now run 'python build.py' to generate the release zips.")
    print("=" * 60)


if __name__ == "__main__":
    main()
