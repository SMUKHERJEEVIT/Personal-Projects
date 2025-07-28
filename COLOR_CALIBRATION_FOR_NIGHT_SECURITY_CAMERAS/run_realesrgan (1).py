# run_realesrgan.py
import argparse
import subprocess
import os

def run_realesrgan(input_img, realesrgan_dir, output_dir="realesrgan_out"):
    print("📈 Running Real-ESRGAN...")
    outdir = os.path.join(realesrgan_dir, output_dir)
    os.makedirs(outdir, exist_ok=True)

    cmd = [
        "python", "inference_realesrgan.py",
        "-n", "RealESRGAN_x4plus",
        "-i", input_img,
        "-o", outdir,
        "--fp32"
    ]
    subprocess.run(cmd, cwd=realesrgan_dir, check=True)

    result = os.path.join(outdir, os.path.basename(input_img))
    if not os.path.isfile(result):
        raise FileNotFoundError("❌ Real-ESRGAN did not produce output.")
    print("✅ Real-ESRGAN result:", result)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--realesrgan_dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = run_realesrgan(args.input, args.realesrgan_dir)
    from PIL import Image
    Image.open(result).save(args.output)
