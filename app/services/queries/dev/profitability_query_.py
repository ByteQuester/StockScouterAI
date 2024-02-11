import numpy as np
import pandas as pd


def profitability_query(df):
    # Pivot the DataFrame so that each metric becomes a column
    pivot_df = df.pivot_table(
        index=['EntityName', 'CIK', 'end', 'year', 'quarter', 'start'],
        columns='Metric',
        values='val')
    pivot_df.reset_index(inplace=True)
    pivot_df.columns.name = None
    df_final = pivot_df.copy()

    # 1. Convert 'end' column to datetime and financial values from cents to millions
    df_final['end'] = pd.to_datetime(df_final['end'], format='%Y-%m-%d')
    for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
        df_final[col] /= 1000000

    # 2. Calculate Profit Margin
    df_final['ProfitMarginPercent'] = df_final.apply(
        lambda row: round((row['NetIncomeLoss'] / row['Revenues']) * 100, 2)
        if pd.notna(row['NetIncomeLoss']) and pd.notna(row[
            'Revenues']) and row['Revenues'] != 0 else None,
        axis=1)

    # 3. Calculate Rolling Averages
    window_size = 4
    for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
        df_final[f'{col}_RollingAvg'] = df_final.groupby(
            ['EntityName', 'CIK'])[col].transform(
                lambda x: x.rolling(window=window_size, min_periods=1).mean())

    # 4. Calculate QoQ Growth Rates based on Rolling Averages
    for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
        df_final[f'{col}_QoQ'] = df_final.groupby(
            ['EntityName', 'CIK'])[f'{col}_RollingAvg'].pct_change() * 100

    # 5. Categorize and quantify QoQ Growth Rates
    def categorize_growth(growth):
        if growth > 10:
            return 'Increase', growth
        elif growth < -10:
            return 'Decrease', growth
        else:
            return 'Stable', growth

    for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
        df_final[[
            f'{col}_QoQ_Category', f'{col}_QoQ_Growth'
        ]] = df_final[f'{col}_QoQ'].apply(categorize_growth).apply(pd.Series)

    # 6. Categorize growth into custom categories and normalize values
    def categorize_custom(growth):
        if growth >= 100:
            return 'gained > 100$'
        elif growth > 0:
            return 'gained <= 100$'
        elif growth > -100:
            return 'lost <= 100$'
        else:
            return 'lost > 100$'

    for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
        df_final[f'{col}_Custom_Category'] = df_final[
            f'{col}_QoQ_Growth'].apply(categorize_custom)

    # 7. Normalize the data and apply the sign of the original QoQ growth value
    for quarter in df_final['quarter'].unique():
        quarter_data = df_final[df_final['quarter'] == quarter]
        total = quarter_data[[
            'NetIncomeLoss_QoQ_Growth', 'Revenues_QoQ_Growth',
            'OperatingIncomeLoss_QoQ_Growth'
        ]].abs().sum(axis=1)
        for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']:
            df_final.loc[df_final['quarter'] == quarter,
                         f'{col}_Normalized'] = (
                             df_final[f'{col}_QoQ_Growth'].abs() / total *
                             100) * np.sign(df_final[f'{col}_QoQ_Growth'])

    # 8. Select and rename columns
    columns_to_select = ['EntityName', 'CIK', 'end', 'NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss',
                         'ProfitMarginPercent', 'year', 'quarter'] + \
                        [f'{col}_RollingAvg' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] + \
                        [f'{col}_QoQ' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] + \
                        [f'{col}_QoQ_Category' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] + \
                        [f'{col}_QoQ_Growth' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] + \
                        [f'{col}_Normalized' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']] + \
                        [f'{col}_Custom_Category' for col in ['NetIncomeLoss', 'Revenues', 'OperatingIncomeLoss']]

    df_final = df_final[columns_to_select]
    df_final.rename(columns={
        'EntityName': 'ENTITY',
        'end': 'DATE',
        'year': 'Year',
        'quarter': 'Quarter'
    },
                    inplace=True)

    return df_final
