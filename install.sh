#!/bin/bash
echo "Installing Watchtower dependencies for Linux/Mac..."

# Update pip first
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

echo "Installation complete!"
echo ""
echo "To start Watchtower:"
echo "  python database.py"
echo "  python main.py --mode both"
