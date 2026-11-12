#!/usr/bin/env python3
"""Build gallery.json from project media folders. No external dependencies."""
from pathlib import Path
import json
from urllib.parse import quote

root = Path(__file__).resolve().parent
projects = ('crosskart', 'biomechanics', 'phillips', 'bechtel', 'printing', 'motorcycle', 'f100-restoration', 'f100-crown-vic', 'yamaha-gp1300r', 'dune-buggy', 'audi-s4')
images = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif'}
videos = {'.mp4', '.webm', '.mov'}  # MP4 (H.264) recommended for browsers
manifest = {}
for project in projects:
    directory = root / 'assets' / project
    entries = []
    for file in sorted(directory.iterdir(), key=lambda p: p.name.lower()) if directory.exists() else []:
        if not file.is_file() or file.suffix.lower() not in images | videos:
            continue
        entries.append({
            'src': '/'.join(quote(part) for part in file.relative_to(root).parts),
            'type': 'video' if file.suffix.lower() in videos else 'image',
            'caption': file.stem.replace('_', ' ').replace('-', ' ').strip(),
        })
    manifest[project] = entries
(root / 'gallery.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Updated gallery.json:', sum(map(len, manifest.values())), 'additional files')
