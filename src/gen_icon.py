"""Generate VSAnimator icon — DAEMON Tools style: clean circle + symbol."""
from PIL import Image, ImageDraw, ImageFilter
import math

def make_icon():
    sz = 512  # high res base for smooth scaling
    img = Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx, cy = sz // 2, sz // 2
    r = 230  # circle radius

    # === Main circle — dark golden gradient effect ===
    # Outer ring (dark gold border)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(180, 125, 15))
    # Inner fill — rich amber/gold
    ri = r - 8
    d.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=(220, 160, 30))
    # Highlight arc (top lighter area for 3D feel)
    ri2 = r - 12
    d.ellipse([cx-ri2, cy-ri2-6, cx+ri2, cy+ri2-6], fill=(240, 185, 45))
    # Re-draw bottom half to create gradient feel
    d.pieslice([cx-ri2, cy-20, cx+ri2, cy+ri2+20], 15, 165, fill=(200, 140, 25))

    # === Central symbol: ANVIL silhouette (simple, bold, white) ===
    # Scale factor
    s = sz / 256

    # Anvil - clean silhouette style like DT's lightning bolt
    col = (255, 250, 240)  # warm white
    col2 = (250, 245, 230, 220)  # slightly transparent

    # Anvil top surface
    ax, ay = cx, cy - int(15*s)  # center of anvil
    # Horn (left point)
    horn_l = (ax - int(95*s), ay - int(8*s))
    horn_lb = (ax - int(85*s), ay + int(8*s))
    # Face left
    face_l = (ax - int(70*s), ay - int(22*s))
    face_lb = (ax - int(70*s), ay + int(8*s))
    # Face right
    face_r = (ax + int(70*s), ay - int(22*s))
    face_rb = (ax + int(70*s), ay + int(8*s))
    # Heel (right step)
    heel_r = (ax + int(90*s), ay - int(15*s))
    heel_rb = (ax + int(90*s), ay + int(8*s))

    # Waist
    waist_l = (ax - int(50*s), ay + int(8*s))
    waist_lb = (ax - int(50*s), ay + int(35*s))
    waist_r = (ax + int(50*s), ay + int(8*s))
    waist_rb = (ax + int(50*s), ay + int(35*s))

    # Base
    base_l = (ax - int(75*s), ay + int(35*s))
    base_lb = (ax - int(75*s), ay + int(55*s))
    base_r = (ax + int(75*s), ay + int(35*s))
    base_rb = (ax + int(75*s), ay + int(55*s))

    # Draw anvil as one bold shape
    anvil_poly = [
        horn_l,        # horn tip left
        face_l,        # top-left
        face_r,        # top-right
        heel_r,        # heel tip right
        heel_rb,       # heel bottom right
        face_rb,       # right side bottom
        waist_r,       # waist right top
        waist_rb,      # waist right bottom
        base_r,        # base right top
        base_rb,       # base right bottom
        base_lb,       # base left bottom
        base_l,        # base left top
        waist_lb,      # waist left bottom
        waist_l,       # waist left top
        face_lb,       # left side bottom
        horn_lb,       # horn bottom left
    ]
    d.polygon(anvil_poly, fill=col)

    # === Small play triangle (bottom-right of anvil) ===
    # Positioned as a "badge" like DT style
    px = cx + int(55*s)
    py = cy + int(65*s)
    pr = int(32*s)

    # Dark circle behind play button
    d.ellipse([px-pr-4, py-pr-4, px+pr+4, py+pr+4], fill=(140, 95, 10))
    d.ellipse([px-pr, py-pr, px+pr, py+pr], fill=(60, 42, 8))
    # Play triangle
    tri_s = int(18*s)
    d.polygon([
        (px - int(10*s), py - tri_s),
        (px - int(10*s), py + tri_s),
        (px + int(16*s), py)
    ], fill=(240, 185, 45))

    # === Motion lines (left side, animation hint) ===
    for i, offy in enumerate([-30, -15, 0]):
        lx = cx - int(105*s)
        ly = cy + int(offy*s) + int(50*s)
        length = int((25 - i*5)*s)
        alpha = 255 - i * 60
        line_col = (255, 250, 240, alpha)
        d.rounded_rectangle(
            [lx - length, ly - int(3*s), lx, ly + int(3*s)],
            radius=int(3*s),
            fill=col if i == 0 else (250, 245, 230)
        )

    # Save as .ico with multiple sizes
    ico_path = r'I:\CLAUDE\VSAnimator\dist\VSAnimator.ico'
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    imgs = []
    for s_size in sizes:
        resampled = img.resize(s_size, Image.LANCZOS)
        imgs.append(resampled)

    imgs[0].save(ico_path, format='ICO',
                 sizes=[(i.width, i.height) for i in imgs],
                 append_images=imgs[1:])
    print(f"Icon saved: {ico_path}")

    # Also save PNG preview
    preview = img.resize((256, 256), Image.LANCZOS)
    preview.save(ico_path.replace('.ico', '_preview.png'))
    print("Preview saved")

if __name__ == '__main__':
    make_icon()
