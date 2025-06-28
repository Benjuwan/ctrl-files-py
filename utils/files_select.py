import glob
import os
import sys


def files_select(extends: str = "*") -> None:
    target_files = (
        glob.glob(
            # `../file/*`：全ファイル対象
            os.path.join("..", "file", extends),
            # サブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）
            recursive=True,
        )
        if len(extends) == 1
        else glob.glob(
            # `../file/*.{extends}`：指定した拡張子のファイルが処理対象
            os.path.join("..", "file", f"*.{extends}"),
            recursive=True,
        )
    )

    if len(target_files) == 0:
        # sys.exit で全体の処理中断
        sys.exit(
            f"`files_select` | ../fileフォルダまたは当該フォルダ内に「{extends}」拡張子を持つファイルが存在しません"
        )

    try:
        pass

    except Exception as e:
        print(f"処理対象ファイルを選択する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    files_select()
