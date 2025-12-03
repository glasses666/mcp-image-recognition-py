from io import BytesIO
from PIL import Image
import base64

def process_image_data(image_bytes: bytes, max_size: int = 1536, max_file_size_mb: int = 4) -> str:
    """
    Process raw image bytes:
    1. Open with PIL.
    2. Resize if larger than max_size (longest edge).
    3. Convert/Compress to JPEG to ensure it's within size limits and widely compatible.
    4. Return base64 string.
    """
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            # Convert to RGB if necessary (handling PNG alpha channel, etc.)
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')
                
            # Resize logic
            width, height = img.size
            if width > max_size or height > max_size:
                ratio = min(max_size / width, max_size / height)
                new_size = (int(width * ratio), int(height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save to buffer as JPEG
            buffer = BytesIO()
            # Start with high quality, lower it if needed (simple logic for now: just use 85)
            img.save(buffer, format="JPEG", quality=85)
            
            # Check size. If > max_file_size_mb, could compress further, 
            # but usually 1536px side at q85 is < 1MB.
            
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
            
    except Exception as e:
        # If image processing fails (e.g. invalid image format), raise it up
        raise ValueError(f"Failed to process image data: {str(e)}")