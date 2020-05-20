from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd

#get the chrome extension
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

#test function
def scrapMarsTitleData():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    #url to visit
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #get the html from the website
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())

    #get the new titles and get the latest aka the top one
    testTitle = soup.find_all('div', class_= "content_title")
    articleExcerpt = soup.find_all('div', class_="article_teaser_body")

    #store the artcile excerpts
    articles = [];
    #pull the exerpt for each article into a list for future use in case to expand scope
    for artcile in articleExcerpt:
        articles.append(artcile.text)

    # get titles
    titles = []
    #put each title into a list for future use in case to expand scope
    for title in testTitle:
        titles.append(title.text)

    #store to be used later
    latestTitle = titles[1]
    excerpt = articles[0]
    return latestTitle, excerpt

def scrapeMarsImage():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    #get the mars image using splinter
    marsURL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(marsURL)

    #create a browser object to get the image
    marsHTML = browser.html
    marsSoup = BeautifulSoup(marsHTML, 'html.parser')
    #go to find the html object
    imageURL = marsSoup.find("div", class_ = "carousel_items")
    #reach into style since that is where the url for the image is
    imageString = imageURL.article["style"]
    #if it does have URL in it, get the image
    if "url" in  imageString:
        #get the position with just the URL for the image and not the extra text
        imageStrPosition = imageString.index("url")+5
        rawString = imageString[imageStrPosition:-3]
        #add the url for the image with the url for the website in order to draw it out
        finalURL = "https://www.jpl.nasa.gov" + rawString
        #later need to add for a else statement
    return finalURL


def scrapeTweet():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    #use splinter to get tweet
    twitterURL = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitterURL)


    #create browser object to get the latest tweet from twitter
    twitterHTML = browser.html
    twitterSoup = BeautifulSoup(twitterHTML, 'html.parser')
    try:
        #find all the tweets
        tweet = twitterSoup.find_all("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
        #get latetst tweet by looking at the most recent
        latestTweet = tweet[0].text
        return latestTweet
    except:
        return "no tweet found"
    


def getMarsTable():
    #using pandas to get facts
    factsURL = "https://space-facts.com/mars/"

    #read the html with pandas
    test = pd.read_html(factsURL)
    #get the correct mars table
    marsFactTable = test[0]
    #rename column
    marsFactTable.columns = ["Mars","Facts"]
    #change to html
    marsTableHTML = marsFactTable.to_html()
    return marsTableHTML


def hemiPictures():
    #get pictures of the mars hemisphere
    marsHemisphere = [
        {"Title": "Cerberus" , "img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
        {"Title":"Schiaparelli","img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
        {"Title":"Syrtis Major","img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
        {"Title":"Valles marineris","img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"}
    ]


#call all helper functions
def scrapeAll():
    newsTitle, newsParagraph = scrapMarsTitleData()
    data = {
        "Title Data": newsTitle,
        "Title Paragraph": newsParagraph,
        "Mars Image": scrapeMarsImage(),
        "Mars Tweet": scrapeTweet(),
        "Mars Facts Table": getMarsTable(),
        "Mars Hemisphere Pictures": hemiPictures()
    }

    return data

