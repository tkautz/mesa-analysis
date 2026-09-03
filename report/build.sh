#!/usr/bin/env bash
# Render report.tex. With a TeX install: pdflatex twice. Without one (this session): pandoc -> HTML -> Chromium PDF.
set -e; cd "$(dirname "$0")"
if command -v pdflatex >/dev/null; then pdflatex -interaction=nonstopmode report.tex && pdflatex -interaction=nonstopmode report.tex; exit 0; fi
PANDOC=${PANDOC:-pandoc}
$PANDOC report.tex -f latex -t html5 --standalone --embed-resources --mathml --toc --resource-path=.:../figures --metadata title="Enrollment uncertainty and the proposed closure of Mesa Elementary" \
  --css=report.css -o report.html
CHROME=${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}
"$CHROME" --headless --disable-gpu --no-sandbox --print-to-pdf=report.pdf --no-pdf-header-footer "file://$PWD/report.html" 2>/dev/null
echo "wrote report.html and report.pdf"
