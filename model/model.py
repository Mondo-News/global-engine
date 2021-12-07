import deepl
from newsapi import NewsApiClient
import pandas as pd
from utils import utils


class Model:

    def __init__(self):
        # We have two NewsAPI api keys for testing
        api_key_2 = '07288a2d35394938b113ad3cf504d9cd'
        api_key_1 = '79e2b6cce45448e7bbe899ce7e8ece2f'

        # The deepl Translator API Key
        api_key_deepl_1 = 'cb0199b6-1ddb-f742-5005-64c9e170b5cb:fx'

        self.newsAPI = NewsApiClient(api_key=api_key_2)
        self.country_codes_top15 = ['de', 'fr']  # For testing TODO: Delete
        #self.country_codes_top15 = ['ar', 'au', 'br', 'de', 'fr', 'in', 'it', 'ca', 'mx', 'ru', 'sa', 'za', 'gb', 'us',
        #                            'cn']
        self.df_articles = pd.DataFrame(
            columns=['country', 'category', 'source', 'title', 'author', 'description', 'content', 'url', 'urlToImage',
                     'publishedAt'])

        self.translator = deepl.Translator(api_key_deepl_1)

        # self.country_codes = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
        # 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my',
        # 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw',
        # 'ua', 'us', 've', 'za'] self.country_codes_g20 = ['ar','au','br','de','fr','in','id','it','jp','ca','mx',
        # 'ru','sa','za', 'kr','tr','gb','us','cn']

    def scrape_newsAPI(self, category):
        """
        This functions scrapes data from the NewsAPI and stores it into the top_headlines dictionary
        :return: Dict with raw API response from NewsAPI
        """

        top_headlines = {}

        for country_code in self.country_codes_top15:
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
        Transforms the response dictionary from scrape_data() into a pandas dataframe by mapping the relevant
        data to predefined columns.
        :return: Transformed article data pandas df
        """

        # Delete old data and override it with an empty data frame
        df = pd.DataFrame(
            columns=['country', 'category', 'source', 'title', 'author', 'description', 'content', 'url', 'urlToImage',
                     'publishedAt'])

        for country in raw_api_response_dict:
            country_dict = {'country': [], 'category': [], 'source': [], 'title': [], 'author': [], 'description': [],
                            'content': [],
                            'url': [], 'urlToImage': [], 'publishedAt': []}

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

            df_country_dict = pd.DataFrame.from_dict(country_dict)
            df = df.append(df_country_dict, ignore_index=True)

        return df

    def storeArticleData(self, transformed_article_data):
        """
        Overwrties df_article with given transformed data frame
        :param transformed_article_data: Pandas data frame with transformed article data
        :return: None
        """
        self.df_articles = transformed_article_data
        print("New Article Data is being stored: ")
        print(self.getFullArticleData()[['url', 'category']].head())
        # self.df_articles.to_csv("df_articles.csv", index=False, encoding="utf-8-sig") # TODO: Delete

    def getFullArticleData(self):
        """
        Returns latest full article data as pandas dataframe.
        :return: Latest article data as pandas dataframe
        """
        return self.df_articles

    def getArticlesByKeywordSearch(self, query_string, category_filtered_df):

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
        Filters full article data by selected categories from the buttons in the UI.
        :param keyword_search_df: Filtered data frame from keyword search that shall be filtered for categories
        :param filter_categories: List of categories to be filtered for
        :return: Filtered pandas dataframe
        """
        # Categories supported by NewsAPI
        newsAPI_categories = ['general', 'technology', 'business', 'science', 'sports', 'health']

        assert type(filter_categories) is list
        assert [cat in newsAPI_categories for cat in filter_categories] or not filter_categories

        # Get full article data from class
        df = self.getFullArticleData()

        # Filter full article data for input categories
        boolean_series = df['category'].isin(filter_categories)
        filtered_articles = df[boolean_series]

        # Sort articles by publishing date
        filtered_articles = filtered_articles.sort_values(by=['publishedAt'], ascending=False)

        return filtered_articles

    def getThreeLetterIsoCodes(self):
        """
        Get Available Iso codes for which there is News data available
        :return: List with 3-Letter Iso codes
        """
        output_list = []
        for iso_code in self.country_codes_top15:
            output_list.append(utils.convertIsoCodes_2_to_3(iso_code))
        return output_list

    def getTwoLetterIsoCodes(self):
        return self.country_codes_top15

    def translateArticleData(self, news_df):
        """
        Gets scraped and transformed dataframe with information on all news articles and translates relevant information.
        That is, it translates only the title, description and content.
        It returns again a pandas dataframe.

        :param news_df:
        :return: Translated article data pandas dataframe
        """
        try:

            news_df['title'] = news_df['title'].apply(lambda title:
                                                      self.translator.translate_text(title, target_lang='EN-GB'))

            # TODO: If translation of description and content is needed, decomment part below
            # news_df['description'] = news_df['description'].apply(lambda description:
            #                                                       self.translator.translate_text(description,
            #                                                                                      target_lang='EN-GB'))
            #
            # news_df['content'] = news_df['content'].apply(lambda content:
            #                                               self.translator.translate_text(content,
            #                                               target_lang='EN-GB'))
        except ValueError as e:
            print("Error occurred: " + str(e))
            print("A empty text cannot be translated. Skipping this one.")
            pass

        return news_df


# Instantiate a View() object
modelObject = Model()

# OLD CODE: Code for storing pandas df as csv in current directory
# modelObject.df_articles.to_csv("df_country_articles.csv", index=False, encoding="utf-8-sig") TODO: Delete
