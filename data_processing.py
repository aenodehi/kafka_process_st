import pandas as pd

def calculate_means(df, window_size=5):
    """
    Calculate the mean of the last five rows for each 'box_id'.
    """
    if df['accel'].apply(lambda x: isinstance(x, str)).any():
        df['accel'] = df['accel'].apply(lambda x: list(map(float, x.split('|'))) if isinstance(x, str) else x)
    df[['x', 'y', 'z']] = pd.DataFrame(df['accel'].tolist(), index=df.index)
    
    # Ensure no missing values in the columns used for calculations
    df = df.dropna(subset=['x', 'y', 'z'])
    
    df['x_m'] = df.groupby('box_id')['x'].rolling(window=window_size, min_periods=1).mean().reset_index(0, drop=True)
    df['y_m'] = df.groupby('box_id')['y'].rolling(window=window_size, min_periods=1).mean().reset_index(0, drop=True)
    df['z_m'] = df.groupby('box_id')['z'].rolling(window=window_size, min_periods=1).mean().reset_index(0, drop=True)
    return df

def calculate_differences(df):
    """
    Calculate the difference between the last window and the previous window.
    """
    df['x_m_diff'] = df.groupby('box_id')['x_m'].diff().fillna(0)
    df['y_m_diff'] = df.groupby('box_id')['y_m'].diff().fillna(0)
    df['z_m_diff'] = df.groupby('box_id')['z_m'].diff().fillna(0)
    return df

def apply_threshold(df, threshold=0.04):
    """
    Determine if the differences are below the threshold.
    """
    df['x_thr'] = df['x_m_diff'].abs() < threshold
    df['y_thr'] = df['y_m_diff'].abs() < threshold
    df['z_thr'] = df['z_m_diff'].abs() < threshold
    return df

def check_sequence(df, window_size=12):
    df['any_thr'] = df[['x_thr', 'y_thr', 'z_thr']].any(axis=1)

    def determine_result(group):
        any_thr_series = group['any_thr']
        results = [0] * len(group)
        for i in range(window_size, len(group)):
            last_12 = any_thr_series.iloc[i-window_size:i]
            last_value = any_thr_series.iloc[i-1]
            
            if all(last_12):
                results[i] = -2
            elif not any(last_12):
                results[i] = 2
            elif last_value and len(last_12) < window_size:
                results[i] = -1
            elif not last_value and len(last_12) < window_size:
                results[i] = 1
            else:
                results[i] = 0

        print(f"Results: {results}")
        return pd.Series(results, index=group.index)
    df['result'] = df.groupby('box_id', group_keys=False).apply(determine_result)
    
    # print("Result Column:")
    # print(df[['any_thr', 'result']])

    return df

def process_data(df):
    """
    Process the data by applying all the steps sequentially.
    """
    df = calculate_means(df)
    df = calculate_differences(df)
    df = apply_threshold(df)
    df = check_sequence(df)
    # print("Sequence checked.")

    return df