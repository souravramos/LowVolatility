import os

def write_df_to_csv(df, output_path):
    output_dir = os.path.dirname(output_path)
    print(output_dir)
    print(df)
    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_path)