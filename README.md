# MCP Image Recognition Server (Python)

An MCP server implementation in Python providing image recognition capabilities using various LLM providers (Gemini, OpenAI, Qwen/Tongyi, Doubao, etc.).

## Features
- **Image Recognition**: Describe images or answer questions about them.
- **Multi-Model Support**: Dynamically switch between Gemini, GPT-4o, Qwen-VL, Doubao, etc.
- **Flexible**: Accepts image URLs or Base64 data.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd mcp-image-recognition-py
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root based on `.env.example`:

### 1. For Google Gemini (Recommended for speed/cost)
Get an API key from [Google AI Studio](https://aistudio.google.com/).
```env
GEMINI_API_KEY=your_google_api_key
DEFAULT_MODEL=gemini-1.5-flash
```

### 2. For Tongyi Qianwen (Qwen - Alibaba Cloud)
Get an API key from [Aliyun DashScope](https://dashscope.console.aliyun.com/).
```env
OPENAI_API_KEY=your_dashscope_api_key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DEFAULT_MODEL=qwen-vl-max
```

### 3. For Doubao (Volcengine)
Get an API key from [Volcengine Ark](https://www.volcengine.com/product/ark).
```env
OPENAI_API_KEY=your_volcengine_api_key
OPENAI_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
DEFAULT_MODEL=doubao-pro-32k
```

## Agent AI Configuration

To use this server with an MCP client (like Claude Desktop), add it to your configuration file (e.g., `claude_desktop_config.json`):

### MacOS
`~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
`%APPDATA%\Claude\claude_desktop_config.json`

### Configuration JSON:
**Important:** Ensure you provide the absolute path to your Python executable (in the virtualenv) and the `server.py` script.

```json
{
  "mcpServers": {
    "image-recognition": {
      "command": "/absolute/path/to/venv/bin/python",
      "args": [
        "/absolute/path/to/mcp-image-recognition-py/server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "your_key_here",
        "DEFAULT_MODEL": "gemini-1.5-flash"
      }
    }
  }
}
```
*Note: You can pass environment variables directly in the config JSON `env` section instead of relying on the `.env` file if you prefer.*

## Usage

Once connected, the server provides the following tool:

### `recognize_image`
Analyzes an image and returns a text description.

**Parameters:**
- `image` (string, required): The image to analyze. Supports:
    - HTTP/HTTPS URLs (e.g., `https://example.com/cat.jpg`)
    - Base64 encoded strings (with or without `data:image/...;base64,` prefix)
- `prompt` (string, optional): Specific instruction. Default: "Describe this image".
- `model` (string, optional): Override the default model for this specific request (e.g., use `gemini-1.5-pro` for complex reasoning).

## License
MIT
