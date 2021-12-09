import os

import sqlalchemy
import pandas as pd


engine = sqlalchemy.create_engine(
    "postgresql://iadujedbpfsesq:c238ad3f75b43b9fd81c2f56160f1164557561e84c4e75ad778a6b3cbcd39e8b@ec2-54-76-249-45.eu"
    "-west-1.compute.amazonaws.com:5432/d6pgndjpkhrscm")
dirname = os.path.dirname(__file__)

def readDataFromSQL():
    df_article_data = pd.read_sql_query('select * from public.articles', con=engine)
    return df_article_data


def writeDataToSQL(pd_dataframe):
    print("Data successfully written to SQL DB!")
    pd_dataframe.to_sql("articles", engine, if_exists='replace', method="multi", index=False, schema="public")


#df_newArticleData = pd.read_csv(os.path.join(dirname, '../data/df_article_data.csv'),
#                                  encoding='utf-8-sig')  # TODO: Delete. Only for testing without API usage
#writeDataToSQL(df_newArticleData)