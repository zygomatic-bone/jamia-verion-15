"""Copy the recovered original photographs, PDFs into public/.

Usage:  python3 tools/import_recovered_assets.py /path/to/backup/homedir/public_html

The original backup is NOT part of the deployable site (and must never be copied into public/ as a whole: it also holds
hosting configuration and CGI folders). Only the files listed in tools/recovery_assets.py are copied. Re-running is safe.

Images are copied byte-for-byte. The exception is CMYK JPEGs (printing colour mode, rendered with wrong colours by many
phones and browsers): those are converted to RGB and re-saved at quality 92.
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recovery_assets as RA

PUB = Path(__file__).resolve().parent.parent / 'public'


def main(src_root):
    src_root = Path(src_root)
    if not (src_root / 'homeimages').is_dir():
        sys.exit(f'{src_root} does not look like the original public_html (no homeimages/ folder)')
    converted = copied = 0
    for key, (src, dest, alt, cap) in RA.IMAGES.items():
        s, d = src_root / src, PUB / RA.R / dest
        d.parent.mkdir(parents=True, exist_ok=True)
        if not s.is_file():
            sys.exit(f'missing source for {key}: {src}')
        done = False
        if s.suffix.lower() in ('.jpg', '.jpeg'):
            from PIL import Image
            im = Image.open(s)
            if im.mode == 'CMYK':
                im.convert('RGB').save(d, 'JPEG', quality=92, optimize=True)
                converted += 1
                done = True
        if not done:
            shutil.copyfile(s, d)
            copied += 1
    for key, (src, dest, title, desc) in RA.DOCUMENTS.items():
        d = PUB / RA.DOC / dest
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_root / src, d)
    print(f'images copied unchanged: {copied}; CMYK converted to RGB: {converted}; documents: {len(RA.DOCUMENTS)}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else sys.exit(__doc__))
