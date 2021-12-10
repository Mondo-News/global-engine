"""
The controller module is the layer between all view and model modules and build the layer between the two.
In the module we call methods from both model and view and transmit data between them.
"""
from model.model import modelObject


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

    def refreshDataFromSQL(self):
        """
        Triggers data from the SQL connector module to request data in remote PostgreSQL database
        :return: None
        """
        modelObject.refreshDataFromSQL()

    def getSelectedCategories(self):
        """
        Return list of currently selected categories
        :return: List of selected categories (Strings)
        """
        return self.selected_categories

    def selectCategory(self, category):
        """
        Add new category to the list of currently selected categories
        :param category: Category to select
        :return: None
        """
        # Check if category is already selected
        if category not in self.getSelectedCategories():
            # Append newly selected category
            self.selected_categories.append(category)
            print("New category selected: " + category)
            print(self.getSelectedCategories())

    def deselectCategory(self, category):
        """
        Remove category from the list of currently selected categories
        :param category: Category to de-select
        :return: None
        """
        # Check if category is selected
        if category in self.getSelectedCategories():
            # If category is selected, then remove it from the list
            self.selected_categories.remove(category)
            print("Category de-selected: " + category)
            print(self.getSelectedCategories())

    def getArticlesByCategories(self, categories):
        """
        Trigger method in model to return filtered dataframe containing only articles in the categories passed to the method.
        Additionally this methods filters for the top-5 articles per category and country.
        :param categories: Categories to filter for.
        :return: Dataframe with top-5 articles per country and category for the categories passed.
        """
        category_filtered_df = modelObject.getArticlesByCategories(categories)

        # Select top five articles per country and category
        top5_filtered_df = category_filtered_df.groupby(['country', 'category']).head(5)
        return top5_filtered_df

    def getArticlesByKeywordSearch(self, categories, query_string):
        """
        Same as getArticlesByCategories, but additionally trigger method in model to filter for query searched for by the user.
        :param categories: Categories to filter for.
        :param query_string: Query inserted by the user.
        :return: Dataframe with top-5 articles per country and category for the categories passed and the query searched for.
        """
        category_filtered_df = modelObject.getArticlesByCategories(categories)

        keyword_filtered_df = modelObject.getArticlesByKeywordSearch(query_string, category_filtered_df)

        # Select top five articles per country per category
        top5_filtered_df = keyword_filtered_df.groupby(['country', 'category']).head(5)
        return top5_filtered_df

    def getFullArticleData(self):
        """
        Trigger method in model to return current full dataframe from the SQL db
        :return: Dataframe with latest data in the remote PostgreSQL database
        """
        return modelObject.getFullArticleData()

    def updateArticleData(self):
        """
        Updates all data pipelines by consecutively triggering methods for scraping NewsAPI, transforming API response
        into dataframe, calling deepL API for translating article titles, and writing the resulting new dataframe into the
        PostgreSQL database remotely.
        :return: None
        """
        print('DATA UPDATE TRIGGERED')

        # Get list of supported categories from the model
        categories = modelObject.getSupportedCategories()

        # Drops all data in Article Data and assigns it to new object
        df_newArticleData = self.getFullArticleData()[0:0]

        # Loop through all categories and trigger required data sourcing & transforming methods required to bring data in the right format.
        for category in categories:
            print("Next category to be parsed: " + category)
            raw_api_response_dict = modelObject.scrape_newsAPI(category)
            print("Data transformation started for category: " + category)
            transformed_data = modelObject.transform_article_data(raw_api_response_dict, category)
            print("Translation started for category: " + category)
            translated_data = modelObject.translateArticleData(transformed_data)
            df_newArticleData = df_newArticleData.append(translated_data, ignore_index=True)

        # Finally, trigger method to store new data in the SQL db remotely
        modelObject.storeArticleData(df_newArticleData)

    def getAvailableIsoCodes(self, iso_type):
        """
        Requests Iso codes from model for which there is news data available and returns them in the desired format that
        is defined by the input parameter iso_type
        :type iso_type: ISO type of return object: Either two or three
        :return: List of Iso codes
        """
        # Check whether input parameter is either 2 or 3 and can be served
        assert iso_type == 2 or iso_type == 3

        if iso_type == 2:
            return modelObject.getTwoLetterIsoCodes()
        else:
            return modelObject.getThreeLetterIsoCodes()


# Create Controller
controllerObject = Controller()
