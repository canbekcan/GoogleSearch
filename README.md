# **Social Media Data Mining** ⛏️ 📊  for New Media and Communication 🧑‍💻 🌐

This repository contains Python code for a Google scraper created as a practice exercise for students in the Social Media Data Mining course offered by the New Media and Communication department. 

## Getting Started 🚀

To use this code, you'll need to have Python installed on your machine. You can download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).

You may need to download [Visual Studio Code](https://code.visualstudio.com) for coding. It is free.

Once you have Python installed, you can clone this repository using the following command (if you setup git package):
```bash
git clone https://github.com/canbekcan/GoogleSearch.git
```

GoogleSearchResults-API code allows to record Google search with API and save results to CSV file.


## Packages
```bash
pip install httpx parsel time csv google-api-python-client python-dotenv
```
## Environment
```bash
python -m venv myevn
```

## Google Custom Search API Setup  🔧
To use the Google Custom Search API, you'll need to set up a project in the Google Cloud Console and enable the Custom Search API. Follow these steps:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Navigate to the "APIs & Services" dashboard and click on "Enable APIs and Services."
4. Search for "Custom Search API" and enable it for your project.
5. Go to the "Credentials" tab and create an API key. This key will be used to authenticate your requests to the API.
6. Set up a Custom Search Engine (CSE) by going to the [Custom Search Engine](https://cse.google.com/cse/) page.
7. Create a new search engine and configure it to search the entire web or specific sites.
8. Note down the Search Engine ID (CX) from the CSE control panel.

## Data Analysis 📈

Once you have scraped the data, you can use Python libraries like Pandas and Matplotlib to analyze the data. These libraries provide tools for data manipulation, cleaning, and visualization.

## Further Exploration 🧭

This scraper is a basic example to get you started with web scraping in Python. There are many ways to extend this code to scrape data from more complex websites. You can also explore other Python libraries for data analysis, such as Seaborn and Scikit-learn.

## Additional Notes 📝

This code is for educational purposes only.
Be sure to check the terms of service of any website before scraping data from it.
Respect robots.txt files.


## Contributors of this repo
<a href="https://github.com/BanaBirSebepVer/GoogleSearch/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=BanaBirSebepVer/GoogleSearch" />
</a>
