from newsapi import NewsApiClient
import pandas as pd
import controller

class Model:

    def __init__(self):
        # We have two api keys for testing
        api_key_1 = '07288a2d35394938b113ad3cf504d9cd'
        api_key_2 = '79e2b6cce45448e7bbe899ce7e8ece2f'

        self.newsAPI = NewsApiClient(api_key=api_key_2)
        self.country_codes_top15 = ['ar', 'au', 'br', 'de', 'fr', 'in', 'it', 'ca', 'mx', 'ru', 'sa', 'za', 'gb', 'us',
                                    'cn']
        self.df_articles = pd.DataFrame(
            columns=['country', 'source', 'title', 'author', 'description', 'content', 'url', 'urlToImage',
                     'publishedAt'])

        # self.country_codes = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de',
        # 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my',
        # 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw',
        # 'ua', 'us', 've', 'za'] self.country_codes_g20 = ['ar','au','br','de','fr','in','id','it','jp','ca','mx',
        # 'ru','sa','za', 'kr','tr','gb','us','cn']

    def scrape_data(self):
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

    def transform_data(self, raw_headlines_dict):
        """
        Transforms the response dictionary from scrape_data() into a pandas dataframe by mapping the relevant
        data to predefined columns.
        :return: Transformed article data pandas df
        """

        for country in raw_headlines_dict:
            print(country)
            country_dict = {'country': [], 'source': [], 'title': [], 'author': [], 'description': [], 'content': [],
                            'url': [], 'urlToImage': [], 'publishedAt': []}

            for article in raw_headlines_dict[country]['articles']:
                country_dict['country'].append(country)
                country_dict['source'].append(article['source']['name'])
                country_dict['title'].append(article['title'])
                country_dict['author'].append(article['author'])
                country_dict['description'].append(article['description'])
                country_dict['content'].append(article['content'])
                country_dict['url'].append(article['url'])
                country_dict['urlToImage'].append(article['urlToImage'])
                country_dict['publishedAt'].append(article['publishedAt'])

            df_country_dict = pd.DataFrame.from_dict(country_dict)
            self.df_articles = self.df_articles.append(df_country_dict, ignore_index=True)

        return self.df_articles

    def updateData(self):
        """
        Triggers scraper and updates database.
        :return: None
        """
        raw_headlines_dict = self.scrape_data()
        transformed_output = self.transform_data(raw_headlines_dict)

    def getArticleData(self):
        """
        Returns latest article data as pandas dataframe.
        :return: Latest article data as pandas dataframe
        """
        return self.df_articles


# Instantiate a View() object
modelObject = Model()

# OLD CODE: Code for storing pandas df as csv in current directory
# modelObject.df_articles.to_csv("df_country_articles.csv", index=False, encoding="utf-8-sig")
