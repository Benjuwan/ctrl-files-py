import glob
import os
import sys

from entry_validation import check_entry_count
from check_and_create_move_dir import check_and_create_move_dir
from files_select import files_select
from rename_file_act_regular import rename_file_act_regular
from check_max_depth_dir import get_max_depth_dirpath_files


def rename_files(mode: str = "") -> None:
    try:
        entry_replace_str = input("1. リネーム前の対象文字列を入力：")
        check_entry_count("リネーム前の対象文字列", entry_replace_str)

        entry_target_str = input("2. リネーム名を入力：")
        check_entry_count("リネーム名", entry_target_str)

        # （../file という）パス文字列として正しく認識してもらうために os.path.join で文字列結合する
        file_dir = os.path.join("..", "file")

        target_files = glob.glob(
            # ../file/*： fileフォルダ内の全ファイル（/*：ワイルドカード）指定というパス文字列
            os.path.join(file_dir, "*"),
            # サブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）
            recursive=True,
        )

        # 最深階層まで検出するようにパス指定した（調整された）イテラブル
        max_depth_dirpath_files = get_max_depth_dirpath_files(file_dir)

        if max_depth_dirpath_files:
            # リネーム前の対象文字列を含んだフォルダまたはファイルが存在するかをチェックする
            is_check_exist_target_file = all(
                [file.count(entry_replace_str) == 0 for file in max_depth_dirpath_files]
            )

        if is_check_exist_target_file:
            sys.exit(
                f"現状「{entry_replace_str}」というフォルダまたはファイル名のデータは存在しないようです"
            )

        if len(target_files) == 0:
            print(
                f"`rename_files` | {file_dir}フォルダまたは当該フォルダ内にファイルが存在しません"
            )

            # ルートに file_dir フォルダが存在しない場合のみ作成
            if os.path.exists(file_dir) is False:
                os.mkdir(file_dir)

            return

        if mode == "all":
            file_dir_path: str | None = check_and_create_move_dir(
                entry_replace_str, entry_target_str, mode
            )

            filtered_extend_files: list[str] | None = files_select(
                entry_replace_str, entry_target_str, mode
            )

            if isinstance(file_dir_path, str) and isinstance(
                filtered_extend_files, list
            ):
                # 拡張子でのフィルター済みイテラブルをセット
                target_files = filtered_extend_files
                # 移動先フォルダパスをリストの先頭に追加
                target_files.insert(0, file_dir_path)

            rename_file_act_regular(
                target_files, "", entry_replace_str, entry_target_str, mode
            )
        elif mode == "dir_move":
            check_and_create_move_dir(entry_replace_str, entry_target_str, mode)
        elif mode == "files_select":
            filtered_files_select: list[str] | None = files_select(
                entry_replace_str, entry_target_str, mode
            )

            if isinstance(filtered_files_select, list):
                # 拡張子でのフィルター済みイテラブルをセット
                target_files = filtered_files_select

            rename_file_act_regular(
                target_files, "", entry_replace_str, entry_target_str, mode
            )
        else:
            # entry_target_str を渡して、部分置換モードで処理を進める
            rename_file_act_regular(
                target_files, "", entry_replace_str, entry_target_str
            )

    except Exception as e:
        print(f"リネーム処理の実行エラー | `rename_files.py` ： {e}")
        return


if __name__ == "__main__":
    rename_files()
