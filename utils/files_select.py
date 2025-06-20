import glob


def files_select(extends: str = "") -> None:
    # * でワイルカード指定
    # サブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）
    target_files_dir = glob.glob(f"../file/*.{extends}", recursive=True)
    if len(target_files_dir) == 0:
        print(f"`files_select` | 「{extends}」拡張子を持つファイルが存在しません")
        return

    try:
        pass

    except Exception as e:
        print(f"処理対象ファイルを選択する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    files_select()
