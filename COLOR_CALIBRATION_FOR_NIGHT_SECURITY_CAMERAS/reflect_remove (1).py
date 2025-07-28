# pip install fast-reflection-removal
import argparse
from frr import FastReflectionRemoval
from PIL import Image
import numpy as np
import os

def run_reflection_removal(input_img, output_img, h=0.1):
    print("🪞 Removing reflections...")
    img = Image.open(input_img).convert("RGB")
    img_np = np.asarray(img).astype(np.float32) / 255.0

    # Apply reflection removal
    remover = FastReflectionRemoval(h=h)
    result = remover.remove_reflection(img_np)

    # Convert and save
    result_img = Image.fromarray((result * 255).astype(np.uint8))
    result_img.save(output_img)
    print("✅ Reflection-removed image saved to:", output_img)
    return output_img

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--h", type=float, default=0.1, help="Reflection strength [0.05 - 0.2]")
    args = parser.parse_args()

    run_reflection_removal(args.input, args.output, h=args.h)
