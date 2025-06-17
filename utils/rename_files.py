import glob

from rename_files_sys import rename_files_sys


def rename_files():
    # 指定したパス（※ファイルやディレクトリの場所を指す文字列）にあるファイルの一覧を取得する
    # 返り値はファイル一覧のリスト形式（イテラブル）となる
    # 今回はサブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）とする
    target_files_dir = glob.glob("../file", recursive=True)
    if len(target_files_dir) == 0:
        print("対象ファイルが存在しません")

    rename_files_sys(target_files_dir)


if __name__ == "__main__":
    rename_files()
