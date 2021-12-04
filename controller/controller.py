from model.model import modelObject
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
        # Make initial API request
        # self.updateArticleData()
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

    def getArticlesByCategories(self, categories):
        category_filtered_df = modelObject.getArticlesByCategories(categories)

        # Select top five articles per country per category
        top5_filtered_df = category_filtered_df.groupby(['country', 'category']).head(5)
        return top5_filtered_df

    def getArticlesByKeywordSearch(self, categories, query_string):

        category_filtered_df = modelObject.getArticlesByCategories(categories)

        keyword_filtered_df = modelObject.getArticlesByKeywordSearch(query_string, category_filtered_df)

        # Select top five articles per country per category
        top5_filtered_df = keyword_filtered_df.groupby(['country', 'category']).head(5)
        return top5_filtered_df

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

        df_newArticleData = pd.read_csv("../data/df_articles_testing.csv",
                                        encoding='utf-8-sig')  # TODO: Delete. Only for testing without API usage
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
