#!/usr/bin/env python3
# Generate PNG icons for PWA using only stdlib
import base64, struct, zlib, os

def make_png(size, bg=(37,99,235), fg=(255,255,255)):
    """Create a simple PNG icon with 'E' letter"""
    w = h = size
    img = []
    cx, cy = w//2, h//2
    r = int(w * 0.42)
    
    for y in range(h):
        row = []
        for x in range(w):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            
            # Circle background
            if dist <= r:
                # Draw stylized "E" letter
                rel_x = (x - cx) / r
                rel_y = (y - cy) / r
                
                # E letter bounds
                lx = rel_x + 0.08  # left edge of E
                
                in_e = False
                if -0.55 < rel_y < 0.55 and -0.12 < rel_x < 0.45:
                    # Vertical bar of E
                    if -0.45 < rel_x < -0.12:
                        in_e = True
                    # Top bar
                    elif 0.38 < rel_y < 0.55 and -0.45 < rel_x < 0.45:
                        in_e = True
                    # Middle bar
                    elif -0.08 < rel_y < 0.08 and -0.45 < rel_x < 0.30:
                        in_e = True
                    # Bottom bar
                    elif -0.55 < rel_y < -0.38 and -0.45 < rel_x < 0.45:
                        in_e = True
                
                if in_e:
                    row.extend(fg)
                else:
                    row.extend(bg)
            else:
                row.extend((255,255,255))
        img.append(row)
    
    # Build PNG
    def png_chunk(tag, data):
        c = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)
    
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    raw = b''
    for row in img:
        raw += b'\x00' + bytes(row)
    
    idat = zlib.compress(raw, 9)
    
    png = b'\x89PNG\r\n\x1a\n'
    png += png_chunk(b'IHDR', ihdr)
    png += png_chunk(b'IDAT', idat)
    png += png_chunk(b'IEND', b'')
    return png

os.makedirs('/home/claude/edudesk', exist_ok=True)

for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
    png = make_png(size)
    with open(f'/home/claude/edudesk/{name}', 'wb') as f:
        f.write(png)
    print(f"Created {name} ({len(png)} bytes)")

print("Icons generated successfully!")
