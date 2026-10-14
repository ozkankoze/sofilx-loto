#!/bin/sh
# Tüm siteyi baştan üretir: TR sayfalar -> diller -> SEO son dokunuş -> önizleme
set -e
cd "$(dirname "$0")/.."
python3 tools/build.py
python3 tools/i18n.py apply
python3 tools/i18n.py fit_tr
python3 tools/seo_post.py
python3 tools/offline.py
