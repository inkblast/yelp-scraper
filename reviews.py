
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import manage_database
from dateutil.parser import parse
import re

'''
parser = argparse.ArgumentParser()
parser.add_argument("-link")
args = parser.parse_args()
'''
options = webdriver.ChromeOptions()
#options.add_argument("user-data-dir=C:\\Users\\acer\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data")
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
driver = webdriver.Chrome(chrome_options=options)
resturentList = []

class ReviewInfo:
    def __init__(self, comment,rating, ratingDate, profileName,profileLocation, profileLink):
        self.comment = comment
        self.rating = rating
        self.ratingDate = ratingDate
        self.profileName = profileName
        self.profileLocation = profileLocation
        self.profileLink = profileLink

    def to_dict(self):
        return {
            'comment': self.comment,
            'rating': self.rating,
            'ratingDate': self.ratingDate,
            'profileName': self.profileName,
            'profileLocation':self.profileLocation,
            'profileLink': self.profileLink,
        }



def getYelpReviews(yelpLink,reviewList):



    driver.get(yelpLink)

    #GET RESTURENT NAME
    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"/html/body/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[1]/h1")))
    name = driver.find_element_by_xpath("/html/body/yelp-react-root/div[1]/div[3]/div[1]/div[1]/div/div/div[1]/h1").text
    resturentList.append(name)

    #WHILE NEXT BUTTON FOR MORE REVIEWS IS THERE WE WILL CONTINUE GETTING REVIEWS
    nextFound = True
    while nextFound:

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/yelp-react-root/div[1]/div[4]/div/div/div[2]/div/div[1]/main/div[2]/section[2]/div[2]/div/ul")))
        reviews = driver.find_elements_by_xpath("/html/body/yelp-react-root/div[1]/div[4]/div/div/div[2]/div/div[1]/main/div[2]/section[2]/div[2]/div/ul/li")
        #print(reviews)

        reviews_list = [r for r in reviews]

        for review in reviews_list:
            theReview = ReviewInfo('', '', '', '', '', '')




            #GET RATING
            #ratingDiv = review.find_element_by_xpath("./div/div[2]/div/div[1]")
            rating = review.find_element_by_xpath("./div/div[2]/div/div[1]/span")

            theReview.rating = rating.find_element_by_tag_name('div').get_attribute('aria-label').replace(" star rating", "")
            #print(rating.find_element_by_tag_name('div').get_attribute('aria-label').replace(" star rating", ""))

            #GET DATE OF RATING
            dateOfReview = review.find_element_by_xpath("./div/div[2]/div/div[2]/span")
            date = parse(dateOfReview.text).strftime('%Y-%m-%d')
            theReview.ratingDate = date
            #print(dateOfReview.text)

            #GET COMMENT
            try:
                commentParagraph = review.find_element_by_xpath("./div/div[4]/p/span")
                theReview.comment = commentParagraph.text
                #print(commentParagraph.text)

            except:
                commentParagraph = review.find_element_by_xpath("./div/div[3]/p/span")
                theReview.comment = commentParagraph.text
                #print(commentParagraph.text)

            #GET PROFILE NAME AND LINK TO PROFILE
            profileDiv = review.find_element_by_xpath("./div/div[1]/div/div[1]/div/div/div[2]/div[1]")
            profileLink = profileDiv.find_element_by_tag_name('a').get_attribute('href')
            profileName = profileDiv.find_element_by_tag_name('span').text
            profileLocation =None
            try:
                profilelocdiv = review.find_element_by_xpath("./div/div[1]/div/div[1]/div/div/div[2]/div[1]")
                profileLocation = profilelocdiv.find_element_by_class_name("css-qgunke").text

            except:
                pass

            else:
                try:
                    profilelocdiv = review.find_element_by_xpath("./div/div[1]/div/div[1]/div/div/div[2]/div[1]/div")
                    profileLocation = profilelocdiv.find_element_by_xpath("./div/span").text

                except:
                    pass

            theReview.profileLink = profileLink
            theReview.profileName = profileName
            theReview.profileLocation = profileLocation

            #print(profileName)
            #print(profileLocation.text)

            #ADD REVIEW TO LIST
            reviewList.append(theReview)
            #print(reviewList)


        #CHECK IF NEXT PAGE FOR MORE COMMENTS EXISTS - IF IT DOES NOT WE WILL STOP GETTING REVIEWS

        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH,"//a[@aria-label='Next']"))).click()


            print("clicked")
            #driver.execute_script('document.querySelector("#main-content > div:nth-child(8) > section:nth-child(2) > div.css-79elbk.border-color--default__09f24__NPAKY > div > div.pagination__09f24__VRjN4.border-color--default__09f24__NPAKY > div:nth-child(1) > div > div:nth-child(11) > span > a")')
            time.sleep(5)
        except Exception as e:
            nextFound = False
            print("No more next found")

            





if __name__ == '__main__':

    with open("resturents.txt") as f:
        lines = f.readlines()
        x = 0
        for line in lines:
            reviewList = []
            getYelpReviews(line,reviewList)
            rname = resturentList[x]
            pattern = '\W'
            name = re.sub(pattern,"",rname)
            try:
                manage_database.createTable(name)
            except:
                pass
            manage_database.insertData(name,reviewList)
            x +=1
    driver.close()