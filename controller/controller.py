from model.newsAPI_scraper import modelObject
import pandas as pd  # TODO: Delete. Only needed for testing


class Controller:
    """
    The Controller class forms the layer between View and Model to guarantee interchangeability and a common
    interface between the two. It also helps in collaborative development, since frontend and backend can be implemented
    autonomously.
    The Controller provides methods that View and Model can use to communicate with each other and get e.g. Data.
    """

    def __init__(self):
        # Make 'general' the default selected category
        self.selected_categories = ['general']
        self.updateArticleData()  # TODO: Comment for testing
        pass

    def getSelectedCategories(self):
        return self.selected_categories

    def selectCategory(self, category):
        if category not in self.getSelectedCategories():
            self.selected_categories.append(category)
            print("New category selected: " + category)
            print(self.getSelectedCategories())

    def deselectCategory(self, category):
        if category in self.getSelectedCategories():
            self.selected_categories.remove(category)
            print("Category de-selected: " + category)
            print(self.getSelectedCategories())

    def getTopArticles(self):
        return modelObject.getTopArticles()

    def getArticlesByCategories(self, categories):
        return modelObject.getArticlesByCategories(categories)

    def getFullArticleData(self):
        return modelObject.getFullArticleData()

    def updateArticleData(self):
        """
        Triggers scraper and updates database.
        :return:
        """
        print('DATA UPDATE TRIGGERED')
        # Categories supported by NewsAPI
        # categories = ['general', 'technology', 'business', 'science', 'sports', 'health'] # TODO: Commented for testing
        categories = ['general', 'technology']  # TODO: Delete

        # Drops all data in Article Data and assigns it to new object
        df_newArticleData = self.getFullArticleData()[0:0]

        for category in categories:
            print("Next category to be parsed: " + category)
            # raw_api_response_dict = modelObject.scrape_newsAPI(category)
            # transformed_data = modelObject.transform_article_data(raw_api_response_dict, category)
            # translated_data = modelObject.translateArticleData(transformed_data)
            # df_newArticleData = df_newArticleData.append(translated_data, ignore_index=True)

        df_newArticleData = pd.read_csv("../data/df_articles_testing.csv", encoding='utf-8-sig')  # TODO: Delete. Only for testing without API usage
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
