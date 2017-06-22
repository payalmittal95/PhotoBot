# importing access token from keys file and requests library
from keys import ACCESS_TOKEN
import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

BASE_URL = "https://api.instagram.com/v1/"


# Defining function for our own info
def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_TOKEN)
    print "GET request URL : %s." % (request_url)
    user_info = requests.get(request_url).json()
    print user_info
    if user_info['meta']['code'] == 200:
        if len(user_info["data"]):
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
            img_name = own_media['data'][0]['id'] + '.jpeg'
            img_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, img_name)
            print "image name= " + str(img_name)
            print "Your image has been downloaded!"
        else:
            print "The photo doesn't exist."
    else:
        print "Status code other than 200 recieved."


# Function to get posts of a user by username
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User doesn't exist"
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'Requestig url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + ".jpeg"
            img_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "Post doesn't exist"
    else:
        print "Status code other than 200 received. [%d]" % user_media['meta']['code']


# Function declaration to get the ID of the recent post of a user by username
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print "Requesting url : %s" % request_url
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
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
    print "POST Requesting URL : %s" % request_url
    post_a_like = requests.get(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print "Post liked successfully!"
    else:
        print "Your like was unsuccessful!"
        print "Status code other than 200 received"


# Function declaration to get the list of comments on the recent post of a user
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = ( BASE_URL + "media/%s/comments?access_token=%s") % (media_id, ACCESS_TOKEN)
    print "GET Requesting URL : %s" % request_url
    comment_list = requests.get(request_url).json()

    if (comment_list['meta']['code'] == 200):
        if len(comment_list['data']):
            for x in range(0, len(comment_list['data'])):
                print "%s : %s" % (comment_list['data'][x]['from']['username'], comment_list['data'][x]['text'])
        else :
            print "No comments on the post."
    else :
        print "Error in receiving the comment list. ( Status code other than 200 received. [%d] )" % comment_list['meta']['code']

def make_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + "media/%s/comments" % media_id
    payload = {'access_token': ACCESS_TOKEN, "text": raw_input("Please enter your comment. : ") }
    print "POST Requesting URL : %s" % request_url
    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again! [%d]" + make_comment['meta']['code']

#Function to make delete negative comments from the recent post
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'

make_a_comment("hermione_granger97")