from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "og-image.png"
LOGO = ROOT / "assets" / "cimplo-logo.png"
FONT_REGULAR = Path("C:/Windows/Fonts/arial.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")

W, H = 1200, 630
CORAL = (216, 93, 78)
CORAL_LIGHT = (238, 111, 92)
INK = (41, 47, 47)
MUTED = (89, 97, 96)
WHITE = (255, 255, 255)
CREAM = (255, 241, 236)


def font(path, size):
    return ImageFont.truetype(str(path), size=size)


def rounded_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap_text(draw, text, font_obj, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=font_obj)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_multiline(draw, xy, text, font_obj, fill, max_width, line_gap):
    x, y = xy
    for line in wrap_text(draw, text, font_obj, max_width):
        draw.text((x, y), line, font=font_obj, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font_obj)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def make_gradient():
    img = Image.new("RGB", (W, H), WHITE)
    px = img.load()
    for y in range(H):
        for x in range(W):
            t = (x / W) * 0.35 + (y / H) * 0.65
            r = int(255 * (1 - t) + CREAM[0] * t)
            g = int(253 * (1 - t) + CREAM[1] * t)
            b = int(251 * (1 - t) + CREAM[2] * t)
            px[x, y] = (r, g, b)
    return img.convert("RGBA")


def add_soft_circle(img, center, radius, color, alpha):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius // 3))
    img.alpha_composite(overlay)


def main():
    img = make_gradient()
    add_soft_circle(img, (995, 105), 210, CORAL_LIGHT, 48)
    add_soft_circle(img, (1040, 520), 260, (255, 255, 255), 150)

    draw = ImageDraw.Draw(img)

    logo = Image.open(LOGO).convert("RGBA")
    logo_ratio = 295 / logo.width
    logo = logo.resize((295, int(logo.height * logo_ratio)), Image.LANCZOS)
    img.alpha_composite(logo, (68, 54))

    eyebrow_font = font(FONT_BOLD, 25)
    title_font = font(FONT_BOLD, 72)
    lead_font = font(FONT_REGULAR, 30)
    footer_font = font(FONT_BOLD, 23)
    item_font = font(FONT_BOLD, 28)
    cta_font = font(FONT_BOLD, 27)

    draw.text((72, 196), "ODONTOLOGIA AVANÇADA EM BARBACENA", font=eyebrow_font, fill=CORAL)
    title_y = draw_multiline(
        draw,
        (72, 236),
        "Restaurando sorrisos, elevando a autoestima.",
        title_font,
        INK,
        690,
        4,
    )
    draw_multiline(
        draw,
        (72, title_y + 28),
        "Implantes, protocolos, coroas, harmonização facial, exames e radiografias em uma estrutura completa.",
        lead_font,
        MUTED,
        700,
        8,
    )

    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded_rect(shadow_draw, (796, 92, 1132, 538), 24, (97, 58, 46, 32))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(shadow)

    rounded_rect(draw, (780, 76, 1116, 522), 24, (255, 255, 255, 210), (238, 111, 92, 80), 2)

    items = [
        "Implantes zigomáticos",
        "Protocolos",
        "Hospital do Dente",
        "Exames na Cimplo",
    ]
    y = 140
    for item in items:
        draw.ellipse((818, y + 8, 836, y + 26), fill=CORAL_LIGHT)
        draw.ellipse((813, y + 3, 841, y + 31), outline=(238, 111, 92, 52), width=6)
        draw.text((858, y), item, font=item_font, fill=INK)
        y += 74

    rounded_rect(draw, (824, 410, 1072, 474), 32, CORAL)
    draw.text((872, 426), "Agende sua consulta", font=cta_font, fill=WHITE)

    draw.text((72, 560), "Cimplo Dental Spa | Desde 2006", font=footer_font, fill=(105, 112, 112))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
