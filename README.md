# MB-iSTFT-VITS(日本語版)
[MB-iSTFT-VITS](https://github.com/MasayaKawamura/MB-iSTFT-VITS)の日本語版実装です．
アクセント入力に対応しています．
まだ動作検証はしていません．

<img src="./fig/proposed_model.png" width="100%">

# 使い方
## 0. 環境構築
### Python環境編
- 必要なモジュールはrequirements.txtにまとまっているはずなので，以下を実行してください．
- 特にPillowのバージョンが高すぎるとエラーが出るのでバージョンを合わせてinstallしてください
```
pip install -r requirements.txt
```
### Monotonic Alignment Search の build
- 以下を実行してください．
- 2行目は公式実装にはなかったのですが，自分の手元ではこれをやらないと動きませんでした
```
cd monotonic_align ; python setup.py build_ext --inplace ; cd -
cp monotonic_align/build/lib*/monotonic_align/ monotonic_align/ -r # 公式実装には無いので不要かもしれない
```
## 1. データセット取得
- [ここ](https://sites.google.com/site/shinnosuketakamichi/publication/jsut)からJSUTコーパスをダウンロードし，`dataset/JSUT`以下に解凍
- 前処理を実行
- 他のデータセットの場合は `dataset/JVS/main.py` を参考に実施
```
cd dataset/JSUT ; python3 preprocess.py
```

## 2. 学習
```
python3 train.py -c configs/jsut_js_istft_vits.json
```

# メモ
- 以下のエラーが出る場合，Pillowのバージョンが高すぎる可能性がある．`$ pip install Pillow==9.5.0`で解決するかもしれない．
    - `AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'`

