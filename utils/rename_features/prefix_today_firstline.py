import time


# ファイル名の先頭に当日（年月日）を明記する処理（※現状 add_begin_end.py モジュールにのみ実装中）
def prefix_today_firstline() -> str | None:
    try:
        prefix_today_entry = input(
            "ファイル名の先頭に当日（yyyymmdd）を表記しますか？\n`y` or `n`で入力してください："
        )

        is_prefix_today = True if prefix_today_entry == "y" else False

        # localtime()：使用している環境（地域）の設定に基づいた現在時刻を取得
        currTime = time.localtime()
        prefix_today: str = (
            f"{currTime.tm_year}{currTime.tm_mon:02d}{currTime.tm_mday:02d}_"  # 月日は 2桁ゼロ埋め
            if is_prefix_today
            else ""
        )

        return prefix_today

    except Exception as e:
        print(
            f"ファイル名先頭に当日表記する処理時にエラー発生 | `prefix_today_firstline.py` ： {e}"
        )
        return None


if __name__ == "__main__":
    prefix_today_firstline()
