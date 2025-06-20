import glob
import os


def files_select(extends: str = "") -> None:
    target_files_dir = glob.glob(
        # `../file/*.{extends}`というパス文字列として正しく認識してもらうために os.path.join で文字列結合する
        os.path.join("..", "file", f"*.{extends}"),
        # サブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）
        recursive=True,
    )
    if len(target_files_dir) == 0:
        print(
            f"`files_select` | ../fileフォルダまたは当該フォルダ内に「{extends}」拡張子を持つファイルが存在しません"
        )
        return

    try:
        pass

    except Exception as e:
        print(f"処理対象ファイルを選択する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    files_select()
