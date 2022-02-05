import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import RobustScaler
import sklearn.metrics
from catboost import CatBoostRegressor
from sklearn.preprocessing import OrdinalEncoder
from pandas_profiling import ProfileReport
import pickle
import psycopg2


host = 'arjuna.db.elephantsql.com'
user = 'qrnyldng'
password = 'TmCangCbHK1oWFRacELzYlFIDB3pWBYe'
database = 'qrnyldng'

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)


cur = connection.cursor()


cur.execute("""
            SELECT * FROM car;
            """)

result = cur.fetchall()

df = pd.DataFrame(result,columns=['Manufacturer', 'Model', 'Km', 'Fuel', 'Loc', 'Price', 'Old_year', 'Old_month'])


# --------Preprocessing--------
def correct_year(value):
  if (50 < value):
    value = value + 1900
    return value
  elif value < 50:
    value = value + 2000
    return value
  else:
    return value

df = df.loc[df['Price'] < 3000]
df['Old_year'] = df['Old_year'].apply(lambda x : correct_year(x))


cat_cols = df.columns[df.dtypes == object]
encoder = OrdinalEncoder()
df[cat_cols] = encoder.fit_transform(df[cat_cols])


df_x = df.drop('Price', axis = 1)
df_y = df['Price']


# --------Modeling--------
# pipe1 = make_pipeline(
#     RobustScaler(),
#     CatBoostRegressor(verbose = 100)
# )

model = CatBoostRegressor(verbose = 100)

model.fit(df_x, df_y)

with open('./model.p','wb') as file:
    pickle.dump(model,file)
    pickle.dump(encoder,file)