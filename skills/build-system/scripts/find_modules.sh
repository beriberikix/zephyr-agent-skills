#!/bin/bash
# find_modules.sh - Identifies required modules from a Zephyr build directory
# Inspired by Golioth's "What modules should you add to a manifest allow list?"

BUILD_DIR=${1:-build}

if [ ! -d "$BUILD_DIR/modules" ]; then
    echo "❌ Error: $BUILD_DIR/modules directory not found."
    echo "Usage: ./find_modules.sh [build_directory]"
    exit 1
fi

echo "🔍 Scanning modules in $BUILD_DIR/modules..."
# List module directories directly instead of parsing file paths
find "$BUILD_DIR/modules" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort

echo -e "\n✅ Above is the list of modules that produced output in this build."
echo "You can add these to your manifest's 'name-allowlist' to optimize checkouts."
