import sys
import os
import torch
from PIL import Image
import numpy as np
from torchvision import transforms
import timm


# Add the 'models' folder to sys.path dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
models_path = os.path.join(current_dir, "models")
if models_path not in sys.path:
    sys.path.append(models_path)

# Import SwinIR model class from network_swinir.py
from SwinIR.models.network_swinir import SwinIR


def save_image(tensor, output_path):
    """
    Converts a tensor to a numpy array and saves it as an image.
    """
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert tensor to numpy array and remove batch dimension
    tensor = tensor.squeeze().cpu().clamp(0, 1).numpy()  # Remove batch dimension and clamp values to [0, 1]
    tensor = np.transpose(tensor, (1, 2, 0))  # Convert to HWC format (height, width, channels)

    # Convert to uint8
    tensor = (tensor * 255).astype(np.uint8)

    # Convert numpy array to PIL Image and save
    img = Image.fromarray(tensor)
    img.save(output_path)
    print(f"Image saved at {output_path}")


def process_image(input_img, output_path, model_weights):
    """
    Processes an image using the SwinIR model and saves the output.
    """
    # Initialize the SwinIR model with predefined parameters
    model = SwinIR(
        img_size=64,       # Example image patch size (adjust if needed)
        patch_size=1,      # Patch size
        in_chans=3,        # Input channels (RGB)
        embed_dim=180,     # Embedding dimension
        depths=[6, 6, 6, 6],  # Depth of each Swin Transformer stage
        num_heads=[6, 6, 6, 6],  # Number of attention heads
        window_size=8,     # Window size
        mlp_ratio=2,       # MLP ratio for transformer layers
        upsampler='pixelshuffle',  # Upsampler type
        upscale=2          # Upscaling factor (2x in this case)
    )

    # Load model weights (with strict=False to ignore mismatches between model and checkpoint)
    try:
        checkpoint = torch.load(model_weights)
        model.load_state_dict(checkpoint, strict=False)
        print("SwinIR model loaded successfully.")
    except Exception as e:
        print(f"Error loading model weights: {e}")
        return None

    # Load and preprocess input image
    try:
        img = Image.open(input_img).convert("RGB")
        # Resize input image to the model's expected size
        transform = transforms.Compose([
            transforms.Resize((64, 64)),  # Resize to model input size (adjust as needed)
            transforms.ToTensor(),
        ])
        x = transform(img).unsqueeze(0)  # Add batch dimension
    except Exception as e:
        print(f"Error loading or preprocessing the image: {e}")
        return None

    # Forward pass (inference)
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        try:
            output = model(x)  # Run the model on the input image
            print(f"Output shape: {output.shape}")
        except Exception as e:
            print(f"Error during model inference: {e}")
            return None

    # Save the output image
    save_image(output, output_path)

    return output
