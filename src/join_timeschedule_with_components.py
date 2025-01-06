import pandas as pd
import os


os.chdir('C:/Users/marce/OneDrive/Desktop/UZH/Network Science/newRpeo/UZH_Network')

semesters = ['FS23', 'HS23', 'FS24', 'HS24']

for semester in semesters:

    csv1_path = f'data/csv/{semester}/VVZ_{semester}_time_schedule.csv'
    csv2_path = f'data/csv/{semester}/VVZ_{semester}_module_components.csv'  

    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path, encoding='utf-16')
    df2 = df2.drop_duplicates(subset=['Module'])


    print(df1.head())
    print(df2.head())

    merged_df = pd.merge(
        df1,
        df2[['Module', 'Components']],
        left_on='Component of Module',
        right_on='Module',
        how='inner'
    )

    merged_df = merged_df.drop(columns=['Module'])
    print(len(df1))
    print(len(df2))
    print(len(merged_df))

    output_path = f'data/csv/{semester}/VVZ_{semester}_joined_time_schedule.csv' 
    merged_df.to_csv(output_path, index=False)

    print(f"Merged CSV saved at: {output_path}")
