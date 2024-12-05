import pickle
import sys

import matplotlib # type: ignore
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt # type: ignore

# コマンドライン引数からファイルパスとキー名を取得
if len(sys.argv) != 3:
    print("Usage: python script.py <filepath> <keyname>")
    sys.exit(1)

filepath = sys.argv[1]
keyname = sys.argv[2]

# ファイルを開いてデータを読み込み、指定されたキーのデータを表示
with open(filepath, "rb") as f:
    data = pickle.load(f)
    fig = data[keyname]
    plt.show()
