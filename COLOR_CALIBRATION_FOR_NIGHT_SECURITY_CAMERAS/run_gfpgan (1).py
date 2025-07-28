import argparse
import subprocess
import os
from PIL import Image
def run_gfpgan(input_img, gfpgan_dir, output_dir="gfpgan_out"):
    print("🧠 Running GFPGAN...")
    outdir = os.path.join(gfpgan_dir, output_dir)
    os.makedirs(outdir, exist_ok=True)

    cmd = [
        "python", "inference_gfpgan.py",
        "-i", input_img,
        "-o", outdir,
        "--bg_upsampler", "realesrgan"
    ]
    subprocess.run(cmd, cwd=gfpgan_dir, check=True)

    output_img = os.path.join(outdir, "restored_imgs", os.path.basename(input_img))
    if not os.path.isfile(output_img):
        raise FileNotFoundError("❌ GFPGAN did not produce output.")
    print("✅ GFPGAN result:", output_img)
    return output_img

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--gfpgan_dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = run_gfpgan(args.input, args.gfpgan_dir)
    Image.open(result).save(args.output)


