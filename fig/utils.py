import pandas as pd

def merge_csv(file_paths):
    """
    指定されたCSVファイルをマージし、simulation_idごとに統合されたDataFrameを返す。

    - 数値カラムは平均を計算
    - 非数値カラムは最初の値を適用

    Args:
        file_paths (list of str): マージするCSVファイルのパスのリスト

    Returns:
        pd.DataFrame: マージ後のDataFrame
    """
    # CSVファイルをデータフレームとして読み込む
    dfs = [pd.read_csv(file) for file in file_paths]

    # `simulation_id` が存在しない場合のチェック
    for df in dfs:
        if "simulation_id" not in df.columns:
            raise ValueError("CSVファイルに 'simulation_id' カラムが存在しません")

    # すべてのデータを結合
    df_combined = pd.concat(dfs)

    # 数値カラムを特定（`simulation_id` は除外）
    numeric_columns = df_combined.select_dtypes(include=["number"]).columns

    # `simulation_id` ごとに平均を計算（数値カラムのみ）
    df_merged = df_combined.groupby("simulation_id", as_index=False).agg({col: "mean" for col in numeric_columns})

    # 数値でないカラムは最初の値を取得
    non_numeric_columns = [col for col in df_combined.columns if col not in numeric_columns and col != "simulation_id"]
    df_non_numeric = df_combined.groupby("simulation_id", as_index=False)[non_numeric_columns].first()

    # 数値と非数値のデータを統合
    df_final = pd.merge(df_merged, df_non_numeric, on="simulation_id", how="left")

    return df_final

# # 関数を適用してDataFrameを取得
# file_paths = [
#     "data/cloth_output_change_pmt_amt_seed1.csv",
#     "data/cloth_output_change_pmt_amt_seed2.csv",
#     "data/cloth_output_change_pmt_amt_seed3.csv",
#     "data/cloth_output_change_pmt_amt_seed4.csv",
#     "data/cloth_output_change_pmt_amt_seed5.csv",
# ]
# df_result = merge_csv(file_paths)
# df_result.to_csv("~/Desktop/out.csv")
