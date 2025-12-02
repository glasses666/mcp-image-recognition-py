# MCP 图像识别服务器 (Python)

这是一个基于 Python 的 MCP (Model Context Protocol) 服务器实现，提供图像识别功能。它支持多种大语言模型提供商（如 Google Gemini, OpenAI, 通义千问 Qwen, 豆包 Doubao 等）。

## 功能特性
- **图像识别**: 描述图像内容或回答关于图像的问题。
- **多模型支持**: 支持动态切换模型，包括 Gemini (推荐), GPT-4o, Qwen-VL (通义千问), Doubao (豆包) 等。
- **灵活性**: 支持 `uv` 包管理器，支持 Windows/Linux/macOS 跨平台部署。

## 安装与使用

你可以使用标准的 Python 工具 (pip) 或者现代化的 `uv` 包管理器来运行此服务器。

### 前置要求
- Python 3.10 或更高版本
- 您选择的模型提供商的 API Key (Google Gemini, OpenAI, 阿里云 DashScope 等)

---

### 方法 1: 使用 `uv` (推荐)

[uv](https://github.com/astral-sh/uv) 是一个极速的 Python 包管理器。

#### 1. 直接使用 `uv run` 运行
你不需要手动创建虚拟环境，`uv` 会自动处理。

```bash
# 克隆仓库
git clone https://github.com/glasses666/mcp-image-recognition-py.git
cd mcp-image-recognition-py

# 创建配置文件
cp .env.example .env
# 编辑 .env 文件填入你的 API Key

# 运行服务器
uv run server.py
```

#### 2. 使用 `uvx` (临时运行)
如果你不想克隆代码仓库，可以直接通过 `uvx` 运行 (支持 git 来源):

```bash
# 注意: 你仍然需要提供环境变量。
# 建议使用上面的 'uv run' 方法以便通过 .env 文件持久化配置。
uvx --from git+https://github.com/glasses666/mcp-image-recognition-py mcp-image-recognition
```

---

### 方法 2: 标准 Python (pip)

#### Linux / macOS

1. **克隆并设置:**
   ```bash
   git clone https://github.com/glasses666/mcp-image-recognition-py.git
   cd mcp-image-recognition-py
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **配置:**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件填入你的 API Key
   ```

3. **运行:**
   ```bash
   python server.py
   ```

#### Windows

1. **克隆并设置:**
   ```powershell
   git clone https://github.com/glasses666/mcp-image-recognition-py.git
   cd mcp-image-recognition-py
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **配置:**
   ```powershell
   copy .env.example .env
   # 编辑 .env 文件填入你的 API Key
   ```

3. **运行:**
   ```powershell
   python server.py
   ```

---

## 配置说明

在项目根目录下创建一个 `.env` 文件（参考 `.env.example`）：

### 1. 使用 Google Gemini (推荐，速度快且成本低)
从 [Google AI Studio](https://aistudio.google.com/) 获取 API Key。
```env
GEMINI_API_KEY=your_google_api_key
DEFAULT_MODEL=gemini-1.5-flash
```

### 2. 使用通义千问 (Qwen - 阿里云)
从 [阿里云百炼 DashScope](https://dashscope.console.aliyun.com/) 获取 API Key。
```env
OPENAI_API_KEY=your_dashscope_api_key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
DEFAULT_MODEL=qwen-vl-max
```

### 3. 使用豆包 (Doubao - 火山引擎)
从 [火山引擎 Ark](https://www.volcengine.com/product/ark) 获取 API Key。
```env
OPENAI_API_KEY=your_volcengine_api_key
OPENAI_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
DEFAULT_MODEL=doubao-pro-32k
```

---

## Agent AI 配置 (如 Claude Desktop)

要将此服务器用于 MCP 客户端（例如 Claude Desktop），请将其添加到您的配置文件中（例如 `claude_desktop_config.json`）。

### 配置文件位置
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### 配置 JSON 示例

**方案 A: 使用 `uv` (最简单)**
如果你安装了 `uv`，可以让它自动管理环境。

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
        "GEMINI_API_KEY": "your_gemini_key_here",
        "OPENAI_API_KEY": "your_openai_key_here",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "DEFAULT_MODEL": "gemini-1.5-flash"
      }
    }
  }
}
```

**方案 B: 标准 Python Venv**
确保使用虚拟环境中 Python 可执行文件的**绝对路径**。

```json
{
  "mcpServers": {
    "image-recognition": {
      "command": "/absolute/path/to/mcp-image-recognition-py/venv/bin/python", 
      "args": [
        "/absolute/path/to/mcp-image-recognition-py/server.py"
      ],
      "env": {
        "GEMINI_API_KEY": "your_gemini_key_here",
        "OPENAI_API_KEY": "your_openai_key_here",
        "OPENAI_BASE_URL": "https://api.openai.com/v1",
        "DEFAULT_MODEL": "gemini-1.5-flash"
      }
    }
  }
}
```
*Windows 注意:* 路径中的反斜杠需要转义，例如 `C:\Users\Name\...`。

---

## 使用工具

### `recognize_image`
分析图像并返回文本描述。

**参数:**
- `image` (string, 必填): 要分析的图像。支持:
    - HTTP/HTTPS URL (例如 `https://example.com/cat.jpg`)
    - Base64 编码字符串 (带或不带 `data:image/...;base64,` 前缀均可)
- `prompt` (string, 选填): 具体的指令或问题。默认值: "Describe this image" (描述这张图片)。
- `model` (string, 选填): 针对本次请求指定使用的模型。

## 许可证
MIT