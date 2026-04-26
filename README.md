# bpad Core

The **bpad core** repository generates custom Arduino IDE Board Manager packages for bpad hardware. It allows you to maintain custom board definitions, pinouts, and partition schemes independent of the upstream ESP32 Arduino cores.

Currently, this repository is configured to build packages for:
- **ESP32 Arduino Core v2.0.17**
- **ESP32 Arduino Core v3.3.5**

It includes support for the following boards:
- `bpad proto1` (4MB Flash)
- `bpad proto2 (2vib)` (16MB Flash)
- `bpad proto3 (4vib)` (16MB Flash)

## Quick Install (Arduino IDE)

1. Open **File → Preferences** in the Arduino IDE.
2. Add this URL to **Additional Board Manager URLs**:
   ```
   https://raw.githubusercontent.com/robonxt/bpad_core/main/package_bpad_index.json
   ```
3. Open **Tools → Board → Boards Manager**.
4. Search for **"bpad"** and install the latest version.
5. Select your board from **Tools → Board → bpad core → [Your Board]**.
6. (Optional) You can use the **Version** dropdown in the Boards Manager to switch between ESP32 v2.0.17 and v3.3.5.

## Repository Structure

To keep this repository lightweight, the actual ESP32 Arduino Core source files are **not** stored here. Instead, we use python scripts to download the cores from Espressif and inject our custom modifications.

- **`custom_files/`**: The source of truth for all bpad-specific configurations.
  - `boards.txt`: The master board definitions.
  - `variants/`: Pinout definitions (`pins_arduino.h`) for each board.
  - `partitions/`: Custom partition scheme files (e.g., `bpad_16MB_4GB.csv`).
- **`setup.py`**: Downloads the target ESP32 core versions, extracts them, and injects the contents of `custom_files/`.
- **`build.py`**: Packages the patched cores into distribution-ready `.zip` files.
- **`package_bpad_index.json`**: The Arduino Board Manager index file that tells the IDE how to download and install the cores.

---

## How to Build a Release

If you've made changes to the board definitions or variants, you need to build a new release.

1. Run the setup script to download the base ESP32 cores and inject your custom files:
   ```bash
   python setup.py
   ```
2. Run the build script to generate the distribution zip files:
   ```bash
   python build.py
   ```
3. The script will output the new file sizes and SHA-256 checksums. Copy these values into `package_bpad_index.json`.
4. Upload the generated `.zip` files (found in the `release/` folder) to your GitHub Releases.
5. Commit and push the updated `package_bpad_index.json` to the `main` branch.

---

## Maintenance Guide

### How to Add a New Board

1. **Update `boards.txt`**: Open `custom_files/boards.txt` and add a new section for your board (e.g., `bpad_proto4`). Define its flash size, partition scheme, and point it to a new variant.
2. **Create a Variant**: Duplicate an existing folder in `custom_files/variants/` (e.g., `bpad_proto3`) and rename it to match the variant name you defined in `boards.txt`. Edit `pins_arduino.h` inside it to reflect the new pinout.
3. **Add Partitions (Optional)**: If your board uses a new custom partition scheme, add the `.csv` file to `custom_files/partitions/`.
4. Run `setup.py` and `build.py` to generate the new release.

### How to Upgrade or Add an ESP32 Core Version

If Espressif releases a new core version (e.g., `3.5.0` or `4.0.0`) and you want to support it:

1. **Update Python Scripts**: 
   Open `setup.py` and `build.py` and add the new version string to the `VERSIONS` list at the top of the scripts:
   ```python
   VERSIONS = ["2.0.17", "3.3.5", "4.0.0"]
   ```
2. **Update `package_bpad_index.json`**: 
   You must add a new platform block to the JSON file for the new version.
   - Duplicate the existing `3.3.5` platform block.
   - Change the `"version"` field to `"4.0.0"`.
   - Update the `"url"` and `"archiveFileName"` to point to the new `bpad_core-4.0.0.zip`.
   - **Crucially**: Ensure the `toolsDependencies` list matches the exact toolchain versions required by the new core. You can find these tool dependencies by inspecting Espressif's official `package_esp32_index.json` for that version.
3. Run `setup.py` and `build.py` to generate the new zip, update the checksums in the JSON, and deploy your release.


Credits: @robonxt & Antigravity
