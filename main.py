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