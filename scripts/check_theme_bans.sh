#!/usr/bin/env bash
# scripts/check_theme_bans.sh: Enforces strict design system rules for Sticker Book Civic
set -euo pipefail

FAIL=0

echo "🔍 Scanning frontend assets for banned styles and motifs..."

# 1. Check for gradients
if grep -rn --exclude-dir=node_modules --exclude="*.log" -E "linear-gradient|radial-gradient|conic-gradient" frontend/css/ frontend/index.html; then
    echo "❌ ERROR: Gradient detected! Sticker Book Civic requires 100% flat fills."
    FAIL=1
fi

# 2. Check for glassmorphism / blur
if grep -rn --exclude-dir=node_modules -E "backdrop-filter|blur\(" frontend/css/; then
    echo "❌ ERROR: Glassmorphism / backdrop-filter detected! Flat neobrutalist cards required."
    FAIL=1
fi

# 3. Check for dark mode
if grep -rn --exclude-dir=node_modules -E "prefers-color-scheme:\s*dark|color-scheme:\s*dark" frontend/css/ frontend/index.html; then
    echo "❌ ERROR: Dark mode detected! All display modes (Normal, Sunlight, Lite) must be light paper."
    FAIL=1
fi

# 4. Check for bus / transit leftovers in user-visible HTML/JS
if grep -rn --exclude-dir=node_modules --exclude="*.log" -E "CampusHop|bus stop|🚌|mini-bus|Transit Guide" frontend/index.html frontend/js/sticker_theme.js; then
    echo "❌ ERROR: CampusHop / transit leftovers detected in user-facing code!"
    FAIL=1
fi

if [ $FAIL -eq 0 ]; then
    echo "✅ SUCCESS: All design system theme bans passed perfectly."
    exit 0
else
    echo "💥 FAILED: Please fix the theme ban violations above."
    exit 1
fi
