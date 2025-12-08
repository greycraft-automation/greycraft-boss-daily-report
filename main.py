# Greycraft 旅館每日營收快報 Demo - 使用 2024/12 Excel
# xx旅館（xx館）專用版本 v0.9
#
# 功能：
#   - 讀取xx旅館「2024/12 收支日報表」中的某一天分頁
#   - 計算：
#       * 本日實際收款總額（以 M 欄「金額」為準）
#       * 入住間數（依房號）
#       * 國籍統計
#       * 來源統計
#   - 輸出一段給老闆看的中文摘要文字
#
# 收款金額規則：
#   1) 優先讀 L 欄為「本日總額」那一列的 M 欄金額
#   2) 若該列沒有數字，退回：
#        有房號 & 非「待收款」的明細列 M 欄加總
#   3) 不直接使用 N 欄金額（視為備註 / 拆帳說明）

from datetime import date
from typing import Tuple

import pandas as pd

# === 可調整常數 ===
HOTEL_NAME = "xxx旅館"
YEAR = 2024
MONTH = 12
XLSX_PATH = "hotel_2024_12.xlsx"

# 開發時若需要看細節可以改成 True
DEBUG = False


def read_hotel_daily_stats(xlsx_path: str, sheet_name: str) -> Tuple[int, int, pd.Series, pd.Series]:
    """
    從指定分頁（例如 "1" ~ "31"）讀取每日收支表，計算：

      - total_amount：本日實際收款總額
      - room_count：本日入住間數
      - nationality_counts：各國籍入住間數
      - source_counts：各來源入住間數

    收款金額以「金額(M 欄)」為準：
      1) 優先使用 L 欄為「本日總額」那一列的金額
      2) 若該列沒有數字，改用明細列 M 欄加總（有房號 & 非待收款）
    """
    header_idx = 1  # 第 2 列是欄位名稱
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None)
    header_row = df.iloc[header_idx]

    # === 欄位位置 ===
    room_col_idx = header_row[header_row == "房號"].index[0]      # B 欄
    nation_col_idx = header_row[header_row == "國籍"].index[0]    # D 欄
    source_col_idx = header_row[header_row == "來源"].index[0]    # F 欄
    amount_col_idx = header_row[header_row == "金額"].index[0]    # M 欄
    payinfo_col_idx = 11  # L 欄：付款方式 / 單號，裡面會出現「待收款」「本日總額」

    # 實際資料從第 4 列開始（index = 3）
    data = df.iloc[header_idx + 2 :].copy()

    # 有房號就算一間房
    room_mask = data[room_col_idx].notna()

    # 合併儲存格：國籍、來源往下補
    data[nation_col_idx] = data[nation_col_idx].ffill()
    data[source_col_idx] = data[source_col_idx].ffill()

    # 付款資訊（L 欄）
    payinfo = data[payinfo_col_idx].astype(str)

    # 待收款列：今天還沒收到錢，不算本日收款
    daishou_mask = payinfo.str.contains("待收款", na=False)

    # 本日總額小計列：L 欄包含「本日總額」
    daily_total_mask = payinfo.str.contains("本日總額", na=False)

    # 金額（M 欄），非數字通通變 0
    amounts_m = pd.to_numeric(data[amount_col_idx], errors="coerce").fillna(0)

    if DEBUG:
        print("\n[DEBUG] 本日總額列：")
        print(data.loc[daily_total_mask, [payinfo_col_idx, amount_col_idx]])
        print("[DEBUG] 本日總額列 M 欄原始值：", data.loc[daily_total_mask, amount_col_idx].tolist())
        print("[DEBUG] 本日總額列 M 欄轉數字後：", amounts_m[daily_total_mask].tolist())

    # 先算出「本日總額列」的金額（如果有）
    daily_total_value = int(amounts_m[daily_total_mask].sum())

    if daily_total_mask.any() and daily_total_value > 0:
        # ✅ 有找到「本日總額」而且金額 > 0，就用它
        total_amount = daily_total_value
    else:
        # ✅ 否則退回用明細加總（有房號 & 非待收款）
        revenue_mask = room_mask & (~daishou_mask)
        total_amount = int(amounts_m.where(revenue_mask).sum())

    # ✅ 入住間數：只要有房號就算一間（包含待收款房）
    room_count = int(room_mask.sum())

    # ✅ 國籍統計：看所有有房號的列
    nationality_series = (
        data.loc[room_mask, nation_col_idx]
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .dropna()
    )
    nationality_counts = nationality_series.value_counts()

    # ✅ 來源統計：看所有有房號的列，統一大小寫
    source_series = (
        data.loc[room_mask, source_col_idx]
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .str.upper()
    )
    source_counts = source_series.value_counts()

    return total_amount, room_count, nationality_counts, source_counts


def format_counts_full(counts: pd.Series, unit: str = "間") -> str:
    """把 value_counts 組成『標籤X間、標籤Y間』字串。"""
    if counts is None or counts.empty:
        return "無"

    parts = []
    for label, cnt in counts.items():
        parts.append(f"{label}{int(cnt)}{unit}")
    return "、".join(parts)


def format_hotel_message(
    report_date: str,
    total_amount: int,
    room_count: int,
    nationality_counts: pd.Series,
    source_counts: pd.Series,
) -> str:
    """組出給老闆看的每日營收摘要文字。"""
    if room_count == 0:
        return f"{report_date} {HOTEL_NAME}｜今日尚無入住紀錄。"

    nat_text = format_counts_full(nationality_counts, unit="間")
    src_text = format_counts_full(source_counts, unit="間")

    return (
        f"{report_date} {HOTEL_NAME}｜"
        f"入住 {room_count} 間｜"
        f"本日實際收款 {total_amount:,} 元｜"
        f"國籍：{nat_text}｜"
        f"來源：{src_text}"
    )


def main() -> None:
    raw = input("請輸入要查看的日期（1-31，直接按 Enter 預設 1）：").strip()
    if raw == "":
        target_day = 1
    else:
        target_day = int(raw)

    report_date = date(YEAR, MONTH, target_day).isoformat()

    total_amount, room_count, nat_counts, src_counts = read_hotel_daily_stats(
        XLSX_PATH, str(target_day)
    )
    message = format_hotel_message(report_date, total_amount, room_count, nat_counts, src_counts)

    print("=== 旅館 Demo 測試輸出 ===")
    print(message)


if __name__ == "__main__":
    main()
