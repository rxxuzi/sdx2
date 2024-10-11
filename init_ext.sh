#!/bin/bash

# 移動先のディレクトリを指定
DIRS=("sd" "extensions")

# 各ディレクトリに対して cd を実行
for DIR in "${DIRS[@]}"; do
  cd "$DIR" || { echo "Error: Failed to change directory to $DIR"; exit 1; }
done

# ディレクトリ移動に成功した場合のみ、以下のクローン操作を実行
echo "Cloning repositories..."

git clone https://github.com/KohakuBlueleaf/a1111-sd-webui-lycoris
git clone https://github.com/Bing-su/adetailer.git
git clone https://github.com/hako-mikan/sd-webui-regional-prompter.git
git clone https://github.com/AlUlkesh/stable-diffusion-webui-images-browser.git

echo "Repositories cloned successfully."
