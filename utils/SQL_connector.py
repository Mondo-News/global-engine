"""
This module builds the connection to the PostgreSQL database hosted remotely by Heroku.
It provides methods to write and read data to and from the database respectively.
"""
import os
import sqlalchemy
import pandas as pd

# Connect to db with login credentials
engine = sqlalchemy.create_engine(
    "postgresql://zwnwqsriotrmek:0904993ac6fd3d85cdb9f290a4f4e70ea532b05bd9cfd5bd14dce8bfeef6d777@ec2-54-217-232-239.eu-west-1.compute.amazonaws.com:5432/dd9gqijjjuook7")
dirname = os.path.dirname(__file__)


def readDataFromSQL():
    """
    Read data from database and store it into a Pandas data frame.
    :return: Pandas data frame with data currently stored in SQL database.
    """
    print("SQL is read into data frame")
    df_article_data = pd.read_sql_query('select * from public.articles', con=engine)
    return df_article_data


def writeDataToSQL(pd_dataframe):
    """
    Write data from data frame to the remote SQL database.
    :param pd_dataframe: Pandas data frame with new data to write to SQL database.
    :return: None
    """
    print("Data successfully written to SQL DB!")
    pd_dataframe.to_sql("articles", engine, if_exists='replace', method="multi", index=False, schema="public")
