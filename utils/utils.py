import pycountry
import os

# PATHS

# Absolute paths to map.html file
dirname = os.path.dirname(__file__)
path_map_html_file = os.path.join(dirname, '../view/map.html')
path_csv_database = os.path.join(dirname, '../data/df_article_data.csv')


def convertIsoCodes_2_to_3(two_letter_iso):
    """
    Converts 2-Letter ISO codes to 3-Letter ISO codes.
    :param two_letter_iso: 2-Letter ISO code
    :return: 3-Letter ISO Code
    """
    countries = {}
    for country in pycountry.countries:
        countries[country.alpha_2.lower()] = country.alpha_3.lower()

    three_letter_iso = countries.get(two_letter_iso.lower(), 'Unknown code')

    return three_letter_iso


def convertIsoCodes_3_to_2(three_letter_iso):
    """
    Converts 3-Letter ISO codes to 2-Letter ISO codes.
    :param three_letter_iso: 3-Letter ISO code
    :return: 2-Letter ISO Code
    """
    countries = {}
    for country in pycountry.countries:
        countries[country.alpha_3.lower()] = country.alpha_2.lower()

    two_letter_iso = countries.get(three_letter_iso.lower(), 'Unknown code')

    return two_letter_iso
