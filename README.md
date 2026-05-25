# My Icon Generator

A collection of Python scripts to generate modern, high-quality icons and animations using radial-conical hybrid gradients.

## Features

- **Static Icon Generation**: Create icons in `.ico`, `.png`, and `.jpg` formats with customizable sizes.
- **Animated Icon Reveal**: Generate an animated `.webp` with a smooth, eased reveal effect.
- **Modern Aesthetic**: Uses a hybrid gradient approach to create a clean, contemporary look.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd my-icon
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Generating Static Icons

Run `create_ico.py` to generate static icons. You can specify the formats (ico, png, jpeg) when prompted.

```bash
python create_ico.py
```

### 2. Generating Animated Reveal

Run `create_animation.py` to create a WebP animation of the icon being revealed. You can specify the duration and initial tilt.

```bash
python create_animation.py
```

## Configuration

You can modify the `MODERN_COLORS` dictionary in both scripts to change the target colors. Default settings include:

- `CANVAS_SIZE`: 1024x1024
- `FPS`: 60 (for animation)
- `DEFAULT_MARGIN`: 64 pixels

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
