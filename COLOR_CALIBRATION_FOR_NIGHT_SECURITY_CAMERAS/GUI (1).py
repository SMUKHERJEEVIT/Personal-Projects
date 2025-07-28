import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tqdm import tqdm


def run_process(cmd_list, cwd=None):
    """
    Runs the subprocess command with a list of arguments and prints progress.
    """
    print(f"\n▶️ Running: {' '.join(cmd_list)}")
    subprocess.run(cmd_list, check=True, cwd=cwd)
    print("✅ Step completed.")


def main(input_img, output_dir, sam_checkpoint, run_steps):
    """
    Main pipeline function that executes each step.
    """
    mask_in = os.path.join(output_dir, "mask.png")
    step1_reflect = os.path.join(output_dir, "step1_noreflect.png")
    step2_inpaint = os.path.join(output_dir, "step2_inpainted.png")
    step3_restored = os.path.join(output_dir, "step3_restored.png")
    step4_upscaled = os.path.join(output_dir, "step4_upscaled.png") 
    step5_swinir = os.path.join(output_dir, "step5_swinir_x2.png")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    gfpgan_dir = os.path.join(base_dir, "GFPGAN")
    realesrgan_dir = os.path.join(base_dir, "Real-ESRGAN")

    if not os.path.isfile(sam_checkpoint):
        raise FileNotFoundError(f"SAM checkpoint not found at {sam_checkpoint}")

    step_names = {
        '0': "🧠 [0/6] Smart Mask Generation",
        '1': "🪞 [1/6] Reflection Removal",
        '2': "🎨 [2/6] LaMa Inpainting",
        '3': "😊 [3/6] GFPGAN Restoration",
        '4': "🚀 [4/6] Real-ESRGAN Upscaling",
        '5': "🧠 [5/6] SwinIR Super-Resolution x2"
    }

    with tqdm(total=len(run_steps), desc="🧪 Pipeline Progress", unit="step") as pbar:
        if '0' in run_steps:
            print(step_names['0'])
            run_process([
                "python", os.path.join(base_dir, "smart_mask.py"),
                "--input", input_img,
                "--output", mask_in,
                "--sam_checkpoint", sam_checkpoint
            ], cwd=base_dir)
            pbar.update(1)

        if '1' in run_steps:
            print(step_names['1'])
            run_process([
                "python", os.path.join(base_dir, "reflect_remove.py"),
                "--input", input_img,
                "--output", step1_reflect,
                "--h", "0.1"
            ], cwd=base_dir)
            pbar.update(1)

        if '2' in run_steps:
            print(step_names['2'])
            run_process([
                "python", os.path.join(base_dir, "lama_inpaint.py"),
                "--input", step1_reflect,
                "--mask", mask_in,
                "--output", step2_inpaint
            ], cwd=base_dir)
            pbar.update(1)

        if '3' in run_steps:
            print(step_names['3'])
            run_process([
                "python", os.path.join(base_dir, "run_gfpgan.py"),
                "--input", step2_inpaint,
                "--gfpgan_dir", gfpgan_dir,
                "--output", step3_restored
            ], cwd=gfpgan_dir)
            pbar.update(1)

        if '4' in run_steps:
            print(step_names['4'])
            run_process([
                "python", os.path.join(base_dir, "run_realesrgan.py"),
                "--input", step3_restored,
                "--realesrgan_dir", realesrgan_dir,
                "--output", step4_upscaled
            ], cwd=realesrgan_dir)
            pbar.update(1)

        if '5' in run_steps:
            print(step_names['5'])
            swinir_weights = os.path.join(base_dir, "model_zoo", "swinir", "001_classicalSR_DF2K_s64w8_SwinIR-M_x2.pth")
            swinir_input = step3_restored if '3' in run_steps else step2_inpaint
            run_process([
                "python", os.path.join(base_dir, "SwinIR.py"),
                "--input", swinir_input,
                "--output", step5_swinir,
                "--model_path", swinir_weights
            ], cwd=base_dir)
            pbar.update(1)

    final_output = None
    if '5' in run_steps:
        final_output = step5_swinir
    elif '4' in run_steps:
        final_output = step4_upscaled
    else:
        final_output = output_dir

    print(f"\n✅ DONE! Final output saved at: {final_output}")


def browse_input():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, path)


def browse_output():
    path = filedialog.askdirectory()
    if path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, path)


def browse_checkpoint():
    path = filedialog.askopenfilename(filetypes=[("Checkpoint files", "*.pth")])
    if path:
        sam_checkpoint_entry.delete(0, tk.END)
        sam_checkpoint_entry.insert(0, path)


def run_pipeline():
    input_img = input_entry.get()
    output_dir = output_entry.get()
    sam_checkpoint = sam_checkpoint_entry.get()

    steps = "".join(str(i) for i, var in enumerate(steps_vars) if var.get())

    if not steps:
        messagebox.showerror("Error", "Select at least one processing step.")
        return

    if not os.path.isfile(input_img):
        messagebox.showerror("Error", "Input image file does not exist.")
        return
    if not os.path.isdir(output_dir):
        messagebox.showerror("Error", "Output directory does not exist.")
        return
    if not os.path.isfile(sam_checkpoint):
        messagebox.showerror("Error", "SAM checkpoint file does not exist.")
        return

    try:
        main(input_img, output_dir, sam_checkpoint, steps)
        messagebox.showinfo("Success", "Processing completed!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Subprocess failed:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")


# GUI Setup
root = tk.Tk()
root.title("Image Processing Pipeline")

# Input Image
tk.Label(root, text="Input Image:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_input).grid(row=0, column=2, padx=5, pady=5)

# Output Folder
tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_output).grid(row=1, column=2, padx=5, pady=5)

# SAM Checkpoint
tk.Label(root, text="SAM Checkpoint:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
sam_checkpoint_entry = tk.Entry(root, width=50)
sam_checkpoint_entry.grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_checkpoint).grid(row=2, column=2, padx=5, pady=5)
sam_checkpoint_entry.insert(0, r"C:\path\to\sam_checkpoint.pth")  # <- Change this default path as needed

# Processing Steps
steps_vars = []
step_labels = [
    "0: Smart Mask Generation",
    "1: Reflection Removal",
    "2: LaMa Inpainting",
    "3: GFPGAN Restoration",
    "4: Real-ESRGAN Upscaling",
    "5: SwinIR Super-Resolution x2"
]

tk.Label(root, text="Select Processing Steps:").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
steps_frame = tk.Frame(root)
steps_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)

for i, label in enumerate(step_labels):
    var = tk.IntVar(value=1)  # default: checked
    cb = tk.Checkbutton(steps_frame, text=label, variable=var)
    cb.pack(anchor='w')
    steps_vars.append(var)

# Run Button
tk.Button(root, text="Run Pipeline", command=run_pipeline).grid(row=4, column=1, pady=15)

root.mainloop()
