import os
import base64
import httpx
import re
from typing import Optional
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from openai import AsyncOpenAI
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from image_processing import process_image_data

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")

# Initialize MCP Server
mcp = FastMCP("image-recognition")

async def get_processed_image_data(image_input: str) -> tuple[str, str]:
    """
    Process image input (URL or Base64), resize/compress it, and return (mime_type, base64_data).
    Always returns image/jpeg.
    """
    image_bytes = b""
    
    # Clean input: remove whitespace/newlines from the *entire* string if it's potentially base64
    image_input = image_input.strip().replace("\n", "").replace("\r", "")

    if image_input.startswith(('http://', 'https://')):
        async with httpx.AsyncClient() as client:
            response = await client.get(image_input)
            response.raise_for_status()
            image_bytes = response.content
    elif image_input.startswith('data:'):
        # Extract base64 part
        try:
            _, data = image_input.split(',', 1)
            # Further clean the data part just in case
            data = data.replace(" ", "")
            missing_padding = len(data) % 4
            if missing_padding:
                data += '=' * (4 - missing_padding)
            image_bytes = base64.b64decode(data)
        except Exception as e:
             raise ValueError(f"Invalid data URI or base64 data: {str(e)}")
    else:
        # Assume raw base64
        # Remove whitespaces which might be present in raw strings
        cleaned_b64 = image_input.replace(" ", "")
        
        # Add padding if necessary to avoid "Incorrect padding" errors
        missing_padding = len(cleaned_b64) % 4
        if missing_padding:
            cleaned_b64 += '=' * (4 - missing_padding)
            
        try:
            image_bytes = base64.b64decode(cleaned_b64)
        except Exception as e:
             raise ValueError(f"Invalid raw base64 string: {str(e)}")
    
    # Process using the new utility
    processed_b64 = process_image_data(image_bytes)
    return "image/jpeg", processed_b64

async def recognize_with_gemini(model_name: str, prompt: str, mime_type: str, b64_data: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set")
    
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name)
    
    # Create the image part properly for Gemini
    image_part = {
        "mime_type": mime_type,
        "data": b64_data
    }
    
    generation_config = genai.GenerationConfig(
        temperature=0.4,
        max_output_tokens=2048,
    )

    try:
        response = await model.generate_content_async(
            [prompt, image_part],
            generation_config=generation_config
        )
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"

async def recognize_with_openai_compat(model_name: str, prompt: str, mime_type: str, b64_data: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")
        
    client = AsyncOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )

    # Construct clean data URI
    final_image_url = f"data:{mime_type};base64,{b64_data}"
    
    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": final_image_url
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content or "No response content"
    except Exception as e:
        return f"OpenAI Compatible API Error: {str(e)}"

@mcp.tool()
async def recognize_image(image: str, prompt: str = "Describe this image", model: Optional[str] = None) -> str:
    """
    Recognize and describe the content of an image using AI models.
    
    Args:
        image: The image to analyze. Can be a URL (http/https) or a Base64 encoded string.
        prompt: Optional instruction or question about the image. Default is 'Describe this image'.
        model: Optional model name (e.g., 'gemini-1.5-flash', 'qwen-vl-max'). If not provided, uses DEFAULT_MODEL env var.
    """
    target_model = model or DEFAULT_MODEL
    
    # Always process image first (resize, compress, standardize to JPEG base64)
    # This fixes 400 errors from strict APIs and reduces token usage.
    try:
        mime_type, b64_data = await get_processed_image_data(image)
    except Exception as e:
        return f"Error processing image: {str(e)}"
    
    # Routing logic
    if "gemini" in target_model.lower():
        return await recognize_with_gemini(target_model, prompt, mime_type, b64_data)
    else:
        # Fallback to OpenAI compatible for qwen, doubao, gpt, etc.
        return await recognize_with_openai_compat(target_model, prompt, mime_type, b64_data)

def main():
    mcp.run()

if __name__ == "__main__":
    main()