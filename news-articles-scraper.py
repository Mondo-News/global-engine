from newsapi import NewsApiClient
import pandas as pd

# Init
benedikt_key = '07288a2d35394938b113ad3cf504d9cd'
victor_key = '79e2b6cce45448e7bbe899ce7e8ece2f'
newsapi = NewsApiClient(api_key=victor_key)

# country codes
country_codes = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb',
                 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl',
                 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua',
                 'us', 've', 'za']
country_codes_g20 = ['ar', 'au', 'br', 'de', 'fr', 'in', 'id', 'it', 'jp', 'ca', 'mx', 'ru', 'sa', 'za', 'kr', 'tr',
                     'gb', 'us', 'cn']
country_codes_top15 = ['ar', 'au', 'br', 'de', 'fr', 'in', 'it', 'ca', 'mx', 'ru', 'sa', 'za', 'gb', 'us', 'cn']

# init dict for raw parsing results
top_headlines = {}

for country_code in country_codes_top15:
    print("country for next request: " + country_code)
    if country_code in ['au', 'gb', 'us', 'za', 'in', 'ca']:
        top_headlines[country_code] = newsapi.get_top_headlines(category='general',
                                                                country=country_code, language='en')
    elif country_code in ['br']:
        top_headlines[country_code] = newsapi.get_top_headlines(category='general',
                                                                country=country_code, language='pt')
    elif country_code in ['mx', 'ar']:
        top_headlines[country_code] = newsapi.get_top_headlines(category='general',
                                                                country=country_code, language='es')
    elif country_code in ['sa']:
        top_headlines[country_code] = newsapi.get_top_headlines(category='general',
                                                                country=country_code, language='ar')
    elif country_code in ['cn']:
        top_headlines[country_code] = newsapi.get_top_headlines(category='general',
                                                                country=country_code, language='zh')
    else:
        top_headlines[country_code] = newsapi.get_top_headlines(category='general',
                                                                country=country_code, language=country_code)

# create empty dataframe for filling unprocessed parsing data in
df_country_articles = pd.DataFrame(
    columns=['country', 'source', 'title', 'author', 'description', 'content', 'url', 'urlToImage', 'publishedAt'])

# for every country in dict, go through every article and store attributes in individual lists in a dict; then fill
# in df and append this dataframe to the empty one created above
for country in top_headlines:
    print(country)
    country_dict = {}
    country_dict['country'] = []
    country_dict['source'] = []
    country_dict['title'] = []
    country_dict['author'] = []
    country_dict['description'] = []
    country_dict['content'] = []
    country_dict['url'] = []
    country_dict['urlToImage'] = []
    country_dict['publishedAt'] = []

    for article in top_headlines[country]['articles']:
        country_dict['country'].append(country)
        country_dict['source'].append(article['source']['name'])
        country_dict['title'].append(article['title'])
        country_dict['author'].append(article['author'])
        country_dict['description'].append(article['description'])
        country_dict['content'].append(article['content'])
        country_dict['url'].append(article['url'])
        country_dict['urlToImage'].append(article['urlToImage'])
        country_dict['publishedAt'].append(article['publishedAt'])

    # create df with the articles from this country
    df_country_dict = pd.DataFrame.from_dict(country_dict)
    # print(df_country_dict.head(3))

    # append it to the general output df
    df_country_articles = df_country_articles.append(df_country_dict, ignore_index=True)

print("Number of parsed articles: " + str(len(df_country_articles)))
print(df_country_articles.head(5))
