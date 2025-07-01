import matplotlib.pyplot as plt
import seaborn as sns
from utils import merge_csv
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.widgets import Slider

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
    ["group_size", "group_limit_rate", "success_rate", "fail_no_path_rate", "fail_no_alternative_path_rate", "cul/average"]]
filtered_df = filtered_df[(filtered_df["group_limit_rate"] != 1.0) & (filtered_df["group_limit_rate"] != 0.0)]

# ピボットテーブルの作成
success_rate_pivot = filtered_df.pivot(index="group_limit_rate", columns="group_size", values="success_rate")
time_success_average_pivot = filtered_df.pivot(index="group_limit_rate", columns="group_size", values="fail_no_path_rate")
time_fail_average_pivot = filtered_df.pivot(index="group_limit_rate", columns="group_size", values="fail_no_alternative_path_rate")

# 初期値
success_rate_min_limit = 0.729
fail_before_send_min_limit = 0.0
fail_after_send_max_limit = 0.005

# フィルタリング用関数
def update_plots(val):
    success_limit = success_slider.val
    fail_before_send_rate_min = fail_before_send_slider.val
    fail_after_send_rate_max = fail_after_send_slider.val

    highlight_mask1 = (success_rate_pivot > success_limit) & (time_fail_average_pivot < fail_after_send_rate_max) & (time_success_average_pivot > fail_before_send_rate_min)
    highlight_mask2 = (success_rate_pivot > success_limit) & (time_success_average_pivot > fail_before_send_rate_min)
    highlight_mask3 = (success_rate_pivot > success_limit) & (time_fail_average_pivot < fail_after_send_rate_max)

    for ax, pivot, mask, cmap, label in zip(
            [ax1, ax2, ax3],
            [success_rate_pivot, time_success_average_pivot, time_fail_average_pivot],
            [highlight_mask1, highlight_mask2, highlight_mask3],
            ["Greens", "coolwarm", "coolwarm"],
            ["Success Rate", "Fail Before Send Rate", "Fail After Send Rate"]):

        ax.clear()
        sns.heatmap(pivot, cmap=cmap, annot=False, fmt=".2f", ax=ax, cbar=False)
        ax.invert_yaxis()

        for i in range(mask.shape[0]):
            for j in range(mask.shape[1]):
                if mask.iloc[i, j]:
                    ax.add_patch(mpatches.Rectangle((j, i), 1, 1, fill=False, edgecolor="white", lw=2))

        ax.set_title(label)

    fig.canvas.draw_idle()

# プロット領域の作成
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
plt.subplots_adjust(bottom=0.25)

# スライダーの作成
ax_slider1 = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_slider2 = plt.axes([0.2, 0.07, 0.65, 0.03])
ax_slider3 = plt.axes([0.2, 0.04, 0.65, 0.03])

success_slider = Slider(ax_slider1, 'Success Rate Min', 0.7, 0.8, valinit=success_rate_min_limit)
fail_before_send_slider = Slider(ax_slider2, 'Fail Before Send Min', 0, 0.4, valinit=fail_before_send_min_limit)
fail_after_send_slider = Slider(ax_slider3, 'Fail After Send Max', 0, 0.5, valinit=fail_after_send_max_limit)

success_slider.on_changed(update_plots)
fail_before_send_slider.on_changed(update_plots)
fail_after_send_slider.on_changed(update_plots)

# 初回プロット更新
update_plots(None)

plt.show()