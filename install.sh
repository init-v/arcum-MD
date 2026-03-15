#!/usr/bin/env bash
set -e

echo ""
echo "  Installing Arcum MD..."
echo ""

# Check Python version
PYTHON=$(command -v python3 || command -v python || true)

if [ -z "$PYTHON" ]; then
  echo "  ✗ Python not found. Install Python 3.10+ from https://python.org and re-run."
  exit 1
fi

VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")

if [ "$MAJOR" -lt 3 ] || { [ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]; }; then
  echo "  ✗ Python $VERSION found, but 3.10+ is required."
  echo "    Download from https://python.org"
  exit 1
fi

echo "  ✓ Python $VERSION"

# Upgrade pip and setuptools silently
$PYTHON -m pip install --upgrade pip setuptools wheel --quiet

# Install the package and all dependencies
$PYTHON -m pip install -e . --quiet

echo ""
echo "  ✓ Arcum MD installed."
echo ""
echo "  Try it:"
echo "    arcum --help"
echo "    arcum convert yourfile.pdf"
echo ""
