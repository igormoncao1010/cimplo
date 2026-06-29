from pathlib import Path
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "og-image-source.png"
OUTPUT = ROOT / "assets" / "og-image.png"
TARGET_SIZE = (1200, 630)


def cover_background(source):
    target_w, target_h = TARGET_SIZE
    scale = max(target_w / source.width, target_h / source.height)
    size = (round(source.width * scale), round(source.height * scale))
    bg = source.resize(size, Image.LANCZOS)

    left = (bg.width - target_w) // 2
    top = (bg.height - target_h) // 2
    bg = bg.crop((left, top, left + target_w, top + target_h))
    bg = bg.filter(ImageFilter.GaussianBlur(18))

    overlay = Image.new("RGBA", TARGET_SIZE, (255, 248, 245, 92))
    bg = bg.convert("RGBA")
    bg.alpha_composite(overlay)
    return bg


def contain_foreground(source):
    target_w, target_h = TARGET_SIZE
    scale = min(target_w / source.width, target_h / source.height)
    size = (round(source.width * scale), round(source.height * scale))
    fg = source.resize(size, Image.LANCZOS).convert("RGBA")

    canvas = cover_background(source)
    left = (target_w - fg.width) // 2
    top = (target_h - fg.height) // 2
    canvas.alpha_composite(fg, (left, top))
    return canvas.convert("RGB")


def main():
    source = Image.open(SOURCE).convert("RGB")
    result = contain_foreground(source)
    result.save(OUTPUT, quality=95)
    print(OUTPUT)


if __name__ == "__main__":
    main()
