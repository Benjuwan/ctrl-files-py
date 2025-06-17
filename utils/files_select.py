import glob


def files_select(extends: str = ""):
    # * でワイルカード指定
    # サブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）
    glob.glob(f"../file/*.{extends}", recursive=True)


if __name__ == "__main__":
    files_select()
