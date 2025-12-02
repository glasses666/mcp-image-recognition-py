import base64
from PIL import Image
import io

def process_image_data(image_data: bytes) -> str:
    """
    Resize and compress image data (bytes), returning a base64 encoded string.
    """
    try:
        # Load image from bytes
        with Image.open(io.BytesIO(image_data)) as img:
            # Resize if too large
            max_size = (600, 600) # As per user's original script
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to buffer
            buffer = io.BytesIO()
            # Convert to RGB if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Compress
            img.save(buffer, format="JPEG", quality=50)
            
            # Encode
            processed_bytes = buffer.getvalue()
            base64_str = base64.b64encode(processed_bytes).decode('utf-8')
            return base64_str
    except Exception as e:
        # If processing fails (e.g. not an image), try to just base64 encode original
        # This acts as a fallback
        print(f"Image processing failed: {e}. Falling back to original data.")
        return base64.b64encode(image_data).decode('utf-8')
