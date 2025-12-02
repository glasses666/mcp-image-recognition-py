# MCP 图像识别服务器 (Python)

这是一个基于 Python 的 MCP (Model Context Protocol) 服务器实现，提供图像识别功能。它支持多种大语言模型提供商（如 Google Gemini, OpenAI, 通义千问 Qwen, 豆包 Doubao 等）。

## 功能特性
- **图像识别**: 描述图像内容或回答关于图像的问题。
- **多模型支持**: 支持动态切换模型，包括 Gemini (推荐), GPT-4o, Qwen-VL (通义千问), Doubao (豆包) 等。
- **灵活输入**: 支持 HTTP/HTTPS 图片链接或 Base64 编码的图片数据。

## 安装步骤

1. **克隆仓库:**
   ```bash
   git clone https://github.com/glasses666/mcp-image-recognition-py.git
   cd mcp-image-recognition-py
   ```

2. **创建虚拟环境 (推荐):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 用户使用: venv\Scripts\activate
   ```

3. **安装依赖:**
   ```bash
   pip install -r requirements.txt
   ```

## 配置说明

在项目根目录下创建一个 `.env` 文件（可以参考 `.env.example`）：

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

## Agent AI 配置 (如 Claude Desktop)

要将此服务器用于 MCP 客户端（例如 Claude Desktop），请将其添加到您的配置文件中（例如 `claude_desktop_config.json`）：

### 配置文件位置
- **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### 配置 JSON 示例:
**重要:** 请确保使用虚拟环境中 Python 可执行文件 (`python` 或 `python.exe`) 的**绝对路径**，以及 `server.py` 脚本的**绝对路径**。

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
*注意: 你也可以直接在 JSON 的 `env` 部分配置环境变量，这样就不依赖 `.env` 文件了。*

## 使用说明

连接成功后，服务器将提供以下工具：

### `recognize_image`
分析图像并返回文本描述。

**参数:**
- `image` (string, 必填): 要分析的图像。支持:
    - HTTP/HTTPS URL (例如 `https://example.com/cat.jpg`)
    - Base64 编码字符串 (带或不带 `data:image/...;base64,` 前缀均可)
- `prompt` (string, 选填): 具体的指令或问题。默认值: "Describe this image" (描述这张图片)。
- `model` (string, 选填): 针对本次请求指定使用的模型 (例如 `gemini-1.5-pro` 用于更复杂的推理)。如果不填则使用环境变量中的 `DEFAULT_MODEL`。

## 许可证
MIT
