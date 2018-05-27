from twitter import Twitter, OAuth
import tweepy
import re
import json
from termcolor import colored
from textblob import TextBlob
from paralleldots import set_api_key, get_api_key, sentiment
import nltk
from nltk.corpus import *
from nltk import Counter
#-----------------------------------------------------------------------------------------------------------------------

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

print (colored("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tWELCOME TO TWITTER-BOT", color= 'green', attrs=['bold']))

API_KEY = 'K0jSV4Y344tjaDIhnPMvMXcdS'
API_SECRET = 'eKVkaa1XPsHWUeEwCEdKSVxXsppLNy4w9pAjRbaUFUxOHKqU7C'
ACCESS_TOKEN = '2974951531-VNDr97JIjxSsNpIsTvhQsJqpOKBeXOdGESW7qjv'
ACCESS_TOKEN_SECRET = 'LjpuABZxi3wZfNTjMg98Im7Iof0U8l9GnYYUf8snCTSNO'

twitter_oauth = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET)
twitter = Twitter(auth = twitter_oauth)

oauth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(oauth)
#-----------------------------------------------------------------------------------------------------------------------

#FOR DISPLAYING MY DETAILS
def details():
    user = api.me()
    print (colored("\nMY DETAILS", color='red', attrs=['underline']))
    print 'Name: '  + user.name
    print 'Location: ' + user.location
    print 'Friends: ' + str(user.friends_count)
    print (colored("------------------------------------------------------------------------------------------"
                   "---------------------------------------------------------------------------------------------",
                   color='green'))
#-----------------------------------------------------------------------------------------------------------------------

# FOR GETTING QUERY

def get_tweets(query):
    tweets = twitter.search.tweets(q='#' +query, count=200)
    return tweets

#-----------------------------------------------------------------------------------------------------------------------
def GetSearch():
    global tweets
    tweet_input = raw_input("Enter the hash tag:" + colored("#",color='red'))
    tweet_input = "#" + tweet_input
    tweets = api.search(q=tweet_input)

    status = tweets[0]
    json_str = json.dumps(status._json,indent=4,sort_keys=True)
    print(json_str)

# -----------------------------------------------------------------------------------------------------------------------
# FOR GETTING NUMBER OF FOLLOWERS

def get_num_followers(query):
    num_followers = 0
    tweets = get_tweets(query)
    #print type(tweets)
    for each_tweet in tweets['statuses']:
        print (colored("-----------------------------------------------------------------------------------------------"
               "---------------------------------------------------------------------------------------", color= 'blue'))
        print "Name: " + each_tweet['user']['screen_name']
        print "Followers: " + str(each_tweet['user']['followers_count'])
        # print each_tweet['user']['location']
        num_followers += each_tweet['user']['followers_count']
    return  num_followers


# FOR GETTING SENTIMENTS

def get_sentiments(query):
    p = 0
    n=0
    ne = 0
    set_api_key('nevysH2HFB0VkHllFav0tUJitebNhLvzU0O5IM9cOTc')
    get_api_key()
    public_tweets = api.search(query)
    for tweet in public_tweets:
        text = tweet.text
        print (colored("-----------------------------------------------------------------------------------------"
                       "----------------------------------------------------------------------------------------------",
                       color='green'))
        print (colored(tweet.text, color='blue'))
        r = sentiment(tweet.text)
        print(colored(r, color= 'red'))
        result = r['sentiment']
        if result == "positive":
            p = p+1
        elif  r['sentiment'] == "neutral":
            n = n+1
        else:
            ne = ne+1
    print (colored("------------------------------------------------------------------------------------------"
                   "-----------------------------------------------------------------------------------------------",
                   color='cyan'))
    print "Maximum positive comments: ", p
    print "Maximum neutral comments: ", n
    print "Maximum negative comments: ", ne
    print (colored("-----------------------------------------------------------------------------------------"
                   "----------------------------------------------------------------------------------------------",
                   color='cyan'))

#-----------------------------------------------------------------------------------------------------------------------

# FOR GETTING LOCATION, LANGUAGE AND TIME ZONE

def llt(query):

    public_tweets = get_tweets(query)


    # for tweet in public_tweets['statuses']:
    #     print (colored("Time Zone: ", color='red', attrs=['bold']) + tweet['user']['created_at'])
    #     print (colored("Language: ", color='red', attrs=['bold']) + tweet['user']['lang'])
    #     print (colored("Location: ", color='red', attrs=['bold']) + tweet['user']['location'])
    #     print (colored("----------------------------------------------------------------------------------------"
    #                    "---------------------------------------------------------------------------------------------",
    #                    color='green'))

    global time_zone1, loca, lang
    location = {}
    language = {}
    time_zone = {}
    for tweet in public_tweets['statuses']:
        loca = tweet['user']['location'] #tweet.user.location
        lang = tweet['user']['lang'] #tweet.user.lang
        time_zone1 = tweet['user']['created_at'] #tweet.user.time_zone
        if loca in location:
            location[loca] += 1
        else:
            location[loca] = 1
        if lang in language:
            language[lang] += 1
        else:
            language[lang] = 1
        if time_zone1 in time_zone:
            time_zone[time_zone1] += 1
        else:
            time_zone[time_zone1] = 1

    # limiting the display of the values
    if None in time_zone:
        del time_zone[None]
    if '' in time_zone:
        del time_zone['']
    if '' in language:
        del language['']
    if '' in location:
        del location['']
    if None in location:
        del location[None]
    if None in language:
        del language[None]
    print (colored("----------------------------------------------------------------------------------------"
                       "---------------------------------------------------------------------------------------------",
                       color='green'))
    language_count = dict(Counter(language).most_common(5))
    print (colored("Language: ", color='red', attrs=['bold']))
    print(language_count)
    print (colored("----------------------------------------------------------------------------------------"
                   "---------------------------------------------------------------------------------------------",
                   color='green'))
    location_count = dict(Counter(location).most_common(5))
    print (colored("Location: ", color='red', attrs=['bold']))
    print(location_count)
    print (colored("----------------------------------------------------------------------------------------"
                   "---------------------------------------------------------------------------------------------",
                   color='green'))
    time_zone_count = dict(Counter(time_zone).most_common(5))
    print (colored("Time Zone: ", color='red', attrs=['bold']))
    print(time_zone_count)
    print (colored("----------------------------------------------------------------------------------------"
                   "---------------------------------------------------------------------------------------------",
                   color='green'))
#-----------------------------------------------------------------------------------------------------------------------

# FOR COMPARISION OF MODI AND TRUMP TWEETS

def Comparision():

    # FOR MODI
    count = 0
    new_tweets = api.user_timeline(screen_name = '@narendramodi', count = 200, tweet_mode='extended')
    for tweet in new_tweets:
        print(tweet.full_text)
        text = tweet.full_text
        temp = []
        temp.append(text)
        temp1 = temp
        words = re.sub(r"http\S+", "", str(temp1))
        word = words.split()
        for i in word:
            i = i.upper()
            if i == "USA" or i == "US" or i == "America" or i == "United States of America":
                count = count + 1
    print (colored("*****************************************************************************************"
                   "********************************************************************************************",
                   color='yellow'))



    #FOR TRUMP
    count1 = 0
    new_tweets = api.user_timeline(screen_name='@realDonaldTrump', count=200, tweet_mode='extended')
    for tweet in new_tweets:
        print(tweet.full_text)
        text = tweet.full_text
        temp = []
        temp.append(text)
        temp1 = temp
        words = re.sub(r"http\S+"," ", str(temp1))
        word = words.split()
        for i in word:
            i = i.lower()
            if i == "India" or i == "INDIA":
                count1 = count1 + 1
    print (colored("-----------------------------------------------------------------------------------------"
                   "---------------------------------------------------------------------------------------------",
                   color='cyan'))
    print "Number of times Narendra Modi mentioned 'USA', 'US', 'America', or 'United States Of America: ", count
    print "Number of times Donald Trump mentioned 'India': ", count1
    print (colored("-----------------------------------------------------------------------------------------"
                   "---------------------------------------------------------------------------------------------",
                   color='cyan'))

#-----------------------------------------------------------------------------------------------------------------------

# FOR DETERMINING TOP USAGE STOPWORDS

def Topusage():
    new_tweets = api.user_timeline(screen_name='@narendramodi', count=200, tweet_mode='extended')
    for tweet in new_tweets:
        #print(tweet.full_text)
        temp = []
        temp.append(tweet.full_text)
        temp1 = temp
        import re
        words = re.sub(r"http\S+"," ", str(temp1))
        word = words.split()
        word1 = [w for w in word if w in stop_words]
        for w in word1:
            if w not in stop_words:
                word1.append(w)
        num = Counter(word1).most_common(10)
        #print word1
        print(num)

#-------------------------------------------------------

# FOR UPDATING STATUS

def tweet_status():
    status = raw_input("Enter your new tweet: ")
    api.update_status(status)
    print(colored("successful",color='green'))
#-----------------------------------------------------

# MAIN FUNCTION

def main():
 print (colored("========================================================================================="
                   "=============================================================================================",
                   color='green'))
 while (True):

     user_choice = input("\nWhat would you like to do? \n"
                   "1. Show my details.\n"
                   "2. Retrieve tweets.\n"
                   "3. Count the number of followers. \n"
                   "4. Determine the sentiments of people Tweeting using a certain has tag. \n"
                   "5. Determining the location, timezone and language of people Tweeting using a certain has tag. \n"
                   "6. Comparision of tweets by Narendera Modi and Donald Trump. \n"
                   "7. Determining Top Usage. \n"
                   "8. Tweet a message from your account. \n"
                   "9. Exit\n"
                   "Enter Choice: ")

     if user_choice == 1:
         details()

     elif user_choice == 2:
         GetSearch()

     elif user_choice == 3:
        print ("Chosen to count the number of followers.")
        user_input = raw_input("Enter the hash tag: ")
        print colored("\n Maximum number of people who might have seen this hash tag are:",color='red')+" %s " % (get_num_followers(user_input))

     elif user_choice == 4:
         user_input = raw_input("Enter the hash tag: ")
         get_sentiments(user_input)

     elif user_choice == 5:
        user_input = raw_input("Enter the hash tag: ")
        llt(user_input)

     elif user_choice == 6:
        Comparision()

     elif user_choice == 7:
          Topusage()

     elif user_choice == 8:

         tweet_status()

     elif user_choice == 9:
       break
     else:
        print("wrong choice try again.")
        exit()
main()