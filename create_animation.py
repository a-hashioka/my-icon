import math
from PIL import Image

# Configuration (Same as create_ico.py)
CANVAS_SIZE = (1024, 1024)
DEFAULT_MARGIN = 64
BACKGROUND_WHITE = (255, 255, 255)
MODERN_COLORS = {"black": (0, 0, 0)}

# Default Animation Configuration
FPS = 30
DEFAULT_DURATION_SEC = 0.5
INITIAL_TILT_DEG = 30  # Matches create_ico.py default
ROTATION_TOTAL = 180  # Total rotation over the entire duration (degrees)


def interpolate_rgb(c1, c2, ratio):
    """Interpolates between two RGB tuples."""
    return tuple(int(a + (b - a) * ratio) for a, b in zip(c1, c2))


def ease_out_cubic(t):
    """Cubic ease-out: starts fast, ends slow."""
    return 1 - pow(1 - t, 3)


class IconAnimationGenerator:
    def __init__(self, size=CANVAS_SIZE, margin=DEFAULT_MARGIN):
        self.width, self.height = size
        self.margin = margin
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.max_radius = (min(size) / 2) - margin

    def generate_full_gradient(self, target_color, initial_tilt_deg):
        """Generates the final state icon gradient (static)."""
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        pixels = img.load()
        rotation_rad = math.radians(initial_tilt_deg)

        for y in range(self.height):
            dy = y - (self.center_y - 0.5)
            dy_sq = dy**2
            for x in range(self.width):
                dx = x - (self.center_x - 0.5)
                dist = math.sqrt(dx**2 + dy_sq)

                if dist <= self.max_radius:
                    angle_rad = (math.atan2(dx, -dy) - rotation_rad) % (2 * math.pi)
                    angle_ratio = (angle_rad % math.pi) / math.pi
                    dist_ratio = (dist / self.max_radius) ** 2
                    mix_ratio = dist_ratio * angle_ratio
                    rgb = interpolate_rgb(BACKGROUND_WHITE, target_color, mix_ratio)
                    pixels[x, y] = (*rgb, 255)
        return img

    def generate_white_circle(self):
        """Generates a plain white circle on transparent background."""
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        pixels = img.load()
        for y in range(self.height):
            dy = y - (self.center_y - 0.5)
            dy_sq = dy**2
            for x in range(self.width):
                dx = x - (self.center_x - 0.5)
                if math.sqrt(dx**2 + dy_sq) <= self.max_radius:
                    pixels[x, y] = (*BACKGROUND_WHITE, 255)
        return img

    def create_animation(
        self, target_color, output_filename, duration_sec, initial_tilt_deg
    ):
        """Creates an animated WebP with an eased reveal effect."""
        total_frames = int(FPS * duration_sec)

        print("Generating base images...")
        full_img = self.generate_full_gradient(target_color, initial_tilt_deg)
        white_img = self.generate_white_circle()

        rotation_rad = math.radians(initial_tilt_deg)
        frames = []

        # Precompute relative angles for all pixels inside the circle
        print("Precomputing geometry...")
        angles = []
        for y in range(self.height):
            dy = y - (self.center_y - 0.5)
            dy_sq = dy**2
            row_angles = []
            for x in range(self.width):
                dx = x - (self.center_x - 0.5)
                dist_sq = dx**2 + dy_sq
                if dist_sq <= self.max_radius**2:
                    angle_deg = math.degrees(
                        (math.atan2(dx, -dy) - rotation_rad) % (2 * math.pi)
                    )
                    row_angles.append(angle_deg % 180)
                else:
                    row_angles.append(None)
            angles.append(row_angles)

        print(f"Generating {total_frames} frames (with Ease-Out speed)...")
        for i in range(total_frames):
            # Linear time progress (0.0 to 1.0)
            t = i / (total_frames - 1) if total_frames > 1 else 1.0

            # Eased progress (start fast, slow down)
            eased_t = ease_out_cubic(t)

            reveal_limit_deg = eased_t * 180

            mask = Image.new("L", (self.width, self.height), 0)
            mask_pixels = mask.load()

            for y in range(self.height):
                row = angles[y]
                for x in range(self.width):
                    val = row[x]
                    if val is not None and val <= reveal_limit_deg:
                        mask_pixels[x, y] = 255

            frame = Image.composite(full_img, white_img, mask)
            frames.append(frame)

        webp_path = f"{output_filename}.webp"
        frames[0].save(
            webp_path,
            save_all=True,
            append_images=frames[1:],
            duration=int(1000 / FPS),
            loop=1,
            quality=90,
            method=6,
        )
        print(f"Saved: {webp_path}")


def main():
    generator = IconAnimationGenerator()

    color_name = "black"
    target_color = MODERN_COLORS[color_name]

    print(f"--- Eased Icon Reveal Animation Generator ---")

    try:
        duration_input = input(
            f"Enter total duration in seconds [default: {DEFAULT_DURATION_SEC}]: "
        ).strip()
        duration_sec = float(duration_input) if duration_input else DEFAULT_DURATION_SEC

        tilt_input = input(
            f"Enter initial tilt in degrees [default: {INITIAL_TILT_DEG}]: "
        ).strip()
        initial_tilt_deg = float(tilt_input) if tilt_input else INITIAL_TILT_DEG
    except ValueError:
        print("Invalid input. Using defaults.")
        duration_sec = DEFAULT_DURATION_SEC
        initial_tilt_deg = INITIAL_TILT_DEG

    print(f"\nSettings:")
    print(f"- Color: {color_name}")
    print(f"- Total Duration: {duration_sec}s")
    print(f"- Initial Tilt: {initial_tilt_deg} deg")
    print(f"- Speed: Ease-Out (Fast start, soft landing)")

    generator.create_animation(target_color, "icon", duration_sec, initial_tilt_deg)

    print("\nDone!")


if __name__ == "__main__":
    main()
