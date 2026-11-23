"""Flatten screenshot with opaque redaction rectangles; requires Pillow.

Usage:
  python tools/redact_screenshot.py input.png safe.png --box 0.10,0.10,0.60,0.25 --box 0.05,0.70,0.95,0.95

Boxes are fractions of the image dimensions, each between 0 and 1. The script
covers chosen regions with opaque solid fill (not blur). Review all content.
"""
import argparse
from pathlib import Path

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('input');a.add_argument('output');a.add_argument('--box',action='append',required=True,help='relative x1,y1,x2,y2 0..1')
    a.add_argument('--color',default='#111111')
    args=a.parse_args()
    try:
        from PIL import Image,ImageDraw
    except ImportError:
        raise SystemExit('Install Pillow: python -m pip install Pillow')
    src=Path(args.input).resolve();dst=Path(args.output).resolve()
    if src==dst:raise SystemExit('Input and output must differ')
    with Image.open(src) as original:
        # Fresh image strips source metadata by default.
        im=Image.new('RGB',original.size)
        im.paste(original.convert('RGB'))
    draw=ImageDraw.Draw(im)
    w,h=im.size
    for box in args.box:
        vals=[float(t) for t in box.split(',')]
        if len(vals)!=4 or not all(0<=v<=1 for v in vals) or vals[0]>=vals[2] or vals[1]>=vals[3]:
            raise SystemExit(f'Invalid box: {box}')
        x1,y1,x2,y2=vals
        draw.rectangle((int(x1*w),int(y1*h),int(x2*w),int(y2*h)),fill=args.color)
    dst.parent.mkdir(parents=True,exist_ok=True)
    im.save(dst,format='PNG')
    print(f'Created {dst}; visual review is required before publication.')

if __name__=='__main__':main()
