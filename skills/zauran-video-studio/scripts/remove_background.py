"""Local photo cutout recipe. Requires rembg[cpu] and Pillow; may download weights."""
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Remove a photo background to a new RGBA PNG.')
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--model', choices=['u2net', 'isnet-general-use', 'birefnet-general'], default='birefnet-general')
    parser.add_argument('--alpha-matting', action='store_true')
    args = parser.parse_args()
    source, target = args.input.resolve(), args.output.resolve()
    if not source.is_file():
        parser.error('Input file does not exist.')
    if target.suffix.lower() != '.png':
        parser.error('Output must be PNG to retain transparency.')
    if source == target or target.exists():
        parser.error('Choose a new output path; existing files are preserved.')
    if not target.parent.is_dir():
        parser.error('Output directory must already exist.')
    try:
        from PIL import Image
        from rembg import new_session, remove
    except ImportError:
        parser.error('Install rembg[cpu] and Pillow in a separate Python environment.')
    try:
        with Image.open(source) as image:
            image.load()
            cutout = remove(image.convert('RGB'), session=new_session(args.model), alpha_matting=args.alpha_matting)
        rgba = cutout.convert('RGBA')
        if rgba.getchannel('A').getextrema() == (255, 255):
            raise ValueError('The returned image is fully opaque; inspect model/input before using it.')
        with target.open('xb') as output:
            rgba.save(output, format='PNG')
    except Exception as error:
        parser.exit(1, f'Background removal failed: {error}\n')
    print(f'Saved {target}; inspect hair, soft edges and translucent surfaces before approval.')


if __name__ == '__main__':
    main()
