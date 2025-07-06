import matplotlib.pyplot as plt
import seaborn as sns
from utils import merge_csv
import numpy as np
import matplotlib.patches as mpatches

# ファイルを読み込む
df = merge_csv([
    "data/cloth_output_change_group_params_seed1.csv",
    "data/cloth_output_change_group_params_seed2.csv",
    "data/cloth_output_change_group_params_seed3.csv",
    "data/cloth_output_change_group_params_seed4.csv",
    "data/cloth_output_change_group_params_seed5.csv",
])

# 必要なカラムの抽出とフィルタリング
filtered_df = df[df["average_payment_amount"] == 10000][
    ["group_size", "group_limit_rate", "success_rate", "fail_no_path_rate", "fail_no_alternative_path_rate", "time_success/average", "time_fail/average"]]

# group_limit_rateが1.0と0.0を除外
filtered_df = filtered_df[(filtered_df["group_limit_rate"] != 1.0) & (filtered_df["group_limit_rate"] != 0.0)]

# ピボットテーブルの作成
success_rate_pivot = filtered_df.pivot(index="group_limit_rate", columns="group_size", values="success_rate")
fail_before_send_rate_pivot = filtered_df.pivot(index="group_limit_rate", columns="group_size", values="fail_no_path_rate")
fail_after_send_rate_pivot = filtered_df.pivot(index="group_limit_rate", columns="group_size", values="fail_no_alternative_path_rate")
time_success_average_pivot = filtered_df.pivot(index="group_limit_rate", columns="group_size", values="time_success/average")
time_fail_average_pivot = filtered_df.pivot(index="group_limit_rate", columns="group_size", values="time_fail/average")

# フォント設定
plt.rcParams["font.family"] = "Andale Mono"
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Andale Mono'
plt.rcParams['mathtext.it'] = 'Andale Mono'
plt.rcParams['mathtext.bf'] = 'Andale Mono'
plt.rcParams["font.size"] = 18

# 整数の目盛を作成
xtick_positions = np.arange(len(success_rate_pivot.columns.astype(int)))




# =========== success_rate ===========
success_rate_min_limit = 0.729
fail_after_send_max_limit = 0.005
highlight_mask = (success_rate_pivot > success_rate_min_limit) & (fail_after_send_rate_pivot < fail_after_send_max_limit)

plt.figure(figsize=(7, 6))
ax = plt.gca()
sns.heatmap(success_rate_pivot, cmap="Greens", annot=False, fmt=".2f", xticklabels=True)
plt.xlabel("group_size")
plt.ylabel("α")
plt.yticks(fontsize=18)
plt.gca().invert_yaxis()
plt.xticks([5-1.5, 10-1.5, 15-1.5, 20-1.5], ["5", "10", "15", "20"], fontsize=18)

# 強調セルのハッチング
if highlight_mask is not None:
    for i in range(highlight_mask.shape[0]):
        for j in range(highlight_mask.shape[1]):
            if highlight_mask.iloc[i, j]:
                ax.add_patch(mpatches.Rectangle((j, i), 1, 1, fill=False, edgecolor="white", lw=2))

ax.text(3, 5.8, f"Success Rate > {success_rate_min_limit}\nFASR < {fail_after_send_max_limit}",
        ha='left', va='bottom', fontsize=20, color="white")
ax.annotate("", xy=(1.5, 3.5), xytext=(3, 5.8), arrowprops=dict(arrowstyle="-", color="white", lw=1))

# カラーバーの横に矢印とテキストを追加
cbar = ax.collections[0].colorbar
cbar.set_label("Success Rate")
cbar.ax.tick_params(labelsize=18)
cbar_min, cbar_max = cbar.vmin, cbar.vmax
target_values = [("LN", 0.70808), ("RBB", 0.73388)]
for text, value in target_values:
    arrow_position = (value - cbar_min) / (cbar_max - cbar_min)
    cbar.ax.annotate(text, xy=(0, arrow_position), xytext=(-0.5, arrow_position),
                     xycoords="axes fraction", ha="right", va="center", fontsize=20,
                     color="black", arrowprops=dict(arrowstyle="->", color="black", lw=1, mutation_scale=8))

plt.savefig("group_limit_rate_and_group_size_heatmap_success_rate.pdf", format="pdf", bbox_inches="tight", transparent=True)
plt.close()





# =========== fail_after_send_rate ===========
highlight_mask = (success_rate_pivot > success_rate_min_limit) & (fail_after_send_rate_pivot < fail_after_send_max_limit)

plt.figure(figsize=(7, 6))
ax = plt.gca()
sns.heatmap(fail_after_send_rate_pivot, cmap="coolwarm", annot=False, fmt=".2f", xticklabels=True)
plt.xlabel("group_size")
plt.ylabel("α")
plt.yticks(fontsize=18)
plt.gca().invert_yaxis()
plt.xticks([5-1.5, 10-1.5, 15-1.5, 20-1.5], ["5", "10", "15", "20"], fontsize=18)

# 強調セルのハッチング
if highlight_mask is not None:
    for i in range(highlight_mask.shape[0]):
        for j in range(highlight_mask.shape[1]):
            if highlight_mask.iloc[i, j]:
                ax.add_patch(mpatches.Rectangle((j, i), 1, 1, fill=False, edgecolor="white", lw=2))

# 矢印とテキスト
ax.text(3, 5.8, f"Success Rate > {success_rate_min_limit}\nFASR < {fail_after_send_max_limit}", ha='left', va='bottom', fontsize=20, color="white")
ax.annotate("", xy=(1.5, 3.5), xytext=(3, 5.8), arrowprops=dict(arrowstyle="-", color="white", lw=1))

# カラーバーのラベル
cbar = ax.collections[0].colorbar
cbar.set_label("FASR")
cbar.ax.tick_params(labelsize=18)
cbar_min, cbar_max = cbar.vmin, cbar.vmax
target_values = [("RBB", 0)]
for text, value in target_values:
    arrow_position = (value - cbar_min) / (cbar_max - cbar_min)
    cbar.ax.annotate(text, xy=(0, arrow_position), xytext=(-0.5, arrow_position),
                     xycoords="axes fraction", ha="right", va="center", fontsize=20,
                     color="black", arrowprops=dict(arrowstyle="->", color="black", lw=1, mutation_scale=8))

plt.savefig("group_limit_rate_and_group_size_heatmap_fail_after_send_rate.pdf", format="pdf", bbox_inches="tight", transparent=True)
plt.close()






# =========== time_success ===========
plt.figure(figsize=(7, 6))
ax = plt.gca()
sns.heatmap(time_success_average_pivot, cmap="coolwarm", annot=False, fmt=".2f", xticklabels=True)
plt.xlabel("group_size")
plt.ylabel("α")
plt.yticks(fontsize=18)
plt.gca().invert_yaxis()
plt.xticks([5-1.5, 10-1.5, 15-1.5, 20-1.5], ["5", "10", "15", "20"], fontsize=18)

# 強調セルのハッチング
print("time_success highlighted cells")
if highlight_mask is not None:
    for i in range(highlight_mask.shape[0]):
        for j in range(highlight_mask.shape[1]):
            if highlight_mask.iloc[i, j]:
                ax.add_patch(mpatches.Rectangle((j, i), 1, 1, fill=False, edgecolor="white", lw=2))
                group_size = j+2
                alpha = round(i/20+0.05, 2)
                print(f"{group_size}\t{alpha}\t{time_success_average_pivot[group_size][alpha]}")

# 矢印とテキスト
ax.text(3, 5.8, f"Success Rate > {success_rate_min_limit}\nFASR < {fail_after_send_max_limit}", ha='left', va='bottom', fontsize=20, color="white")
ax.annotate("", xy=(1.5, 3.5), xytext=(3, 5.8), arrowprops=dict(arrowstyle="-", color="white", lw=1))

# カラーバーのラベル
cbar = ax.collections[0].colorbar
cbar.set_label("Latency (Success) [ms]")
cbar.ax.tick_params(labelsize=18)
cbar_min, cbar_max = cbar.vmin, cbar.vmax
target_values = [("RBB", 643.467332)]
for text, value in target_values:
    arrow_position = (value - cbar_min) / (cbar_max - cbar_min)
    cbar.ax.annotate(text, xy=(0, arrow_position), xytext=(-0.5, arrow_position),
                     xycoords="axes fraction", ha="right", va="center", fontsize=20,
                     color="black", arrowprops=dict(arrowstyle="->", color="black", lw=1, mutation_scale=8))

plt.savefig("group_limit_rate_and_group_size_heatmap_latency_success.pdf", format="pdf", bbox_inches="tight", transparent=True)
plt.close()






# =========== time_fail ===========
plt.figure(figsize=(7, 6))
ax = plt.gca()
sns.heatmap(time_fail_average_pivot, cmap="coolwarm", annot=False, fmt=".2f", xticklabels=True)
plt.xlabel("group_size")
plt.ylabel("α")
plt.yticks(fontsize=18)
plt.gca().invert_yaxis()
plt.xticks([5-1.5, 10-1.5, 15-1.5, 20-1.5], ["5", "10", "15", "20"], fontsize=18)

# 強調セルのハッチング
print("time_fail highlighted cells")
if highlight_mask is not None:
    for i in range(highlight_mask.shape[0]):
        for j in range(highlight_mask.shape[1]):
            if highlight_mask.iloc[i, j]:
                ax.add_patch(mpatches.Rectangle((j, i), 1, 1, fill=False, edgecolor="white", lw=2))
                group_size = j+2
                alpha = round(i/20+0.05, 2)
                print(f"{group_size}\t{alpha}\t{time_fail_average_pivot[group_size][alpha]}")

# 矢印とテキスト
ax.text(3, 5.8, f"Success Rate > {success_rate_min_limit}\nFASR < {fail_after_send_max_limit}", ha='left', va='bottom', fontsize=20, color="white")
ax.annotate("", xy=(1.5, 3.5), xytext=(3, 5.8), arrowprops=dict(arrowstyle="-", color="white", lw=1))

# カラーバーのラベル
cbar = ax.collections[0].colorbar
cbar.set_label("Latency (Fail) [ms]")
cbar.ax.tick_params(labelsize=18)
cbar.ax.annotate("RCB", xy=(0, 0), xytext=(-0.5, 0), xycoords="axes fraction", ha="right", va="center", fontsize=20, color="black", arrowprops=dict(arrowstyle="->", color="black", lw=1, mutation_scale=8))

plt.savefig("group_limit_rate_and_group_size_heatmap_latency_fail.pdf", format="pdf", bbox_inches="tight", transparent=True)
plt.close()
