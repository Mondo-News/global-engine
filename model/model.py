"""
The model is where all data operations take place. The news article data is retrieved from the NewsAPI,
transformed into a pandas dataframe, translated into English and stored to the SQL database.
Additionally, the keyword search and the filtering based on news categories is implemented here.

"""


import deepl
from newsapi import NewsApiClient
import pandas as pd
from utils import utils, SQL_connector


class Model:
    """
    The Model consists of pure application logic, which interacts with the database.
    It includes all the information to represent data to the end user and directly manages the data,
    logic and rules of the application.
    """

    def __init__(self):
        # We use the NewsAPI to retrieve the news articles. The API always offers the most important headlines from over
        # 80.000 sources worldwide and always ranks them by newest headline first.
        # We have four NewsAPI api keys. Each one uses a NewsAPI Developer account, which is limited to 100 requests
        # per day. In case we need to perform more requests than that, we can switch to a different API key.
        api_key_1 = '07288a2d35394938b113ad3cf504d9cd'
        api_key_2 = '79e2b6cce45448e7bbe899ce7e8ece2f'
        api_key_3 = '8211359a9d754b858ded09f1db22c86d'
        api_key_4 = 'ad9f4f1f95f241469d57d1605bb47725'

        # For translating the articles to English we use the Deepl Translator. Deepl is offering an API which has a
        # free Pro version, allowing to translate up to 500.000 characters per month. In case we need reach the limit
        # we may have to switch to a paid version. For now we use two accounts, each with their own API key, so we can
        # switch as soon as we reach the limit on one.
        api_key_deepl_1 = 'cb0199b6-1ddb-f742-5005-64c9e170b5cb:fx'
        api_key_deepl_2 = '888f984b-dd99-fb06-b220-7af59a2f4b84:fx'

        # First we initialise the NewsAPI. In case we need to switch API key, we can to that here.
        self.newsAPI = NewsApiClient(api_key=api_key_4)

        # These are the countries that are currently supported by Mondo News. All of them are part of the G20 Group of
        # Countries. Mondo News only supports these 14 yet, as the NewsAPI only offers news from these countries.
        # We use the two-letter codes to refer to these countries and store them in the country_codes list.
        self.country_codes = ['ar', 'au', 'br', 'de', 'fr', 'in', 'it', 'ca', 'mx', 'ru', 'za', 'gb', 'us', 'cn']

        # The article data of MondoNews is stored in a SQL database.
        # Here, they are retrieved from that database and stored in df_articles.
        self.df_articles = SQL_connector.readDataFromSQL()

        # The Deepl Translation API is initialised. In case we need to switch API key, we can to that here.
        self.translator = deepl.Translator(api_key_deepl_2)

    def scrape_newsAPI(self, category):
        """
        This functions scrapes data from the NewsAPI and stores it into the top_headlines dictionary.
        The function uses a for-loop to go through the list of all countries and then retrieves the data for the
        category passed on as parameter of the function based on the language of the country that the news
        is retrieved for.

        :param category: The category of which to scrape the news.
        :return: Dictionary with raw API response from NewsAPI for all countries and the category specified
        in the parameter
        """

        top_headlines = {} # Initialize an empty dictionary first

        # Go through all countries specified above and save the raw API response from the NewsAPI in the top_headlines
        # dictionary.
        for country_code in self.country_codes:
            print("Country for next NewsAPI request: " + country_code)
            if country_code in ['au', 'gb', 'us', 'za', 'in', 'ca']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category=category,
                                                                             country=country_code, language='en')
            elif country_code in ['br']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category=category,
                                                                             country=country_code, language='pt')
            elif country_code in ['mx', 'ar']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category=category,
                                                                             country=country_code, language='es')
            elif country_code in ['sa']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category=category,
                                                                             country=country_code, language='ar')
            elif country_code in ['cn']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category=category,
                                                                             country=country_code, language='zh')
            else:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category=category,
                                                                             country=country_code,
                                                                             language=country_code)

        return top_headlines

    def transform_article_data(self, raw_api_response_dict, category):
       """
       This function transforms the response dictionary from scrape_newsAPI() into a pandas dataframe
       by mapping the relevant data to predefined columns.

       :param raw_api_response_dict: The dictionary containing the raw NewsAPI response object for a category
       :param category: The news category for which the raw_api_response_dict contains news data
       :return: Transformed article data pandas dataframe
       """

        # Delete old data and overwrite it with an empty data frame
        df = pd.DataFrame(
            columns=['country', 'category', 'source', 'title', 'author', 'description', 'content', 'url', 'urlToImage',
                     'publishedAt'])

        # Goes through all countries for which data is available in the raw NewsAPI response dictionary
        # and for each country, save all available information in corresponding columns of a pandas dataframe
        for country in raw_api_response_dict:
            country_dict = {'country': [], 'category': [], 'source': [], 'title': [], 'author': [], 'description': [],
                            'content': [],
                            'url': [], 'urlToImage': [], 'publishedAt': []}

            # Now all articles in the raw NewsAPI response dictionary are taken one by one for each country and
            # the information is put in the corresponding column in the new dataframe.
            # Note that here we change the two letter country codes to three letter country codes, because the JSON
            # files used for creating the map use three letter country codes.
            for article in raw_api_response_dict[country]['articles']:
                country_dict['country'].append(utils.convertIsoCodes_2_to_3(country))
                country_dict['category'].append(category)
                country_dict['source'].append(article['source']['name'])
                country_dict['title'].append(article['title'])
                country_dict['author'].append(article['author'])
                country_dict['description'].append(article['description'])
                country_dict['content'].append(article['content'])
                country_dict['url'].append(article['url'])
                country_dict['urlToImage'].append(article['urlToImage'])
                country_dict['publishedAt'].append(article['publishedAt'])

            # Now the dictionary is converted to a pandas dataframe
            df_country_dict = pd.DataFrame.from_dict(country_dict)
            # As this is done for every country individually, the dataframes for all individual countries are now
            # aggregated together in a dataframe containing all articles for all countries and the desired category.
            df = df.append(df_country_dict, ignore_index=True)

        return df

    def storeArticleData(self, transformed_article_data):
        """
        This function overwrites the df_article class variable with the transformed data frame given as parameter.
        The function then also pushes the transformed article data given as parameter to the SQL database where it
        is being stored.

        :param transformed_article_data: Pandas data frame with transformed article data.
        :return: None
        """

        self.df_articles = transformed_article_data
        print("New Article Data is being stored: ")
        print(self.getFullArticleData()[['url', 'category']].head())

        SQL_connector.writeDataToSQL(transformed_article_data)

    def refreshDataFromSQL(self):
        """
        This function saves the latest full article data as pandas dataframe from the SQL database in the df_article
        class variable.
        :return: None
        """
        self.df_articles = SQL_connector.readDataFromSQL()

    def getFullArticleData(self):
        """
        Returns latest full article data as pandas dataframe.
        :return: Latest article data as pandas dataframe
        """
        return self.df_articles

    def getArticlesByKeywordSearch(self, query_string, category_filtered_df):
        """
        Performs the keyword search on the headlines in the data frame passed in category_filtered_df.
        The user can input any search string on Mondo News as well as select one or more categories in which to search
        for articles. This function returns the dataframe that contains only articles of the desired category where
        the query appears in the headline.
        This function is robust to upper- or lowercase strings, as all queries as well as headlines are converted to
        lowercase before the search is performed.

        :param query_string: The search string entered by the user on Mondo News.
        :param category_filtered_df: The dataframe containing all article data of the selected categories.
        :return: A dataframe containing the articles where the query_string appears in the headline and the article is
        of the selected category
        """

        # Convert query to lowercase and remove leading and trailing whitespaces
        query_string = query_string.lower().strip()

        # Convert title column to list for faster search
        listed = category_filtered_df['title'].tolist()
        # Convert all titles to lowercase to match query string
        listed = [title.lower() for title in listed]

        # Perform search with list to have better performance
        filtered_df = category_filtered_df[[query_string in title for title in listed]]

        return filtered_df

    def getArticlesByCategories(self, filter_categories):
        """
        Filters full article data by selected categories from the buttons in the UI. When the user clicks on one or
        multiple categories on Mondo News, this function filters the article data based on these selected categories and
        returns a dataframe containing all article data of the corresponding categories.


        :param filter_categories: List of categories selected
        :return: Filtered pandas dataframe
        """
        # Categories supported by NewsAPI
        newsAPI_categories = ['general', 'technology', 'business', 'science', 'sports', 'health']

        # We have to assert that the parameter filter_categories is actually a list of one or multiple articles.
        # We also have to assert that the categories given are in the supported categories.
        assert type(filter_categories) is list
        assert [cat in newsAPI_categories for cat in filter_categories] or not filter_categories

        # Get full article data from class
        df = self.getFullArticleData()

        # Filter full article data for selected categories.
        # The data is given as a boolean series and then transformed to a pandas dataframe.
        boolean_series = df['category'].isin(filter_categories)
        filtered_articles = df[boolean_series]

        # Sort articles by publishing date with newest first.
        filtered_articles = filtered_articles.sort_values(by=['publishedAt'], ascending=False)

        return filtered_articles

    def getThreeLetterIsoCodes(self):
        """
        Get Available three letter Iso country codes for the countries for which there is News data available.

        :return: List with three letter Iso codes of the countries which have news data available.
        """
        # We first initialise a new empty list that we will then return.
        output_list = []

        # Now loop through all the countries that are supported by Mondo News. Their two letter country codes are
        # saved in the class variable country_codes.
        # For each of them, the three letter Iso code is added to the list to be returned.
        for iso_code in self.country_codes:
            output_list.append(utils.convertIsoCodes_2_to_3(iso_code))
        return output_list

    def getTwoLetterIsoCodes(self):
        """
        This function returns the two letter country codes of all countries supported by Mondo News as a list.

        :return: List of two letter country codes of countries supported by Mondo News.
        """
        return self.country_codes

    def translateArticleData(self, news_df):
        """
        Gets scraped and transformed dataframe with information on all news articles and translates relevant information
        using the Deepl translator API. The API recognizes the original language and translates to British English.
        It translates only the title as only the title is used on Mondo News and returns a pandas dataframe which
        contains the translated headlines for every article instead of the original one. All other columns of the
        dataframe except the headline remain unchanged.

        :param news_df: Data frame containing data on all news articles.
        :return: Article data pandas dataframe with headline (title column) translated into English.
        """

        # In the rare event of an empty value in the title column, a Value Error arises. In order to not let the
        # execution stop in such a case, we use try.
        # The function replaces the old headline with the translated headline.
        try:

            news_df['title'] = news_df['title'].apply(lambda title:
                                                      self.translator.translate_text(title, target_lang='EN-GB'))

        except ValueError as e:
            print("Error occurred: " + str(e))
            print("A empty text cannot be translated. Skipping this one.")
            pass

        return news_df


# Instantiate a View() object
modelObject = Model()

# OLD CODE: Code for storing pandas df as csv in current directory
# modelObject.df_articles.to_csv("df_country_articles.csv", index=False, encoding="utf-8-sig") TODO: Delete
# df_newArticleData = pd.read_csv(utils.path_csv_database, encoding='utf-8-sig')  # TODO: Delete
