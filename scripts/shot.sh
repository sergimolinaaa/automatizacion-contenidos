#!/bin/bash
# uso: shot.sh in.svg out.png
/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell --no-sandbox --disable-gpu --hide-scrollbars --window-size=1000,700 --screenshot="$2" "file://$(realpath $1)" >/dev/null 2>&1
