# convention-ignore-file PY003
"""
Script to compute SHA256 checksums of binaries in assets/ directory
and update manifest.json for clipclop-assets releases.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
MANIFEST_PATH = BASE_DIR / "manifest.json"


def compute_sha256(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def update_manifest(tag: str, owner_repo: str = "themasfebrianto/clipclop-assets"):
    if not MANIFEST_PATH.exists():
        print(f"Error: {MANIFEST_PATH} not found.")
        return

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest["version"] = tag.lstrip("v")
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()

    assets = manifest.get("assets", {})
    for asset_key, asset_data in assets.items():
        filename = asset_data.get("filename")
        if filename:
            asset_file = ASSETS_DIR / filename
            if asset_file.is_file():
                sha256 = compute_sha256(asset_file)
                asset_data["sha256"] = sha256
                size_bytes = asset_file.stat().st_size
                asset_data["size_bytes"] = size_bytes
                asset_data["url"] = f"https://github.com/{owner_repo}/releases/download/{tag}/{filename}"
                print(f"[OK] Processed '{asset_key}' ({filename}): SHA256={sha256[:12]}..., Size={size_bytes} bytes")
            else:
                print(f"[WARNING] File '{filename}' for asset '{asset_key}' not found in {ASSETS_DIR}")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n[SUCCESS] Updated {MANIFEST_PATH} for release tag {tag}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update manifest.json checksums for release")
    parser.add_argument("--tag", required=True, help="Release tag (e.g. v1.0.4)")
    parser.add_argument("--repo", default="themasfebrianto/clipclop-assets", help="GitHub owner/repo")
    args = parser.parse_args()

    update_manifest(tag=args.tag, owner_repo=args.repo)
