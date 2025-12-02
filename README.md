# MCP Image Recognition Server (Python)

An MCP server implementation in Python providing image recognition capabilities using various LLM providers (Gemini, OpenAI, Qwen/Tongyi, Doubao, etc.).

## Features
- **Image Recognition**: Describe images or answer questions about them.
- **Multi-Model Support**: Dynamically switch between Gemini, GPT-4o, Qwen-VL, Doubao, etc.
- **Flexible**: Accepts image URLs or Base64 data.

## Installation & Usage

You can run this server using standard Python tools or the modern `uv` package manager.

### Prerequisites
- Python 3.10 or higher
- An API Key for your preferred model provider (Google Gemini, OpenAI, Aliyun DashScope, etc.)

---

### Method 1: Using `uv` (Recommended)

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package manager.

#### 1. Run directly with `uv run`
You don't need to manually create a virtual environment.

```bash
# Clone the repo
git clone https://github.com/glasses666/mcp-image-recognition-py.git
cd mcp-image-recognition-py

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your keys

# Run the server
uv run server.py
```

#### 2. Using `uvx` (for ephemeral execution)
If you want to run it without cloning the repo explicitly (experimental support via git):

```bash
# Note: You still need to provide environment variables. 
# It's easier to clone and use 'uv run' for persistent config via .env
uvx --from git+https://github.com/glasses666/mcp-image-recognition-py mcp-image-recognition
```

---

### Method 2: Standard Python (pip)

#### Linux / macOS

1. **Clone and Setup:**
   ```bash
   git clone https://github.com/glasses666/mcp-image-recognition-py.git
   cd mcp-image-recognition-py
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Run:**
   ```bash
   python server.py
   ```

#### Windows

1. **Clone and Setup:**
   ```powershell
   git clone https://github.com/glasses666/mcp-image-recognition-py.git
   cd mcp-image-recognition-py
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure:**
   ```powershell
   copy .env.example .env
   # Edit .env and add your API keys
   ```

3. **Run:**
   ```powershell
   python server.py
   ```

---

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

---

## Agent AI Configuration (Claude Desktop, etc.)

To use this server with an MCP client (like Claude Desktop), add it to your configuration file.

### Configuration File Paths
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json` (if available)

### Configuration JSON

**Option A: Using `uv` (Easiest)**
If you have `uv` installed, you can let it handle the environment.

```json
{
  "mcpServers": {
    "image-recognition": {
      "command": "/path/to/uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp-image-recognition-py",
        "server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "your_key_here",
        "DEFAULT_MODEL": "gemini-1.5-flash"
      }
    }
  }
}
```

**Option B: Standard Python Venv**
Ensure you provide the **absolute path** to the python executable in your virtual environment.

```json
{
  "mcpServers": {
    "image-recognition": {
      "command": "/absolute/path/to/mcp-image-recognition-py/venv/bin/python", 
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

*Windows Note:* For paths, use double backslashes `\\` (e.g., `C:\\Users\\Name\\...`).

---

## Usage Tool

### `recognize_image`
Analyzes an image and returns a text description.

**Parameters:**
- `image` (string, required): The image to analyze. Supports:
    - HTTP/HTTPS URLs (e.g., `https://example.com/cat.jpg`)
    - Base64 encoded strings (with or without `data:image/...;base64,` prefix)
- `prompt` (string, optional): Specific instruction. Default: "Describe this image".
- `model` (string, optional): Override the default model for this specific request.

## License
MIT