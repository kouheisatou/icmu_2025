import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from utils import merge_csv


# CSVデータを読み込み
df_capestimationattack = pd.read_csv("data/result_capacity_estimation_attack_simulation.csv")
df_groupsize = merge_csv([
    "data/cloth_output_change_group_params_seed1.csv",
    "data/cloth_output_change_group_params_seed2.csv",
    "data/cloth_output_change_group_params_seed3.csv",
    "data/cloth_output_change_group_params_seed4.csv",
    "data/cloth_output_change_group_params_seed5.csv",
])

# "average_payment_amount"が10000 かつ "group_limit_rate"が0.1 のデータのみ抽出
df_filtered = df_groupsize[
    (df_groupsize['average_payment_amount'] == 10000) &
    (df_groupsize['group_limit_rate'] == 0.1)
    ][['group_size', 'time/average']].dropna()
df_filtered = df_filtered.sort_values(by='group_size')

# "group_size(k)" を "group_size" に統一
df_capestimation_filtered = df_capestimationattack[['group_size(k)', 'success_rate']].dropna()
df_capestimation_filtered.rename(columns={'group_size(k)': 'group_size'}, inplace=True)

plt.rcParams["font.family"] = "Andale Mono"
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Andale Mono'
plt.rcParams['mathtext.it'] = 'Andale Mono'
plt.rcParams['mathtext.bf'] = 'Andale Mono'
plt.rcParams["font.size"] = 16
plt.figure()

# プロットの作成
fig, ax1 = plt.subplots(figsize=(10, 6))
# 二つ目の軸（右軸, Attack Success Rate）
ax1.set_ylabel('Attack Success Rate')
ax1.plot(df_capestimation_filtered['group_size'], df_capestimation_filtered['success_rate'], marker='s', markersize=4, linestyle='-', color="black", label='Attack Success Rate')
ax1.set_xlabel('group_size')
ax1.set_xticks(np.arange(df_capestimation_filtered['group_size'].min(), df_capestimation_filtered['group_size'].max() + 1, 1))


# グリッドの追加
ax1.grid(True, linestyle='--', alpha=0.6, axis="y")

plt.savefig("group_size_vs_attack_resistance.pdf", bbox_inches="tight", transparent=True)
