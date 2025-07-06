import os
import glob


# 対象フォルダ内の最深下層（数値）を取得
def _get_max_depth(root_dir: str) -> int:
    # 最深下層（数値）を管理するための変数
    max_depth = 0

    # イテラブル変数は3つ必要： 現在のディレクトリパス, サブディレクトリ名リスト, ファイル名リスト
    # os.walk： 引数に指定したディレクトリパス内を探索して、それぞれ上記3つのデータを検出する
    for dirpath, _dirnames, _filenames in os.walk(root_dir):
        # os.path.relpath： 引数に指定したディレクトリパスと、各ディレクトリパスの相関性をチェックして相対パスを取得
        rel_path = os.path.relpath(dirpath, root_dir)

        # 兄弟関係＝ルート（`./dirpath`）の場合は同階層として扱う
        if rel_path == ".":
            depth = 0

        # そうでない場合は階層を分けて階層数値を取得
        #  rel_path.count(os.sep) + 1： os.sep（`/`： ディレクトリパスの区切り文字）をカウント。ルートからの位置とするため1つ加算しておく
        else:
            depth = rel_path.count(os.sep) + 1

        # 最深下層を随時更新
        if depth > max_depth:
            max_depth = depth

    return max_depth


# 最深階層まで検出するようにパス指定したイテラブルを生成及び返却
def get_max_depth_dirpath_files(file_dir: str | None = None) -> list[str] | None:
    if file_dir is None:
        return None

    # 最深階層を取得
    max_depth: int = _get_max_depth(file_dir)

    # パターンを動的生成
    # 1. `../file/` +
    # 2. os.sep（`/`： ディレクトリパスの区切り文字） +
    # 3. "*/" * max_depth： 最深下層までのディレクトリをワイルドカード（全対象）指定
    # 4. "*"： 各ディレクトリファイルをワイルドカード（全対象）指定
    pattern: str = file_dir + os.sep + ("*/" * max_depth) + "*"

    # Windows対策でパスを正規化（ノーマライズ）
    pattern = os.path.normpath(pattern).replace("\\", "/")

    # 最深階層まで検出するようにパス指定した（調整された）イテラブル
    max_depth_dirpath_files: list[str] = glob.glob(pattern, recursive=True)

    return max_depth_dirpath_files


if __name__ == "__main__":
    get_max_depth_dirpath_files()
