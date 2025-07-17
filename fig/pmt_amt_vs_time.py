import argparse
import pandas as pd
import matplotlib.pyplot as plt

from utils import merge_csv

# CSVファイルを読み込む
df = merge_csv([
    "data/cloth_output_change_pmt_amt_seed1.csv",
    "data/cloth_output_change_pmt_amt_seed2.csv",
    "data/cloth_output_change_pmt_amt_seed3.csv",
    "data/cloth_output_change_pmt_amt_seed4.csv",
    "data/cloth_output_change_pmt_amt_seed5.csv",
])

# 必要なカラムを選択
columns_needed = ["average_payment_amount", "time_success/average", "time_success/95-percentile", "routing_method"]
df_selected = df[columns_needed]

# "routing_method" が "group_routing" または "cloth_original" のデータを抽出
df_filtered = df_selected[df_selected["routing_method"].isin(["group_routing", "cloth_original"])]

# "group_routing" と "cloth_original" でデータを分けてソート
df_group_routing = df_filtered[df_filtered["routing_method"] == "group_routing"].sort_values(by="average_payment_amount")
df_cloth_original = df_filtered[df_filtered["routing_method"] == "cloth_original"].sort_values(by="average_payment_amount")

# 10^5 の average_payment_amount を除外
df_group_routing_filtered = df_group_routing[df_group_routing["average_payment_amount"] != 10**5]
df_cloth_original_filtered = df_cloth_original[df_cloth_original["average_payment_amount"] != 10**5]

plt.rcParams["font.family"] = "Andale Mono"
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Andale Mono'
plt.rcParams['mathtext.it'] = 'Andale Mono'
plt.rcParams['mathtext.bf'] = 'Andale Mono'
plt.rcParams["font.size"] = 16
plt.figure()

# グラフの描画
plt.figure(figsize=(10, 5))

# "cloth_original" のプロット（黒色）
plt.plot(df_cloth_original_filtered["average_payment_amount"], df_cloth_original_filtered["time_success/average"],
         label="LN (Average)", markersize=4, marker='s', color='gray', linestyle="-")
plt.plot(df_cloth_original_filtered["average_payment_amount"], df_cloth_original_filtered["time_success/95-percentile"],
         label="LN (95%ile)", markersize=4, marker='s', color='gray', linestyle="dashed")

# "group_routing" のプロット（グレー）
plt.plot(df_group_routing_filtered["average_payment_amount"], df_group_routing_filtered["time_success/average"],
         label="GCB (Average)", markersize=4, marker='o', color='black', linestyle="-")
plt.plot(df_group_routing_filtered["average_payment_amount"], df_group_routing_filtered["time_success/95-percentile"],
         label="GCB (95%ile)", markersize=4, marker='o', color='black', linestyle="dashed")

# 軸ラベルの設定
plt.xlabel("Average Payment Amount [satoshi]")
plt.ylabel("Latency (Success) [ms]")
plt.ylim([0,5500])

# 横軸を対数スケールに変更
plt.xscale("log")

# タイトルを削除（何も設定しない）
plt.title("")

# グリッドを追加（対数スケールでも見やすいように）
plt.grid(True, linestyle="--", alpha=0.5)

# 凡例を表示
plt.legend(framealpha=0)

# PDFとして保存（bbox_inches="tight" で余白を調整）
plt.savefig("pmt_amt_vs_time.pdf", format="pdf", bbox_inches="tight", transparent=True)