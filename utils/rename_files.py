import glob
import os

from rename_files_sys import rename_files_sys


def rename_files(entry_replace_str: str = "", entry_target_str: str = "") -> None:
    # （../file という）パス文字列として正しく認識してもらうために os.path.join で文字列結合する
    file_dir = os.path.join("..", "file")

    target_files = glob.glob(
        # ../file/*： fileフォルダ内の全ファイル（/*：ワイルドカード）指定というパス文字列
        os.path.join(file_dir, "*"),
        # サブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）
        recursive=True,
    )

    if len(target_files) == 0:
        print(
            f"`rename_files` | {file_dir}フォルダまたは当該フォルダ内にファイルが存在しません"
        )

        # ルートに file_dir フォルダが存在しない場合のみ作成
        if os.path.exists(file_dir) is False:
            os.mkdir(file_dir)

        return

    try:
        rename_files_sys(target_files, entry_replace_str, entry_target_str)

    except Exception as e:
        print(f"リネーム処理の実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_files()
