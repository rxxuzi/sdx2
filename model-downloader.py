import json
import os
import requests
from tqdm import tqdm

# 設定ファイルの読み込み
with open('sdx2/civitai.json', 'r') as f:
    config = json.load(f)

# モデルリストの読み込み
with open('sdx2/models.json', 'r') as f:
    models = json.load(f)

API_KEY = config['API']
DOWNLOAD_DIR = config['DIR']

# ダウンロードディレクトリの作成（存在しない場合）
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_download_url(model_id):
    api_url = f"https://civitai.com/api/v1/models/{model_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    model_data = response.json()
    return model_data['modelVersions'][0]['files'][0]['downloadUrl']

def download_file(url, filename):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))

    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=8192):
            size = file.write(data)
            progress_bar.update(size)

def main():
    print("利用可能なモデル:")
    for i, model in enumerate(models):
        print(f"{i+1}. {model['name']} ({model['type']})")

    while True:
        choice = input("ダウンロードしたいモデルの番号を入力してください（複数選択する場合はカンマで区切ってください。全てダウンロードする場合は'all'と入力）: ")

        if choice.lower() == 'all':
            selected_models = models
            break
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                selected_models = [models[i] for i in indices]
                break
            except (ValueError, IndexError):
                print("無効な入力です。もう一度試してください。")

    for model in selected_models:
        print(f"\nモデル名: {model['name']}")
        try:
            download_url = get_download_url(model['id'])
            filename = os.path.join(DOWNLOAD_DIR, f"{model['name'].replace(' ', '_')}.safetensors")
            print(f"ダウンロードを開始します: {filename}")
            download_file(download_url, filename)
            print(f"{filename} のダウンロードが完了しました。")
        except requests.exceptions.RequestException as e:
            print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
