#!/usr/bin/env bash
set -e

VENV_DIR=".venv"

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

# Wipe existing venv so we always start clean
if [ -d "$VENV_DIR" ]; then
  echo "  Removing existing virtual environment for a clean install..."
  rm -rf "$VENV_DIR"
fi

# Clear pip cache to avoid reusing corrupted downloads
$PYTHON -m pip cache purge --quiet 2>/dev/null || true

# Create virtual environment
echo "  Creating virtual environment..."
$PYTHON -m venv "$VENV_DIR"

# Use the venv's pip and python from here on
PIP="$VENV_DIR/bin/pip"
PYTHON="$VENV_DIR/bin/python"

# Upgrade pip and setuptools — no cache to avoid stale wheels
$PIP install --no-cache-dir --upgrade pip setuptools wheel --quiet

# Install the package and all dependencies — no cache
echo "  Installing dependencies (this may take a few minutes on first run)..."
$PIP install --no-cache-dir -e . --quiet

echo ""
echo "  ✓ Arcum MD installed."
echo ""
echo "  To use it, activate the environment first:"
echo ""
echo "    source .venv/bin/activate"
echo "    arcum --help"
echo "    arcum convert yourfile.pdf"
echo ""
echo "  Or run it directly without activating:"
echo ""
echo "    .venv/bin/arcum convert yourfile.pdf"
echo ""
