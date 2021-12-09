import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine(
    "postgresql://iadujedbpfsesq:c238ad3f75b43b9fd81c2f56160f1164557561e84c4e75ad778a6b3cbcd39e8b@ec2-54-76-249-45.eu"
    "-west-1.compute.amazonaws.com:5432/d6pgndjpkhrscm")


def readDataFromSQL():
    df_article_data = pd.read_sql_query('select * from public.articles', con=engine)
    return df_article_data


def writeDataToSQL(pd_dataframe):
    pd_dataframe.to_sql("articles", engine, if_exists='replace', method="multi", index=False, schema="public")
