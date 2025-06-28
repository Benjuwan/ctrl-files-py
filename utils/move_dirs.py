import os
import glob
import sys
import shutil


def check_and_create_move_dir(dirname: str = "rename") -> None:
    try:
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

            # sys.exit で全体の処理中断
            sys.exit(f"「{dirname}」を作成したので再実行してください")

    except Exception as e:
        print(f"移動先フォルダのチェック及び作成処理における実行エラー | {e}")
        return


def move_dir(
    target_file_dir: list[str] | None = None, rename_files: list[str] | None = None
):
    if target_file_dir is None or rename_files is None:
        return

    try:
        move_target_dir = target_file_dir[1]
        src_file = rename_files

        for file in src_file:
            # shutil.move(file, move_target_dir)
            shutil.copy2(file, move_target_dir)

    except Exception as e:
        print(f"フォルダ移動の処理実行エラー | {e}")
        return


if __name__ == "__main__":
    check_and_create_move_dir()
    move_dir()
