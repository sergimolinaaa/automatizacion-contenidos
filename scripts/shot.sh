#!/bin/bash
# uso: shot.sh in.svg out.png
"$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-*/headless_shell | sort -r | head -1)" --no-sandbox --disable-gpu --hide-scrollbars --window-size=1000,700 --screenshot="$2" "file://$(realpath $1)" >/dev/null 2>&1
