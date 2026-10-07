"""Tile rendered stills into one contact sheet for review."""
import sys
from PIL import Image
out, files = sys.argv[1], sys.argv[2:]
ims = [Image.open(f).resize((540, 960)) for f in files]
cols = min(4, len(ims)); rows = (len(ims) + cols - 1) // cols
W = Image.new('RGB', (540 * cols, 960 * rows), 'white')
for i, im in enumerate(ims): W.paste(im, (540 * (i % cols), 960 * (i // cols)))
W.save(out, quality=88)
