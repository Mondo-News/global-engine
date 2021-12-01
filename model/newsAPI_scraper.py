import deepl
from newsapi import NewsApiClient
import pandas as pd
from utils import utils


class Model:

    def __init__(self):
        # We have two NewsAPI api keys for testing
        api_key_1 = '07288a2d35394938b113ad3cf504d9cd'
        api_key_2 = '79e2b6cce45448e7bbe899ce7e8ece2f'

        # API Key for deepl
        api_key_deepl_1 = 'cb0199b6-1ddb-f742-5005-64c9e170b5cb:fx'

        self.newsAPI = NewsApiClient(api_key=api_key_2)
        self.country_codes_top15 = ['de', 'us'] # For testing
        #self.country_codes_top15 = ['ar', 'au', 'br', 'de', 'fr', 'in', 'it', 'ca', 'mx', 'ru', 'sa', 'za', 'gb', 'us',
        #                            'cn'] # TODO: Replace test variable with commented real list
        self.df_articles = pd.DataFrame()

        self.translator = deepl.Translator(api_key_deepl_1)

        # self.country_codes = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
        # 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my',
        # 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw',
        # 'ua', 'us', 've', 'za'] self.country_codes_g20 = ['ar','au','br','de','fr','in','id','it','jp','ca','mx',
        # 'ru','sa','za', 'kr','tr','gb','us','cn']

    def scrape_newsAPI(self):
        """
        This functions scrapes data from the NewsAPI and stores it into the top_headlines dictionary
        :return: Dict with raw API response from NewsAPI
        """
        top_headlines = {}

        for country_code in self.country_codes_top15:
            print("country for next request: " + country_code)
            if country_code in ['au', 'gb', 'us', 'za', 'in', 'ca']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category='general',
                                                                             country=country_code, language='en')
            elif country_code in ['br']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category='general',
                                                                             country=country_code, language='pt')
            elif country_code in ['mx', 'ar']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category='general',
                                                                             country=country_code, language='es')
            elif country_code in ['sa']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category='general',
                                                                             country=country_code, language='ar')
            elif country_code in ['cn']:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category='general',
                                                                             country=country_code, language='zh')
            else:
                top_headlines[country_code] = self.newsAPI.get_top_headlines(category='general',
                                                                             country=country_code,
                                                                             language=country_code)

        return top_headlines

    def transform_article_data(self, raw_api_response_dict):
        """
        Transforms the response dictionary from scrape_data() into a pandas dataframe by mapping the relevant
        data to predefined columns.
        :return: Transformed article data pandas df
        """

        # Delete old data and override it with an empty data frame
        df = pd.DataFrame(
            columns=['country', 'source', 'title', 'author', 'description', 'content', 'url', 'urlToImage',
                     'publishedAt'])

        for country in raw_api_response_dict:
            print(country)
            country_dict = {'country': [], 'source': [], 'title': [], 'author': [], 'description': [], 'content': [],
                            'url': [], 'urlToImage': [], 'publishedAt': []}

            for article in raw_api_response_dict[country]['articles']:
                country_dict['country'].append(utils.convertIsoCodes_2_to_3(country))
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

    def storeArticleData(self,  transformed_article_data):
        """
        Overwrties df_article with given transformed data frame
        :param transformed_article_data: Pandas data frame with transformed article data
        :return: None
        """
        self.df_articles = transformed_article_data
        print("New Article Data: ") # TODO: Delete
        print(self.df_articles.head()) # TODO: Delete

    def getFullArticleData(self):
        """
        Returns latest full article data as pandas dataframe.
        :return: Latest article data as pandas dataframe
        """
        return self.df_articles

    def getTopArticles(self):
        """
        Filters for topmost five articles per country of the full df_article data frame
        :return: Filtered pandas data frame
        """
        topArticles = self.df_articles.groupby('country').head(5)
        return topArticles

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
                                                            self.translator.translate_text(title, target_lang="EN-GB"))

            # TODO: If translation of description and content is needed, decomment part below
            # news_df['description'] = news_df['description'].apply(lambda description:
            #                                                             self.translator.translate_text(description,
            #                                                                                            target_lang="EN-GB"))
            #
            # news_df['content'] = news_df['content'].apply(lambda content:
            #                                                     self.translator.translate_text(content,
            #                                                                                    target_lang="EN-GB"))
        except ValueError as e:
            print("Error occurred: " + str(e))
            print("A empty text cannot be translated. Skipping this one.")
            pass

        return news_df


# Instantiate a View() object
modelObject = Model()



# OLD CODE: Code for storing pandas df as csv in current directory
# modelObject.df_articles.to_csv("df_country_articles.csv", index=False, encoding="utf-8-sig")
