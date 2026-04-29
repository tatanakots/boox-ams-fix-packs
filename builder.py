import os
import sys
import re
import zipfile
import argparse
import tempfile
import shutil
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Build Magisk module zip")
    parser.add_argument("services_jar", help="Path to services.jar file")
    parser.add_argument("device_name", help="Device name")
    parser.add_argument("booxos_version", help="BOOX OS version")
    parser.add_argument(
        "--src", default="src", help="Source folder path (default: ./src)"
    )
    parser.add_argument("--output", help="Output zip path")
    return parser.parse_args()


def preprocess_content(content, device_name, booxos_version):
    pattern = re.compile(r"\{\{\s*DEVICE_NAME\s*\}\}")
    content = pattern.sub(device_name, content)
    pattern = re.compile(r"\{\{\s*BOOXOS_VERSION\s*\}\}")
    content = pattern.sub(booxos_version, content)
    return content


def preprocess_file(src_path, dest_path, device_name, booxos_version):
    with open(src_path, "rb") as f:
        content = f.read()
    try:
        text = content.decode("utf-8")
        text = preprocess_content(text, device_name, booxos_version)
        content = text.encode("utf-8")
    except UnicodeDecodeError:
        pass
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(content)


def build_zip(src_dir, services_jar, device_name, booxos_version, output_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_src = os.path.join(tmpdir, "src")
        os.makedirs(tmp_src)

        for root, dirs, files in os.walk(src_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_dir)
                dest_path = os.path.join(tmp_src, rel_path)
                preprocess_file(src_path, dest_path, device_name, booxos_version)

        services_dest = os.path.join(tmpdir, "system", "framework")
        os.makedirs(services_dest, exist_ok=True)
        shutil.copy2(services_jar, os.path.join(services_dest, "services.jar"))

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(tmp_src):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, tmp_src)
                    zf.write(file_path, arcname)
            zf.write(
                os.path.join(services_dest, "services.jar"),
                "system/framework/services.jar",
            )

        print(f"Built: {output_path}")


def main():
    args = parse_args()

    src_dir = args.src
    if not os.path.isdir(src_dir):
        print(f"Error: src folder not found: {src_dir}")
        sys.exit(1)

    services_jar = args.services_jar
    if not os.path.isfile(services_jar):
        print(f"Error: services.jar not found: {services_jar}")
        sys.exit(1)

    device_name = args.device_name
    booxos_version = args.booxos_version

    output_path = args.output
    if not output_path:
        output_path = f"boox-ams-fix-{device_name}-{booxos_version}-1.0.zip"

    build_zip(src_dir, services_jar, device_name, booxos_version, output_path)


if __name__ == "__main__":
    main()
