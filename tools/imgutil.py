"""Image size from the file header, standard library only (PNG, JPEG, GIF)."""
import struct


def image_size(path):
    """(width, height) read from a PNG/JPEG/GIF header using only the standard library."""
    with open(path, 'rb') as f:
        head = f.read(32)
        if head[:6] in (b'GIF87a', b'GIF89a'):
            return struct.unpack('<HH', head[6:10])
        if head[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', head[16:24])
        f.seek(2)
        while True:
            b = f.read(1)
            while b and b != b'\xff': b = f.read(1)
            while b == b'\xff': b = f.read(1)
            if not b: break
            m = b[0]
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7: continue
            seg = f.read(2)
            if len(seg) < 2: break
            n = struct.unpack('>H', seg)[0]
            if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack('>HH', f.read(5)[1:5])
                return w, h
            f.seek(n - 2, 1)
    raise ValueError(path)


