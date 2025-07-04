import glob
import os
import sys

# rename_features. からの相対パスでないと ModuleNotFoundError が発生する
from rename_features.regular_part import regular_part_numbering
from rename_features.regular_part import regular_part
from rename_features.regular_all import regular_all_numbering
from rename_features.regular_all import regular_all


# モード：all, part ルート時におけるリネーム処理
def rename_file_act_regular(
    target_file_dir: list[str] | None = None,
    numbering: str = "",
    replace_str: str = "",
    target_str: str | None = None,
    mode: str = "",
) -> None:
    if target_file_dir is None:
        print(
            "処理対象フォルダが指定されていないようです\n処理する場合は rename_files_sys.py を通じて実行してください "
        )
        return

    try:
        is_mode_all: bool = mode == "all"
        is_files_select: bool = mode == "files_select"
        is_mode_dir_move: bool = mode == "dir_move"

        # フォルダ移動処理の場合は`../file/rename`ディレクトリパスとイテラブルを用意
        if is_mode_dir_move:
            dir_move_rename_dir_path = os.path.join("../", "file", "rename")
            dir_move_rename_dir = glob.glob(dir_move_rename_dir_path, recursive=True)

        # file ディレクトリ配下のフォルダから rename（処理対象ディレクトリ）という文字列を含んだフォルダまたはファイルリストを取得
        target_rename_dir = list(
            # filter(関数, イテラブル)
            filter(
                # lambda 引数: 式
                lambda dir: dir.count("rename"),
                # フォルダ移動処理の場合は dir_move_rename_dir （`../file/rename`イテラブル）を指定
                # このルートの場合 target_file_dir には移動先フォルダ名が入っているので上書きはNG
                dir_move_rename_dir if is_mode_dir_move else target_file_dir,
            )
        )

        # 処理対象ディレクトリ内の全てのファイルリスト（以下の内包表記からうまれるイテラブル）
        rename_files = [
            f  # 式：ループ変数fをそのまま取得
            for f  # ループ変数：glob結果の各要素（target_file_dirフォルダ内の全データ）を順次取得
            # アンパック（*イテラブル）： JavaScriptのスプレッド構文（...）と同じようにリストやタプルの中身を展開して渡す仕組み
            in glob.glob(os.path.join(*target_rename_dir, "*"))
            # isfile：対象がファイルかどうかを判定（ディレクトリを除外してファイルのみを抽出）
            if os.path.isfile(f)
        ]

        # ファイル選択処理または全モードの場合はそのまま target_rename_dir（拡張子でのフィルター済みイテラブル）を処理対象にする
        if is_files_select or is_mode_all:
            rename_files = target_rename_dir

        if is_mode_all is False and len(rename_files) == 0:
            print(f"{target_rename_dir}内のファイルは現在「{len(rename_files)}」件です")
            return

        is_replace_str = len(replace_str) == 0
        if is_replace_str:
            print("リネーム対象文字列が未入力なようです")
            return

        is_check_correct_numbering_code = numbering == "y" or numbering == "n"
        is_add_numbering = len(numbering) > 0 and is_check_correct_numbering_code

        if len(numbering) > 0 and is_check_correct_numbering_code is False:
            sys.exit(
                f"\n処理受付可能なコードは「y」または「n」のみです\n入力されたコードは「{numbering}」なので処理を中断します\n"
            )

        run_move_dir: bool = is_mode_all or is_mode_dir_move

        # part：ナンバリング有りver
        if is_add_numbering and target_str is not None:
            regular_part_numbering(
                numbering,
                target_str,
                target_file_dir,
                rename_files,
                replace_str,
                run_move_dir,
            )
            return  # 以降の処理を実行させないように処理終了

        # part：ナンバリング無しver
        if target_str is not None:
            regular_part(
                target_str,
                target_file_dir,
                rename_files,
                replace_str,
                run_move_dir,
            )
            return  # 以降の処理を実行させないように処理終了

        # all：ナンバリング有りver
        if is_add_numbering:
            regular_all_numbering(
                numbering,
                target_file_dir,
                rename_files,
                replace_str,
                run_move_dir,
            )
            return  # 以降の処理を実行させないように処理終了

        # all：ナンバリング無しver
        regular_all(
            target_file_dir,
            rename_files,
            replace_str,
            run_move_dir,
        )

    except Exception as e:
        print(f"ファイル名の置換処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_file_act_regular()
