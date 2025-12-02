#!/bin/bash

# Setup script for MCP Image Recognition Server (Linux/macOS)

echo "🚀 Setting up MCP Image Recognition Server..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check python version
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$python_version < 3.10" | bc -l) )); then
    echo "❌ Error: Python 3.10+ is required. Found Python $python_version."
    exit 1
fi

echo "✅ Python $python_version found."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "ℹ️ Virtual environment 'venv' already exists."
fi

# Activate venv and install dependencies
echo "⬇️ Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies."
    exit 1
fi

# Setup configuration
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env configuration file..."
    cp .env.example .env
    echo "✅ Created .env from template."
else
    echo "ℹ️ .env configuration file already exists."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "👉 Next steps:"
echo "1. Edit the .env file to add your API keys: nano .env"
echo "2. Run the server:"
echo "   source venv/bin/activate"
echo "   python server.py"
echo ""
echo "   Or use the absolute path in your MCP client config:"
echo "   $(pwd)/venv/bin/python"
