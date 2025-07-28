import os
import subprocess

# Base directory of your project
base_dir = r"C:\Users\HIKVISION\Desktop\PYTHON\FINAL PROJECT"

# Input/output paths
img_raw = os.path.join(base_dir, "input", "in.jpg")
mask_in = os.path.join(base_dir, "input", "mask.png")

step1_reflect = os.path.join(base_dir, "outputs", "step1_noreflect.png")
step2_inpaint = os.path.join(base_dir, "outputs", "step2_inpainted.png")
step3_restored = os.path.join(base_dir, "outputs", "step3_restored.png")
step4_upscaled = os.path.join(base_dir, "outputs", "final_output.png")

# Directories of the repos inside the project folder
gfpgan_dir = os.path.join(base_dir, "GFPGAN")
realesrgan_dir = os.path.join(base_dir, "Real-ESRGAN")
segment_anything_dir = os.path.join(base_dir, "segment-anything")

# SAM checkpoint path inside segment-anything repo
sam_checkpoint = os.path.join(segment_anything_dir, "checkpoints", "sam_vit_b_01ec64.pth")

# Check SAM checkpoint existence
if not os.path.isfile(sam_checkpoint):
    raise FileNotFoundError(
        f"❌ SAM checkpoint not found at {sam_checkpoint}. Please download it and place it there."
    )

print("🧠 [0/5] Generating smart mask with SAM fallback")
subprocess.run([
    "python", os.path.join(base_dir, "smart_mask.py"),
    "--input", img_raw,
    "--output", mask_in,
    "--sam_checkpoint", sam_checkpoint
], check=True, cwd=base_dir)

print("🪞 [1/5] Reflection Removal")
subprocess.run([
    "python", os.path.join(base_dir, "reflect_remove.py"),
    "--input", img_raw,
    "--output", step1_reflect,
    "--h", "0.1"
], check=True, cwd=base_dir)

print("🎨 [2/5] LaMa Inpainting")
subprocess.run([
    "python", os.path.join(base_dir, "lama_inpaint.py"),
    "--input", step1_reflect,
    "--mask", mask_in,
    "--output", step2_inpaint
], check=True, cwd=base_dir)

print("😊 [3/5] GFPGAN Face Restoration")
subprocess.run([
    "python", os.path.join(base_dir, "run_gfpgan.py"),
    "--input", step2_inpaint,
    "--gfpgan_dir", gfpgan_dir,
    "--output", step3_restored
], check=True, cwd=gfpgan_dir)

print("🚀 [4/5] Real-ESRGAN Upscaling")
subprocess.run([
    "python", os.path.join(base_dir, "run_realesrgan.py"),
    "--input", step3_restored,
    "--realesrgan_dir", realesrgan_dir,
    "--output", step4_upscaled
], check=True, cwd=realesrgan_dir)

print("\n✅ DONE! Final output saved at:", step4_upscaled)
