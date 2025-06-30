from rename_files import rename_files
from files_select import files_select
from move_dirs import check_and_create_move_dir


def run() -> None:
    try:
        entry_replace_str = input("1. リネーム前の対象文字列を入力：")
        entry_target_str = input("2. リネーム名を入力：")
        entry_move_dir = input(
            "3. （任意）移動先フォルダを入力 ---\n処理不要の場合は enterキーを押下："
        )
        entry_file_select = input(
            "4. （任意）処理対象ファイルの拡張子を入力 ---\n処理不要の場合は enterキーを押下："
        )

        is_allow_rename = (
            len(entry_replace_str) > 0 and isinstance(entry_replace_str, str)
        ) and (len(entry_target_str) > 0 and isinstance(entry_target_str, str))

        if is_allow_rename is False:
            print(
                f"--- リネーム処理「{entry_replace_str}」->「{entry_target_str}」は必ず入力してください"
            )
            return

        is_allow_move_dir = len(entry_move_dir) > 0 and isinstance(entry_move_dir, str)
        is_allow_file_select = len(entry_file_select) > 0 and isinstance(
            entry_file_select, str
        )
        is_allow_all_feature = (
            is_allow_rename and is_allow_move_dir and is_allow_file_select
        )

        if is_allow_all_feature:
            print(
                f"--- 1.すべての処理（リネーム：{entry_replace_str} -> {entry_target_str} + フォルダ移動：{entry_move_dir} + 指定したファイル：{entry_file_select}）"
            )
            check_and_create_move_dir(entry_move_dir)
            files_select(entry_file_select, entry_replace_str)
        elif is_allow_rename and is_allow_move_dir:
            print(
                f"--- 2.特定処理（リネーム：{entry_replace_str} -> {entry_target_str} + フォルダ移動：{entry_move_dir}）"
            )
            check_and_create_move_dir(entry_move_dir)
            rename_files(entry_replace_str, entry_target_str)
        elif is_allow_rename and is_allow_file_select:
            print(
                f"--- 3.特定処理（リネーム：{entry_replace_str} -> {entry_target_str} + 指定したファイル：{entry_file_select}）"
            )
            files_select(entry_file_select, entry_replace_str)
        elif is_allow_rename:
            print(
                f"--- 4.特定処理（リネーム：{entry_replace_str} -> {entry_target_str}）"
            )
            rename_files(entry_replace_str, entry_target_str)
        else:
            print("5.リネーム名を入力してください")

    except Exception as e:
        print(f"コアモジュール main.py での処理実行エラー | {e}")
        return


run()

print("Done | すべての処理が完了しました.")
