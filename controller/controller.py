from model.newsAPI_scraper import modelObject


class Controller:
    """
    The Controller class forms the layer between View and Model to guarantee interchangeability and a common
    interface between the two. It also helps in collaborative development, since frontend and backend can be implemented
    autonomously.
    The Controller provides methods that View and Model can use to communicate with each other and get e.g. Data.
    """

    def __init__(self):
        #self.updateArticleData() # TODO: Comment for testing
        pass

    def getTopArticles(self):
        return modelObject.getTopArticles()

    def getFullArticleData(self):
        return modelObject.getFullArticleData()

    def updateArticleData(self):
        """
        Triggers scraper and updates database.
        :return:
        """
        # Categories supported by NewsAPI
        # categories = ['general', 'technology', 'business', 'science', 'sports', 'health'] # TODO: Commented for testing
        categories = ['general', 'technology'] # TODO: Delete

        # Drops all data in Article Data and assigns it to new object
        df_newArticleData = modelObject.getFullArticleData()[0:0]

        for category in categories:
            print("Next category to be parsed: " + category)
            raw_api_response_dict = modelObject.scrape_newsAPI(category)
            transformed_data = modelObject.transform_article_data(raw_api_response_dict, category)
            translated_data = modelObject.translateArticleData(transformed_data)
            df_newArticleData = df_newArticleData.append(translated_data, ignore_index=True)

        print("New Article Data is being stored: ")
        print(df_newArticleData.head())
        modelObject.storeArticleData(df_newArticleData)


    def searchArticleData(self, keyword):
        """
        Searches the full df_article data frame of the model and filters for the given keyword from the search.
        :return: Filtered pandas data frame
        """
        pass

    def getAvailableIsoCodes(self, iso_type):
        """
        Requests Iso codes from model for which there is news data available
        :type iso_type: ISO type of return object: Either two or three
        :return: List of Iso codes
        """
        assert iso_type == 2 or iso_type == 3

        if iso_type == 2:
            return modelObject.getTwoLetterIsoCodes()
        else:
            return modelObject.getThreeLetterIsoCodes()


controllerObject = Controller()
