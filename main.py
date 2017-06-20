#importing access token from keys file and requests library
from keys import ACCESS_TOKEN
import requests, urllib
BASE_URL = "https://api.instagram.com/v1/"

#Defining function for our own info
def self_info():
    request_url = (BASE_URL + "users/self/?access_token=%s") % (ACCESS_TOKEN)
    print "GET request URL : %s." % (request_url)
    user_info = requests.get(request_url).json()
    print user_info
    if user_info['meta']['code'] == 200:
        if len(user_info["data"]):
            print "Username: %s." % (user_info['data']['username'])
            print "Number of followers: %s." %(user_info['data']['counts']['followed_by'])
            print "Following: %s." % (user_info['data']['counts']['follows'])
            print "Number of posts: %s." % (user_info['data']['counts']['follows'])
        else:
            print "User does not exist."
    else:
        print "Status code other than 200 received."
        print user_info['meta']['code']

#Function to get a user's id by their username
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
        print "status code : %d" % user_info['meta']['code']
        return None

#function to get a user's information by their user-name
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print "User doesn't exist."
        exit()
    else:
        print "user id= %d" % user_id
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_TOKEN)
    print "Requesting url : %s" % request_url
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else :
            print "There is no data for this user."
    else :
        print "Status code other than 200 recieved.[%d]" % user_info['meta']['code']

#Function to download own image post.
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print "Requesting url for : %s" % request_url
    own_media = requests.get(request_url).json()
    #condition to check the status code.
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            img_name = own_media['data'][0]['id'] + '.jpeg'
            img_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url, img_name)
            print "Your image has been downloaded!"
        else:
            print "The photo doesn't exist."
    else :
        print "Status code other than 200 recieved [%d]" % own_media['meta']['code']

#Function to get posts of a user by username
def get_user_post(insta_username):
    user_id = get_user_id()
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
            urllib.urlretrieve(img_url,image_name)
            print "Your image has been downloaded!"
        else:
            print "Post doesn't exist"
    else:
        print "Status code other than 200 received. [%d]" % user_media['meta']['code']

#Function declaration to get the ID of the recent post of a user by username
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
    else :
        print "Status code other than 200 received [%d]" % user_media['meta']['code']
        exit()