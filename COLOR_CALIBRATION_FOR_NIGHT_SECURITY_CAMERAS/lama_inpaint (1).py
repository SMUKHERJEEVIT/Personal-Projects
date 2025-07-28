#pip install simple-lama-inpainting Pillow

import argparse
from simple_lama_inpainting import SimpleLama
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description="LaMa inpainting")
    parser.add_argument("--input", required=True, help="Path to input image (RGB)")
    parser.add_argument("--mask", required=True, help="Path to binary mask (white = mask)")
    parser.add_argument("--output", required=True, help="Path to save inpainted image")
    args = parser.parse_args()

    img = Image.open(args.input).convert("RGB")
    mask = Image.open(args.mask).convert("L")
    simple_lama = SimpleLama()  # loads pretrained model
    result = simple_lama(img, mask)
    result.save(args.output)
    print("✅ LaMa inpainted image saved to:", args.output)

if __name__ == "__main__":
    main()
