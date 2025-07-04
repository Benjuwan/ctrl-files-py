import os
import glob
import sys

from entry_validation import check_entry_count

"""
- Notice
utils/move_dirs.py 内に記述して（関係する関数をまとめて）しまうと、機能（またはモジュールの読み込み処理が）競合するのか ModuleNotFoundError が発生するため別のモジュールとして分離させた
"""


def check_and_create_move_dir(
    entry_replace_str: str | None = None,
    entry_target_str: str | None = None,
    mode: str = "dir_move",
) -> str | None:
    from rename_file_act_regular import rename_file_act_regular

    if entry_replace_str is None:
        entry_replace_str = input("1. リネーム前の対象文字列を入力：")
        check_entry_count("リネーム前の対象文字列", entry_replace_str)

    if entry_target_str is None:
        entry_target_str = input("2. リネーム名を入力：")
        check_entry_count("リネーム名", entry_target_str)

    try:
        dirname = input("移動先フォルダ名を入力：")
        check_entry_count("移動先フォルダ名", dirname)

        # `../file/{dirname}`というパス文字列として正しく認識してもらうために os.path.join で文字列結合する
        file_dir = os.path.join("..", "file", dirname)
        target_files = glob.glob(file_dir, recursive=True)

        if len(target_files) == 0:
            print(
                f"`check_and_create_move_dir` | 処理対象フォルダ「{dirname}」が存在しません"
            )

            # ルートに file_dir フォルダが存在しない場合のみ作成
            if os.path.exists(f"{file_dir}") is False:
                # 再帰的にディレクトリを作成（※指定したフォルダ構成通りに作成してくれる）
                os.makedirs(f"{file_dir}")

            sys.exit(f"「{dirname}」を作成したので再実行してください")

        # 「モード：フォルダ移動 + ファイル選択 + リネーム」の場合、移動先フォルダパスを返す
        if mode == "all":
            return file_dir

        # target_files（`../file/{dirname}`内のデータイテラブル）を渡して、部分置換モードで処理を進める
        rename_file_act_regular(
            target_files, "", entry_replace_str, entry_target_str, mode
        )

        return None

    except Exception as e:
        print(f"移動先フォルダのチェック及び作成処理における実行エラー | {e}")
        return None


if __name__ == "__main__":
    check_and_create_move_dir()
