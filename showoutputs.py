import pickle
import pprint
import argparse

def main():
    # ArgumentParserを作成
    parser = argparse.ArgumentParser(description="Process input file and keynames.")

    # 必須の引数
    parser.add_argument('input', type=str, help='Input file path')

    args = parser.parse_args()

    filepath = args.input
    keynames = []

    # ファイルを開いてデータを読み込み、指定されたキーのデータを表示
    with open(filepath, "rb") as f:
        data = pickle.load(f)
        pprint.pprint(data, width=50, sort_dicts=False)


if __name__ == "__main__":
	main()