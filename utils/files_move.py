import os
import glob
import shutil


def files_move(move_dirname: str = "dist", replace_result_str: str | None = None):
    try:
        # `../file/*： fileフォルダ内の全ファイル`
        file_dir_path = os.path.join("../", "file", "*")
        file_dir_iter = glob.glob(file_dir_path, recursive=True)

        # 移動元フォルダパス（../file/rename）を抽出
        target_rename_dir = list(filter(lambda dir: dir.count("rename"), file_dir_iter))

        # 移動元フォルダパス（../file/rename/*）から各ファイルデータパス（イテラブル）を取得
        src_file = glob.glob(os.path.join(*target_rename_dir, "*"))

        for file in src_file:
            # ※部分置換処理の場合のみ
            # 置換対象文字が存在して、それを含んでいない場合はスキップ
            if replace_result_str is not None and file.count(replace_result_str) == 0:
                continue

            # ファイルの移動（メタデータを含む完全コピー）
            shutil.copy2(file, move_dirname)

    except Exception as e:
        print(f"フォルダ移動の処理実行エラー | {e}")
        return


if __name__ == "__main__":
    files_move()
