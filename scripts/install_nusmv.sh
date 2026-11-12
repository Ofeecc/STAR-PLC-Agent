#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
root_dir="$(cd -- "$script_dir/.." && pwd)"
target_root="$root_dir/.local/model_checkers"
target_dir="$target_root/NuSMV-2.7.1-linux64"
archive="$target_root/nusmv-2.7.1-3-x86_64.pkg.tar.zst"
url="${NUSMV_LINUX_URL:-https://mirrors.cernet.edu.cn/archlinuxcn/x86_64/nusmv-2.7.1-3-x86_64.pkg.tar.zst}"

mkdir -p "$target_dir"
curl -fL --retry 2 -o "$archive" "$url"
tar --use-compress-program=zstd -xf "$archive" -C "$target_dir"
rm -f "$archive"
if [ -x "$target_dir/usr/bin/NuSMV" ]; then
  ln -sf NuSMV "$target_dir/usr/bin/nusmv"
fi

echo "NuSMV executable:"
find "$target_dir" -maxdepth 4 -type f -name 'NuSMV'
