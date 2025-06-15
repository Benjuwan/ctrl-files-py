import glob
import sys
import os


def _rename_file_act_alt(
    target_files: str, numbering: str, replace_str: str, is_begin: bool = True
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
    target_files: str,
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


def rename_files_sys():
    """
    # 指定した位置（インデックス）の値を取得
    # sys.argv[0]  # プログラム名
    # sys.argv[1]  # 第一引数：モード（ all, part, add_begin, add_end ）
    """
    com_lists = ["all", "part", "add_begin", "add_end"]

    print(sys.argv)
    # コマンドライン引数が2つ未満または com_lists 内の文字列でない場合は早期終了
    if len(sys.argv) < 2 or sys.argv[1] not in com_lists:
        print(
            "コマンドライン引数が2つ未満または所定コマンド（ all, part, add_begin, add_end ）が入力されていません"
        )
        return

    mode = sys.argv[1]
    rename_files = glob.glob("../rename")
    print(rename_files)
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


def rename_files():
    rename_files_sys()

    # 指定したパス（※ファイルやディレクトリの場所を指す文字列）にあるファイルの一覧を取得する
    # 返り値はファイル一覧のリスト形式（イテラブル）となる
    # 今回はサブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）とする
    target_files_dir = glob.glob("../file", recursive=True)
    if len(target_files_dir) == 0:
        print("対象ファイルが存在しません")


if __name__ == "__main__":
    rename_files()
