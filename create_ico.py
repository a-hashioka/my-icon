import math
from PIL import Image, ImageFilter

# Configuration
CANVAS_SIZE = (1024, 1024)
ICO_STANDARD_SIZES = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (96, 96),
    (128, 128),
    (256, 256),
]
DEFAULT_MARGIN = 64
BACKGROUND_WHITE = (255, 255, 255)

# Modern Color Palette
MODERN_COLORS = {
    "black": (0, 0, 0)
    # "deep_ocean": (12, 36, 58),
    # "soft_teal": (45, 150, 150),
    # "vivid_coral": (255, 111, 97),
    # "royal_purple": (103, 58, 183),
    # "slate_gray": (52, 73, 94),
    # "forest_green": (34, 139, 34),
    # "midnight": (10, 10, 10),
    # "cyber_neon": (0, 255, 255),
    # "electric_indigo": (99, 102, 241),
    # "dusty_rose": (180, 120, 130),
    # "sunset_orange": (255, 77, 0),
    # "mint_fresh": (0, 200, 150),
    # "golden_hour": (255, 190, 0),
    # "berry_smoothie": (180, 50, 100),
}


def interpolate_rgb(c1, c2, ratio):
    """Interpolates between two RGB tuples."""
    return tuple(int(a + (b - a) * ratio) for a, b in zip(c1, c2))


class IconGenerator:
    def __init__(self, size=CANVAS_SIZE, margin=DEFAULT_MARGIN):
        self.width, self.height = size
        self.margin = margin
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.max_radius = (min(size) / 2) - margin

    def generate_gradient(self, target_color, rotation_deg=30):
        """Generates a radial-conical hybrid gradient."""
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        pixels = img.load()
        rotation_rad = math.radians(rotation_deg)

        for y in range(self.height):
            # Precompute y-related values
            dy = y - (self.center_y - 0.5)
            dy_sq = dy**2

            for x in range(self.width):
                dx = x - (self.center_x - 0.5)
                dist = math.sqrt(dx**2 + dy_sq)

                if dist <= self.max_radius:
                    # Angle calculation
                    angle = (math.atan2(dx, -dy) - rotation_rad) % (2 * math.pi)
                    angle_ratio = (angle % math.pi) / math.pi

                    # Gradient blending
                    dist_ratio = (dist / self.max_radius) ** 2
                    mix_ratio = dist_ratio * angle_ratio

                    rgb = interpolate_rgb(BACKGROUND_WHITE, target_color, mix_ratio)
                    pixels[x, y] = (*rgb, 255)

        return img

    def apply_effects(self, image, blur_radius=0):
        """Applies post-processing effects."""
        if blur_radius > 0:
            return image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        return image

    def save(self, image, base_filename, formats=["ico", "png"]):
        """Saves the image in multiple formats."""
        for fmt in formats:
            fmt = fmt.lower().strip(".")
            ext = "jpg" if fmt == "jpeg" else fmt
            output_path = f"{base_filename}.{ext}"

            try:
                if fmt == "ico":
                    image.save(output_path, format="ICO", sizes=ICO_STANDARD_SIZES)
                elif fmt in ["jpg", "jpeg"]:
                    # JPEG doesn't support alpha; blend with white background
                    bg = Image.new("RGB", image.size, BACKGROUND_WHITE)
                    bg.paste(image, mask=image.split()[3])
                    bg.save(output_path, format="JPEG", quality=95)
                else:
                    image.save(output_path, format=fmt.upper())
                print(f"Saved: {output_path}")
            except Exception as e:
                print(f"Failed to save {fmt}: {e}")


def main():
    generator = IconGenerator()

    print("--- Icon Generator ---")
    print("Available formats: ico, png, jpeg")
    user_input = input(
        "Enter formats to generate (comma separated, e.g., 'ico, png') [default: ico]: "
    ).strip()

    if not user_input:
        formats_to_generate = ["ico"]
    else:
        formats_to_generate = [f.strip().lower() for f in user_input.split(",")]

    print(f"Selected formats: {', '.join(formats_to_generate)}\n")

    for name, color in MODERN_COLORS.items():
        print(f"Processing color: {name}...")
        img = generator.generate_gradient(target_color=color)
        img = generator.apply_effects(img, blur_radius=0)

        base_name = f"icon_{name}"
        generator.save(img, base_name, formats=formats_to_generate)

    print("\nDone!")


if __name__ == "__main__":
    main()
