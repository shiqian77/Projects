import pandas as pd

# Data Preprocessing
df = pd.read_csv('speeddating.csv')
from sklearn.preprocessing import OrdinalEncoder

for col in df.columns:
    if df[col].dtype == "object" :
        oe = OrdinalEncoder()
        oe.fit(df[[col]])
        df[col] = oe.fit_transform(df[[col]])


df.drop('has_null', axis = 1, inplace = True)

df.dropna(inplace = True)
df['samerace'] = df['samerace'].astype('int')
# Create age difference column
df['age_diff'] = df['age'] - df['age_o']

# Drop other age colum
df.drop(['age','age_o', 'd_age', 'd_d_age'], axis = 1, inplace = True)

to_drop = [column_name for column_name in df.columns if column_name.startswith('d_')]
df.drop(to_drop, axis = 1, inplace = True)

# we would like to use gender same_race wave field like met decision age_diff sincere ambitious and funny
columns_to_select = ['gender', 'samerace', 'wave', 'field', 'like', 'met',  'age_diff', 'sinsere_o', 'ambitous_o', 'funny_o', 'match']

selected_columns_df = df[columns_to_select]
selected_columns_df.to_csv('selected_columns.csv', index=False)