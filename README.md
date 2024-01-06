# MB-iSTFT-VITS(日本語版)
[MB-iSTFT-VITS](https://github.com/MasayaKawamura/MB-iSTFT-VITS)の日本語版実装です．
アクセント入力に対応しています．
まだ動作検証はしていません．

<img src="./fig/proposed_model.png" width="100%">

# 使い方
## 0. 準備
環境を構築する
```
pip install -r requirements.txt
```
Monotonic Alignment Search の build をする
```
cd monotonic_align && python setup.py build_ext --inplace
cd monotonic_align && cp build/lib*/monotonic_align/ ./ -r # 公式実装には無いので不要かもしれない
```


## 1. データセット取得
- JSUT の場合
    - [ここ](https://sites.google.com/site/shinnosuketakamichi/publication/jsut)からダウンロードし，`dataset/JSUT`以下に解凍
    - 前処理を実行： `$ cd dataset/JSUT ; python3 preprocess.py`
- JVS の場合
    - [ここ](hhttps://sites.google.com/site/shinnosuketakamichi/research-topics/jvs_corpu)からダウンロードし，`dataset/JVS`以下に解凍
    - 前処理を実行： `$ cd dataset/JVS ; python3 preprocess.py`
- その他の場合
    - TODO

## 2. 学習
```
python3 train.py -c configs/jsut_js_istft_vits.json
```

# 知識
- `$ pip install Pillow==9.5.0`

