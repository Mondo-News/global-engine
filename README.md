<H1 align="center">
    <img href="https://mondo-news.herokuapp.com/" src="https://github.com/Mondo-News/global-engine/blob/065deb89e18a021c6d171173a10e643657f7c806/assets/mondo-news_header.PNG?raw=true" width="400px">
</H1>
    
Our product delivers an interactive world map where users can **visualize the top headlines per country**, within fourteen countries from the Group of Twenty (G20) intergovernmental forum. The target user is someone interested in knowing what is going on from **multicultural worldview**, with it being specially useful for scholars in the fields of public policy and international affairs.

Take a look at Mondo News <a href="https://mondo-news.herokuapp.com/">**here!**</a>

See <a href="https://mondo-news.readthedocs.io/en/latest/">**documentation!**</a>

## Features

Our product is a website with an **interactive globe** that allows the user to zoom in on trending news from specific countries. 
We focus on countries that are in the G20 and parse news articles in **nine different languages and translate them to English**.
Per country and category, five news articles are shown, including a thumbnail picture, the headline, and a link to the article page.
The articles are automatically categorized into the following categories:

| Symbol    | Category | 
| :-------- | :------- |
| <img src="https://github.com/Mondo-News/global-engine/blob/main/data/pictures/general.png?raw=true" width="30px"> | `General` |
| <img src="https://github.com/Mondo-News/global-engine/blob/main/data/pictures/technology.png?raw=true" width="30px"> | `Technology` |
| <img src="https://github.com/Mondo-News/global-engine/blob/main/data/pictures/health.png?raw=true" width="30px"> | `Health` |
| <img src="https://github.com/Mondo-News/global-engine/blob/main/data/pictures/science.png?raw=true" width="30px"> | `Science` |
| <img src="https://github.com/Mondo-News/global-engine/blob/main/data/pictures/business.png?raw=true" width="30px"> | `Business` |
| <img src="https://github.com/Mondo-News/global-engine/blob/main/data/pictures/sports.png?raw=true" width="30px"> | `Sports` |

By default, the articles shown are the most **popular articles in that country from the last 24 hours**.
A filter on the world map level allows to change the categories to be displayed.
In addition, a search bar on the world map level allows the user to search for specific keywords from within the headlines.

## Try it yourself!
In order to install and run Mondo News on your own maschine, just download the repo and follow the instructions:
1. Download the repo as .zip
2. Navigate inside the global-engine directory and open a terminal/command prompt
3. Install all dependencies from the requirements.txt file with:
    `$ pip install -r requirements.txt`

4. Run `dash_app.py`
5. Open the localhost URL printed out in the console after a little while

**Note:** Alternatively, we recommend to **take a look at our live demo** <a href="https://mondo-news.herokuapp.com/">**here!**</a>


  
## API Reference

The data for Mondo News is mainly acquired and transformed by utilizing the following APIs.

| Name     | Description                |
| :------- | :------------------------- |
| <a href="https://newsapi.org/">NewsAPI.org</a> | News API is a simple HTTP REST API for searching and retrieving live articles from all over the web. |
| <a href="https://deep-translator.readthedocs.io/en/latest/#">deep_translator</a> | A flexible FREE and UNLIMITED tool to translate between different languages in a simple way using multiple translators. |
| <a href="https://pypi.org/project/pycountry/">pycountry</a> | pycountry provides the ISO databases. |

  
## Authors

- [@GamesluxX](https://www.github.com/@GamesluxX)
- [@sailandcode](https://www.github.com/sailandcode)
- [@skier921](https://www.github.com/skier921)
- [@annaccd](https://www.github.com/@annaccd)

  
