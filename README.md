# clipclop-assets

Unified Immutable Asset CDN Repository for **clipclop**.

This repository hosts pre-packaged, isolated portable binary dependencies for Windows (`ffmpeg`, `node`, `yt-dlp`) and AI models (`whisper`, `yolo`) used by clipclop.

---

## 📁 Repository Structure

```
clipclop-assets/
├── .github/
│   └── workflows/
│       └── release-assets.yml   # Automatic GitHub Release packager
├── assets/
│   ├── ffmpeg-v7.1-win64.zip
│   ├── node-v24.5.0-win-x64.zip
│   └── yt-dlp-2026.06.28.exe
├── manifest.json                 # Single source of truth for versions & SHA256 checksums
├── generate_manifest.py          # Automatic SHA256 manifest generator script
└── README.md
```

---

## 🚀 How to Add or Update an Asset

1. Place the new binary or ZIP file into the `assets/` directory (e.g. `assets/ffmpeg-v7.1-win64.zip`).
2. Run the manifest generator:
   ```bash
   python generate_manifest.py --tag v1.0.4
   ```
3. Commit and push the updated `manifest.json`:
   ```bash
   git add manifest.json
   git commit -m "feat: update assets manifest for release v1.0.4"
   git tag v1.0.4
   git push origin main --tags
   ```
4. GitHub Actions will automatically publish the files in `assets/` and `manifest.json` to GitHub Release `v1.0.4`.

---

## 🔒 Security & Integrity Verification

Every binary distributed via this repository is hashed with **SHA256**. The clipclop desktop client verifies `manifest.json` and the SHA256 checksum of each asset upon download and extraction before executing any binary.
