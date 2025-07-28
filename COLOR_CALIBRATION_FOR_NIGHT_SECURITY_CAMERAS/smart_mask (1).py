import sys
import os

# ✅ Add the segment-anything repo to sys.path
segment_anything_root = r"C:\Users\HIKVISION\Desktop\PYTHON\FINAL PROJECT\segment-anything"
if segment_anything_root not in sys.path:
    sys.path.insert(0, segment_anything_root)

try:
    from segment_anything import sam_model_registry, SamPredictor
    import torch
    SAM_AVAILABLE = True
except ImportError:
    SAM_AVAILABLE = False
    print("⚠️ SAM not installed or import failed. SAM fallback disabled.")

from PIL import Image, ImageDraw
import cv2
import numpy as np

def create_bbox_mask(img, bbox_rel=(0.25, 0.2, 0.75, 0.6)):
    w, h = img.size
    left = int(w * bbox_rel[0])
    top = int(h * bbox_rel[1])
    right = int(w * bbox_rel[2])
    bottom = int(h * bbox_rel[3])

    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([left, top, right, bottom], fill=255)
    return mask

def create_color_mask(img, lower_hsv, upper_hsv):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(img_cv, lower_hsv, upper_hsv)
    return Image.fromarray(mask)

def refine_mask(mask, kernel_size=15):
    mask_np = np.array(mask)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    mask_np = cv2.dilate(mask_np, kernel, iterations=1)
    mask_np = cv2.erode(mask_np, kernel, iterations=1)
    return Image.fromarray(mask_np)

def sam_mask(img, sam_checkpoint, device='cuda'):
    if not SAM_AVAILABLE:
        print("⚠️ SAM not available, skipping SAM mask.")
        return None

    print("🤖 Running SAM fallback...")

    sam = sam_model_registry["vit_b"](checkpoint=sam_checkpoint)
    sam.to(device=device)
    predictor = SamPredictor(sam)
    img_np = np.array(img)
    predictor.set_image(img_np)

    w, h = img.size
    points = np.array([[int(w * 0.5), int(h * 0.4)]])  # center-ish point inside glass

    masks, scores, logits = predictor.predict(
        point_coords=points,
        point_labels=np.array([1]),
        multimask_output=False
    )
    mask = masks[0].astype(np.uint8) * 255
    return Image.fromarray(mask)

def mask_is_valid(mask, min_area_ratio=0.01):
    arr = np.array(mask)
    area = np.count_nonzero(arr)
    total = arr.size
    ratio = area / total
    return ratio > min_area_ratio

def generate_smart_mask(image_path, output_mask_path, sam_checkpoint=None, use_sam_fallback=True):
    img = Image.open(image_path).convert("RGB")

    print("🟢 Creating bbox mask...")
    mask = create_bbox_mask(img)

    if not mask_is_valid(mask):
        print("⚠️ Bbox mask too small, trying color mask fallback...")
        lower_hsv = np.array([90, 20, 20])
        upper_hsv = np.array([130, 255, 200])
        mask = create_color_mask(img, lower_hsv, upper_hsv)

        if not mask_is_valid(mask):
            print("⚠️ Color mask too small or invalid.")
            if use_sam_fallback and sam_checkpoint:
                mask_sam = sam_mask(img, sam_checkpoint)
                if mask_sam and mask_is_valid(mask_sam):
                    mask = mask_sam
                else:
                    print("⚠️ SAM fallback failed or produced invalid mask.")
            else:
                print("⚠️ No SAM fallback or checkpoint missing.")

    print("🛠 Refining mask with morphological operations...")
    mask = refine_mask(mask)

    mask.save(output_mask_path)
    print(f"✅ Saved final mask to {output_mask_path}")
    return output_mask_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input image path")
    parser.add_argument("--output", required=True, help="Output mask path")
    parser.add_argument("--sam_checkpoint", default=None, help="Path to SAM checkpoint (.pth file)")
    parser.add_argument("--no_sam", action="store_true", help="Disable SAM fallback")
    args = parser.parse_args()

    generate_smart_mask(
        args.input,
        args.output,
        sam_checkpoint=args.sam_checkpoint,
        use_sam_fallback=not args.no_sam
    )