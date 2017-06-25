# importing access token from keys file.
# importing required libraries such as requests, urllib, textblob.
from keys import ACCESS_TOKEN
import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

BASE_URL = "https://api.instagram.com/v1/"


# Defining function for our own info
def self_info():
    # creating the url to access information.
    request_url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_TOKEN)
    print "GET request URL : %s." % (request_url)
    # making a get call to the url and converting it to a json object.
    user_info = requests.get(request_url).json()
    # checking the status code of the returned json object.
    if user_info['meta']['code'] == 200:
        # noinspection PyInterpreter
        if len(user_info["data"]):
            # printing our on=wn informaton.
            print "Username: %s." % (user_info['data']['username'])
            print "Number of followers: %s." % (user_info['data']['counts']['followed_by'])
            print "Following: %s." % (user_info['data']['counts']['follows'])
            print "Number of posts: %s." % (user_info['data']['counts']['follows'])
        else:
            print "User does not exist."
    else:
        print "Status code other than 200 received."


# Function to get a user's id by their username
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        return None

# function to get a user's information by their user-name
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User doesn't exist."
        exit()
    else:
        print "user id= " + str(user_id)
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_TOKEN)
    print "Requesting url : %s" % request_url
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        # printing user information if there is data present.
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print "There is no data for this user."
    else:
        print "Status code other than 200 recieved."


# Function to download own image post.
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print "Requesting url for : %s" % request_url
    own_media = requests.get(request_url).json()
    # condition to check the status code.
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            # getting image information from own_media
            img_name = own_media['data'][0]['id'] + '.jpeg'
            img_url = own_media['data'][0]['images']['standard_resolution']['url']
            # downloading the image using its url and saving it with img_name.
            urllib.urlretrieve(img_url, img_name)
            print "image name= " + str(img_name)
            print "Your image has been downloaded!"
        else:
            print "The photo doesn't exist."
    else:
        print "Status code other than 200 recieved."

#dictionary to define keys to identify posts with minimum or maximum likes.
like_count = {}

#function to check post with  minimum and maximum likes.
def num_of_likes(insta_username, ):
    user_id = get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            like_count["min_id"] = 0
            like_count["max_id"] = 0
            like_count['min'] = user_media['data'][0]['likes']['count']
            like_count['max'] = user_media['data'][0]['likes']['count']
            for x in range(0, len(user_media['data'])):
                #to find the post with minimum likes.
                if like_count["min"] > user_media['data'][x]['likes']['count']:
                    like_count['min_id'] = x
                    like_count['min'] = user_media['data'][x]['likes']['count']
                #to find the post with maximum likes.
                if like_count['max'] < user_media['data'][x]['likes']['count']:
                    like_count['max_id'] = x
                    like_count['max'] = user_media['data'][x]['likes']['count']

# Function to get posts of a user by username
def get_user_post(insta_username):
    # getting user id from username.
    user_id = get_user_id(insta_username)
    if user_id is None:
        print "User doesn't exist"
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'Requestig url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    i = None
    #to display the selection criteria
    while i is not 1 or 2 or 3:
        print "Select criteria for selecting post : "
        print "1) Minimum Likes.\n2) Maximum Likes.\n3)Most Recent Post."
        post_choice = int(raw_input("Please Enter Your Post Selection Criteria : "))
        if post_choice == 1:
            i = like_count['min_id']
        elif post_choice == 2:
            i = like_count['max_id']
        elif post_choice == 3:
            i = 0
        else:
            print "Wrong choice. Enter one of the above 3."

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            # getting image information from user_media
            image_name = user_media['data'][i]['id'] + ".jpeg"
            img_url = user_media['data'][i]['images']['standard_resolution']['url']
            # downloading the image using its url and saving it with img_name.
            urllib.urlretrieve(img_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "Post doesn't exist"
    else:
        print "Status code other than 200 received. [%d]" % user_media['meta']['code']


# Function declaration to get the ID of the recent post of a user by username
def get_post_id(insta_username):
    # getting user-id from username.
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print "Requesting url : %s" % request_url
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            # returning the id of the post.
            print user_media['data'][0]['id']
            return user_media['data'][0]['id']
        else:
            print "There is no recent post"
            exit()
    else:
        print "Status code other than 200 received"
        exit()


# Function to get the list of people who have liked the recent post of a user
def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    print media_id
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, ACCESS_TOKEN)
    print "Requesting URL : %s" % request_url
    likes_info = requests.get(request_url).json()

    if likes_info['meta']['code'] == 200:
        if len(likes_info['data']):
            # traversing through likes_info to print usernames of people who liked the post.
            for x in range(0, len(likes_info['data'])):
                print likes_info['data'][x]['username']
        else:
            print "no user has liked this post yet."
    else:
        print "Status code other than 200  received"


# Function to like a post
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % media_id
    payload = {'access_token': ACCESS_TOKEN}
    print "GET Requesting URL : %s" % request_url
    post_a_like = requests.get(request_url, payload).json()

    if post_a_like['meta']['code'] == 200:
        print "Post liked successfully!"
    else:
        print "Your like was unsuccessful!"
        print "Status code other than 200 received"


# Function declaration to get the list of comments on the recent post of a user
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/comments?access_token=%s") % (media_id, ACCESS_TOKEN)
    print "GET Requesting URL : %s" % request_url
    comment_list = requests.get(request_url).json()

    if (comment_list['meta']['code'] == 200):
        if len(comment_list['data']):
            # traversing through comment_list to print username and comment text.
            for x in range(0, len(comment_list['data'])):
                print "%s : %s" % (comment_list['data'][x]['from']['username'], comment_list['data'][x]['text'])
        else:
            print "No comments on the post."
    else:
        print "Error in receiving the comment list. ( Status code other than 200 received. [%d] )" % \
              comment_list['meta']['code']


# function added to post a comment on a media.
def make_a_comment(insta_username):
    # getting media-id.
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + "media/%s/comments" % media_id
    payload = {'access_token': ACCESS_TOKEN, "text": raw_input("Please enter your comment. : ")}
    print "POST Requesting URL : %s" % request_url
    # making a post request to post the comment.
    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again! [%d]" + make_comment['meta']['code']


# Function to make delete negative comments from the recent post
def del_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    # getting the list of comments.
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                # getting comment-id and comment-text from list of comments.
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                # Condition to check if the comment is negative or positive.
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    # deleting the comment if its negative sentiment is more than the positive sentiment.
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()
                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print "Comment couldn't be deleted. ( Status code other than 200 recieved. [%d] )" % \
                              delete_info['meta']['code']
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print "Unable to recieve comments. status code other than 200 received. [%d]" % comment_info['meta']['code']

#function to read and return caption on a post.
def get_media_info(media_id):
    request_url = (BASE_URL + 'media/%s?access_token=5629236876.1cc9688.86db895c038043b5960dc2949785299a') % (media_id)
    print "GET Requesting URL for media info : %s" % request_url
    media_info = requests.get(request_url).json()
    caption = media_info['data']['caption']['text']
    return caption

#list that contains common words for a natural calamity.
natural_calamity_words = ['#flood', '#earthquake', '#relief', '#help']
#function to get the recent media in a given area using location-id
def get_media_by_location(location_id):
    request_url = (BASE_URL + 'locations/%s/media/recent?access_token=5629236876.1cc9688.86db895c038043b5960dc2949785299a') % location_id
    media_info = requests.get(request_url).json()

    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            #traversing through all the images for the given location id
            for x in range(0, len(media_info['data'])):
                media_id = media_info['data'][x]['id']
                #receiving the caption for the given image.
                caption = get_media_info(media_id)
                #to check if the caption contains any word that relates to a natural calamity.
                for i in natural_calamity_words:
                    if i in caption:
                        print "This image was for the natural calamity : %s" % i
                        #downloading the image related to a natural calamity.
                        image_name = media_info['data'][x]['id'] + ".jpeg"
                        img_url = media_info['data'][x]['images']['standard_resolution']['url']
                        # downloading the image using its url and saving it with img_name.
                        urllib.urlretrieve(img_url, image_name)
                        print "The image has been downloaded."
                        break
        else:
            print "There are no images for this location id"
    else :
        print "satus code other than 200 received."
#function to get location id by latitude and longitude.
def get_location_id():
    request_url = (BASE_URL + 'locations/search?lat=28.6303&lng=77.2201&distance=0&access_token=5629236876.1cc9688.86db895c038043b5960dc2949785299a')
    print "Get Requesting URL to get location id : %s"% request_url
    location_info = requests.get(request_url).json()

    if location_info['meta']['code'] == 200:
        if len(location_info['data']):
            #traversing through vthe list of location-ids received for the given coordinates.
            for x in range(0, len(location_info['data'])):
                location_id = location_info['data'][x]['id']
                print "For Location ID = " + str(location_id)
                #checking the recent media for the given location-id.
                get_media_by_location(location_id)
        else:
            print "No location id for these coordinates."
    else:
        print "status code other than 200 recieved."

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!\nHere are your menu options :'
        print "a.Get your own details\nb.Get details of a user by username"
        print "c.Get your own recent post\nd.Get the recent post of a user by username"
        print "e.Get a list of people who have liked the recent post of a user"
        print "f.Like the recent post of a user\ng.Get a list of comments on the recent post of a user"
        print "h.Make a comment on the recent post of a user\ni.Delete negative comments from the recent post of a user"
        print "j.Analyse the caption and determine if it is about a natural calamity\nk.Exit"
        #to find the pic with maximum & minimum likes.

        choice = raw_input("Enter you choice : ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            num_of_likes(insta_username)
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            num_of_likes(insta_username)
            get_like_list(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            num_of_likes(insta_username)
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            num_of_likes(insta_username)
            get_comment_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            num_of_likes(insta_username)
            make_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            num_of_likes(insta_username)
            del_negative_comment(insta_username)
        elif choice == "j":
            get_location_id()
        elif choice == "k":
            exit()
        else:
            print "Wrong Option. Please select one of the options."
# function call to start the bot.
start_bot()
