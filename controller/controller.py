from model.newsAPI_scraper import modelObject


class Controller:
    """
    The Controller class forms the layer between View and Model to guarantee interchangeability and a common
    interface between the two. It also helps in collaborative development, since frontend and backend can be implemented
    autonomously.
    The Controller provides methods that View and Model can use to communicate with each other and get e.g. Data.
    """

    def __init__(self):
        #self.updateArticleData() # TODO:decomment
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
        raw_api_response_dict = modelObject.scrape_newsAPI()
        transformed_data = modelObject.transform_article_data(raw_api_response_dict)
        modelObject.storeArticleData(transformed_data)


    def searchArticleData(self, keyword):
        """
        Searches the full df_article data frame of the model and filters for the given keyword from the search.
        :return: Filtered pandas data frame
        """
        pass

    def getAvailableIsoCodes(self):
        """
        Requests Iso codes from model for which there is news data available
        :return: List of Iso codes
        """
        return modelObject.getThreeLetterIsoCodes()


controllerObject = Controller()
