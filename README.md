# Boox AMS NullPointerException Fix

> Fix Magisk app crash on Boox firmware 4.1+

[![Firmware](https://img.shields.io/badge/Firmware-4.1%2B-orange)]()
[![Magisk](https://img.shields.io/badge/Magisk_Module-v30.6-brightgreen)]()

## Overview

This is a fork of the original [boox-ams-fix](https://github.com/dynamicfire/boox-ams-fix) project, extended to provide Magisk fix packs for **all supported device models and firmware versions**.

Pre-packaged Magisk module downloads are available at:  
**[Releases](https://github.com/tatanakots/boox-ams-fix-packs/releases)**

**Important:** Always download the package that matches your exact device model and firmware version. Packages for different firmware versions are **not interchangeable**.

This repository also hosts a dynamic patcher at [boox-ams-fix-patcher](https://github.com/tatanakots/boox-ams-fix-patcher) for on-device patching.

## Problem

On Boox firmware 4.1+, the Magisk app freezes on the splash screen and never reaches the main UI. Root itself works fine (`su -c id` returns uid=0) — only the management interface is broken.


## Installation

Since the Magisk app cannot open, install via ADB:

```bash
adb push boox-ams-fix-<DEVICE_NAME>-<VERSION>.zip /sdcard/
adb shell su -c 'magisk --install-module /sdcard/boox-ams-fix-<DEVICE_NAME>-<VERSION>.zip'
adb reboot
```

The Magisk app should launch normally after reboot.

## Uninstallation

```bash
adb shell su -c 'rm -rf /data/adb/modules/boox-ams-fix'
adb reboot
```

## Building from Source

Use the included `builder.py` script to build Magisk module packages:

```bash
python builder.py <services.jar_path> <DEVICE_NAME> <BOOXOS_VERSION> [--src <src_folder>] [--output <output_zip>]
```

Example:

```bash
python builder.py ./jar/NoteAir3C/4.1/services.jar NoteAir3C 4.1 --src ./src --output ./boox-ams-fix-NoteAir3C-4.1.zip
```

The script:
1. Scans all files in the src folder
2. Replaces `{{ DEVICE_NAME }}` and `{{ BOOXOS_VERSION }}` placeholders in file contents with provided values
3. Packages `services.jar` into `system/framework/services.jar`
4. Outputs a Magisk-compatible zip file

## Contributing services.jar Files

The `/jar` directory collects `services.jar` files organized by device model and firmware version. If you have a device affected by this bug, your contributions are welcome via PR.

**Note:** Only `services.jar` files from devices affected by this bug should be submitted. Unaffected devices are not included.

## Notes

- Packages are device and firmware specific. Always download the correct version for your device
- If Boox fixes this in a future firmware update, uninstall this module
- May need to be reinstalled after OTA updates

## Related

- [boox-ams-fix-patcher](https://github.com/tatanakots/boox-ams-fix-patcher) — Dynamic on-device patcher
- [boox-p6pro-root](https://github.com/dynamicfire/boox-p6pro-root) — Full root guide for P6 Pro (includes EDL bootloader unlock)

## Credits

- **[dynamicfire/boox-ams-fix](https://github.com/dynamicfire/boox-ams-fix)**
- **[topjohnwu/Magisk](https://github.com/topjohnwu/Magisk)** — Root solution
- **[Kisuke](https://github.com/Kisuke-CZE/Palma_2_Pro-tips#rooting-palma-2-pro)** — Palma 2 Pro root method
