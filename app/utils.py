import base64
import os
import subprocess
from pdf2image import convert_from_path
from typing import List, Tuple

from PIL import Image
from io import BytesIO
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2

def pdf_to_base64_images(pdf_path: str) -> List[str]:
    """Converts PDF pages to base64-encoded PNG images."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    images = convert_from_path(pdf_path)
    base64_images = []
    for img in images:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        base64_images.append(img_str)
    return base64_images

def calculate_similarity(img1_base64: str, img2_base64: str) -> float:
    """Calculates Structural Similarity Index (SSIM) between two base64 images."""
    try:
        # Load images
        img1 = Image.open(BytesIO(base64.b64decode(img1_base64))).convert("L") # Grayscale
        img2 = Image.open(BytesIO(base64.b64decode(img2_base64))).convert("L")
        
        # Ensure same size
        if img1.size != img2.size:
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
            
        # Convert to numpy arrays
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        
        # Calculate SSIM
        # win_size should be odd and smaller than image dimensions
        score, _ = ssim(arr1, arr2, full=True)
        
        return float(score)
    except Exception as e:
        print(f"Error calculating SSIM: {e}")
        return 0.0

def compile_typst(typst_code: str, output_pdf: str = "output.pdf") -> Tuple[bool, str]:
    """Compiles Typst code into a PDF. Returns (success, logs)."""
    with open("temp.typ", "w") as f:
        f.write(typst_code)
    
    try:
        result = subprocess.run(
            ["typst", "compile", "temp.typ", output_pdf],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return True, "Compilation successful."
        else:
            print(f"Typst Error: {result.stderr}")
            return False, result.stderr
    except FileNotFoundError:
        msg = "Error: 'typst' command not found. Please install Typst (https://typst.app/)."
        print(msg)
        return False, msg
    except Exception as e:
        print(f"Subprocess Exception: {e}")
        return False, str(e)

def cleanup_temp_files(files: List[str]):
    for f in files:
        if os.path.exists(f):
            os.remove(f)
