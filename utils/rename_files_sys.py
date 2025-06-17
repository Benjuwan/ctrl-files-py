import sys
import os
import glob


def _rename_file_act_alt(
    target_files: list[str], numbering: str, replace_str: str, is_begin: bool = True
) -> None:
    # ナンバリング有りver
    if len(numbering) > 0:
        for i, file in enumerate(target_files):
            # ファイル名の変更
            os.rename(
                file,
                f"{i}-{replace_str}-{file}"
                if numbering == "y"
                else f"{file}-{replace_str}-{i}",
            )
        return  # 無用な後続処理を避けるため明示的に処理終了

    for file in target_files:
        adjust_filename = (
            f"{replace_str}-{file}" if is_begin else f"{file}-{replace_str}"
        )
        os.rename(file, adjust_filename)
    return


def _rename_file_act(
    target_files: list[str],
    numbering: str,
    replace_str: str,
    target_str: str | None = None,
) -> None:
    # all：ナンバリング有りver
    if len(numbering) > 0:
        for i, file in enumerate(target_files):
            # ファイル名の変更
            os.rename(
                file, f"{i}-{replace_str}" if numbering == "y" else f"{replace_str}-{i}"
            )
        return  # 無用な後続処理を避けるため明示的に処理終了

    # part：ナンバリング有りver
    if len(numbering) > 0 and target_str is not None:
        for i, file in enumerate(target_files):
            adjust_filename = file.replace(target_str, replace_str)
            os.rename(
                file,
                f"{i}-{adjust_filename}"
                if numbering == "y"
                else f"{adjust_filename}-{i}",
            )
        return

    # part：ナンバリング無しver
    if target_str is not None:
        for file in target_files:
            adjust_filename = file.replace(target_str, replace_str)
            os.rename(file, adjust_filename)
        return

    # all：ナンバリング無しver
    else:
        for file in target_files:
            os.rename(file, replace_str)
        return


def rename_files_sys(target_files_dir: list[str] | None = None):
    """
    # 指定した位置（インデックス）の値を取得
    # sys.argv[0]  # プログラム名
    # sys.argv[1]  # 第一引数：モード（ all, part, add_begin, add_end ）
    """

    # ----- main.py 経由の処理ルート
    if target_files_dir is not None:
        if len(target_files_dir) == 0:
            sys.exit("処理対象フォルダまたはファイルが存在しないようです")

        replace_str = input(
            f"「{target_files_dir}」フォルダ内の全ファイル名を入力文字で置換："
        )
        target_str = input(
            f"「{target_files_dir}」フォルダ内の全ファイル名の置換対象となる文字列を入力："
        )
        _rename_file_act(target_files_dir, "", replace_str, target_str)
        return

    # ----- rename_files_sys.py 単体実行の処理ルート
    # 以下のコマンドライン引数の場合、入力文字に応じた処理を実行する
    com_lists = ["all", "part", "add_begin", "add_end"]
    attention_com_lists = f"実行可能コマンドは{com_lists}です"

    print(sys.argv)
    # 入力したコマンドライン引数が1つ未満（※何も入力せずとも[0]にはファイル名が入る）または1つ以上の場合
    if len(sys.argv) != 2 or len(sys.argv) > 2:
        print(f"1つのコマンドライン引数を入力してください\n{attention_com_lists}")
        return

    # com_lists 内の文字列でない場合
    elif sys.argv[1] not in com_lists:
        print(f"{sys.argv[1]} は実行コマンドに含まれていません\n{attention_com_lists}")

    mode = sys.argv[1]
    rename_files = glob.glob("../rename")
    if len(rename_files) == 0:
        print("renameフォルダが存在しないか、フォルダ内にデータが用意されていません")
        return

    numbering = input(
        "（任意）ファイルをナンバリングする\n`n-`ファイル名：先頭に追加する場合は「y」と入力\nファイル名`-n`：末尾に追加する場合は「n」と入力\n不要の場合は何も入力せず enterキーを押下："
    )
    if mode == "all":
        replace_all_str = input("入力した文字列で全置換：")
        _rename_file_act(rename_files, numbering, replace_all_str)

    elif mode == "part":
        replace_str = input("置換結果となる文字列：")
        target_str = input("置換したいファイル名の文字列：")
        _rename_file_act(rename_files, numbering, replace_str, target_str)

    elif mode == "add_begin":
        add_begin_str = input("ファイル名の先頭に追加したい文字列：")
        _rename_file_act_alt(rename_files, numbering, add_begin_str)

    elif mode == "add_end":
        add_end_str = input("ファイル名の末尾に追加したい文字列：")
        _rename_file_act_alt(rename_files, numbering, add_end_str, is_begin=False)


if __name__ == "__main__":
    rename_files_sys()
