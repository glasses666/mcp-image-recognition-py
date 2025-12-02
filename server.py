import os
import base64
import httpx
from typing import Optional
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from openai import AsyncOpenAI
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")

# Initialize MCP Server
mcp = FastMCP("image-recognition")

async def get_image_data(image_input: str) -> tuple[str, str]:
    """
    Process image input (URL or Base64) and return (mime_type, base64_data).
    """
    if image_input.startswith(('http://', 'https://')):
        async with httpx.AsyncClient() as client:
            response = await client.get(image_input)
            response.raise_for_status()
            mime_type = response.headers.get('content-type', 'image/jpeg')
            data = base64.b64encode(response.content).decode('utf-8')
            return mime_type, data
    
    if image_input.startswith('data:'):
        header, data = image_input.split(',', 1)
        mime_type = header.split(';')[0].split(':')[1]
        return mime_type, data
        
    # Assume raw base64, default to jpeg
    return 'image/jpeg', image_input

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

async def recognize_with_openai_compat(model_name: str, prompt: str, image_input: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set")
        
    client = AsyncOpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )

    # Clean the input: remove newlines and whitespace which cause base64 decode errors
    cleaned_input = image_input.strip().replace("\n", "").replace("\r", "").replace(" ", "")

    # Determine the final image URL format
    if cleaned_input.startswith(('http://', 'https://')):
        # It is a URL, use original input (trimmed) but don't strip spaces inside URL just in case (though invalid)
        # Actually, standard URLs shouldn't have spaces, but let's just use .strip() for URLs
        final_image_url = image_input.strip() 
    elif cleaned_input.startswith('data:'):
        # It is already a data URI
        final_image_url = cleaned_input
    else:
        # Assume raw base64 if it's not a URL or Data URI. Default to jpeg.
        final_image_url = f"data:image/jpeg;base64,{cleaned_input}"
    
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
    
    # Routing logic
    if "gemini" in target_model.lower():
        # Gemini usually requires the image data to be uploaded or passed as inline data (bytes)
        # It does not natively support fetching public URLs in the same way OpenAI's API does for 'image_url'
        mime_type, b64_data = await get_image_data(image)
        return await recognize_with_gemini(target_model, prompt, mime_type, b64_data)
    else:
        # Fallback to OpenAI compatible for qwen, doubao, gpt, etc.
        # These providers often support URLs directly, or data URIs.
        return await recognize_with_openai_compat(target_model, prompt, image)

def main():
    mcp.run()

if __name__ == "__main__":
    main()