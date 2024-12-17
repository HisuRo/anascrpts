import pickle
import sys
import argparse

import matplotlib # type: ignore
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt # type: ignore

from matplotlib.colors import Normalize, LogNorm  # type: ignore
from matplotlib.widgets import RadioButtons  # type: ignore

# ArgumentParserを作成
parser = argparse.ArgumentParser(description="Process input file and keynames.")

# 必須の引数
parser.add_argument('input', type=str, help='Input file path')
parser.add_argument('keyname', type=str, help='Keyname of figure')

# オプション引数 -c または --cmap
parser.add_argument('-c', '--cmap', action='store_true', help='for colormap plot. If specified, requires 3 additional keynames')

# 追加のkeyname引数（-c/--cmap指定時のみ必要）
parser.add_argument('keyname_pcm', type=str, nargs="?", help='Keyname of pcolormesh object')
parser.add_argument('keyname_cbar', type=str, nargs="?", help='Keyname of colorbar object')
parser.add_argument('keyname_data', type=str, nargs="?", help='Keyname of data')

args = parser.parse_args()

filepath = args.input
keyname = args.keyname
iscmap = args.cmap

# -c/--cmap が指定された場合、追加のkeynameをチェック
if args.cmap:
    keyname_pcm = args.keyname_pcm
    keyname_cbar = args.keyname_cbar
    keyname_data = args.keyname_data
    if not (args.keyname_pcm and args.keyname_cbar and args.keyname_data):
        print("Error: --cmap requires keyname_pcm, keyname_cbar, and keyname_data to be specified.")
        sys.exit(1)

# ファイルを開いてデータを読み込み、指定されたキーのデータを表示
with open(filepath, "rb") as f:
    data = pickle.load(f)
    fig = data[keyname]
    if iscmap:
        pcm = data[keyname_pcm]
        cbar = data[keyname_cbar]
        d = data[keyname_data]
        # 初期設定
        current_norm = Normalize(vmin=d.min(), vmax=d.max())  # 初期は線形

        # 描画のセットアップ
        fig.subplots_adjust(left=0.3, right=0.95)  # スペースを確保

        # ラジオボタンでスケールを選択
        ax_scale = fig.add_axes([0.05, 0.3, 0.10, 0.15], frameon=True)
        scale_selector = RadioButtons(ax_scale, labels=['Linear', 'Log'], active=0)


        def update_scale(label):
            """スケールを変更してプロットを更新"""
            global current_norm
            if label == 'Linear':
                current_norm = Normalize(vmin=d.min(), vmax=d.max())
            elif label == 'Log':
                current_norm = LogNorm(vmin=d.min(), vmax=d.max())

            pcm.set_norm(current_norm)
            cbar.update_normal(pcm)  # カラーバーを更新
            fig.canvas.draw_idle()

        scale_selector.on_clicked(update_scale)
    
    plt.show()
