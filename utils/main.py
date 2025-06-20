def run() -> None:
    try:
        entry_rename_target = input(
            "1. リネーム前の対象文字列を入力\n例：ページ -> page の場合「ページ」と入力："
        )
        entry_rename_src = input(
            "2. リネーム名を入力\n例：例：ページ -> page の場合「page」と入力："
        )
        entry_move_dir = input(
            "3. （任意）移動先フォルダを入力：\n処理不要の場合は enterキーを押下："
        )
        entry_file_select = input(
            "4. （任意）処理対象ファイルの拡張子を入力：\n処理不要の場合は enterキーを押下："
        )

        is_allow_rename = (
            len(entry_rename_target) > 0 and isinstance(entry_rename_target, str)
        ) and (len(entry_rename_src) > 0 and isinstance(entry_rename_src, str))

        if is_allow_rename is False:
            print(
                f"--- リネーム処理「{entry_rename_target}」->「{entry_rename_src}」は必ず入力してください"
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
                f"--- 1.すべての処理（リネーム：{entry_rename_target} -> {entry_rename_src} + フォルダ移動：{entry_move_dir} + 指定したファイル：{entry_file_select}）"
            )
        elif is_allow_rename and is_allow_move_dir:
            print(
                f"--- 2.特定処理（リネーム：{entry_rename_target} -> {entry_rename_src} + フォルダ移動：{entry_move_dir}）"
            )
        elif is_allow_rename and is_allow_file_select:
            print(
                f"--- 3.特定処理（リネーム：{entry_rename_target} -> {entry_rename_src} + 指定したファイル：{entry_file_select}）"
            )
        elif is_allow_rename:
            print(
                f"--- 4.特定処理（リネーム：{entry_rename_target} -> {entry_rename_src}）"
            )
        else:
            print("5.リネーム名を入力してください")

    except Exception as e:
        print(f"コアモジュール main.py での処理実行エラー | {e}")
        return


run()
print("run 終了.")
