import glob
# import os
# import shutil


def move_dirs(dirname: str = "") -> None:
    target_files_dir = glob.glob(f"{dirname}", recursive=True)
    if len(target_files_dir) == 0:
        print(f"`rename_files` | 対象フォルダ「{dirname}」が存在しません")
        return

    try:
        pass

        # 完全なファイルコピー
        # shutil.copy2(コピー元, コピー先)

        # ファイルの移動
        # shutil.move(移動元, 移動先)

    except Exception as e:
        print(f"フォルダ移動の処理実行エラー | {e}")
        return


if __name__ == "__main__":
    move_dirs()
