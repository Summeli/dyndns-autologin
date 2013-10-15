__author__ = 'Antti Pohjola'

# DynDns autologin
# automatically logins to dyndns
import webapp2
import logging
import urllib
import urllib2
import cookielib
import time

class Settings:
    dyndns_username = ""
    dyndns_password = ""
    loginurl = "https://account.dyn.com/entrance"
    loginredirecturl = "https://account.dyn.com/"
    logouturl = "https://account.dyn.com/entrance/?__logout=1"


class HTMLSession:
    cj = None
    opener = None
    txHeaders = None
    
    def __init__(self, txHeaders):
        #The CookieJar will hold any cookies necessary throughout the login process.
        self.cj = cookielib.CookieJar()
        self.txHeaders = txHeaders
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setHeaders(self, txheaders):
        self.txHeaders = txHeaders
    
    def getHeaders(self):
        return self.txHeaders

    def openURI(self, uri, txdata):
        try:
            req = urllib2.Request(uri, txdata, self.txHeaders)
            # create a request object
            handle = urllib2.urlopen(req)
            # and open it to return a handle on the url
        except IOError as e:
            logging.debug("IOError, now its time to panic and freak out")
            return None
        else:
            return handle.read()


class CronController(webapp2.RequestHandler):
    def getHiddenRandHTMLResponse(self,response):
        target = "<input type=\'hidden\' name=\'multiform\' value=\'"
        return response[response.find(target)+len(target):response.find(target)+len(target)+34]

    def checkLogin(self,response):
        target = "<title>My Dyn Account</title>"
        if response.find(target) == -1:
            return False
        return True

    def autologin(self):
        hiddenval = ""
        txHeaders = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0'}
        hiddenval = ""    
        txdata = None

        myhtmlSession = HTMLSession(txHeaders)
        response = myhtmlSession.openURI(Settings.loginurl, None)

        if response == None:
            logging.debug("Empty response")
            return
        
        hiddenval = self.getHiddenRandHTMLResponse(response)
        txdata = urllib.urlencode({'username':Settings.dyndns_username, 'password':Settings.dyndns_password, 'multiform':hiddenval, 'submit': "Log in"})
        response = myhtmlSession.openURI(Settings.loginurl, txdata)
        if response == None:
            loging.debug("login failed: ")
            return
        
        #the response is 302 to new url, load it, and see if the login succeed
        response = myhtmlSession.openURI(Settings.loginredirecturl,None)
        if self.checkLogin(response):
            logging.info("Login succeed to dynDns")

        #sleep a while before logout
        time.sleep(5)

        response = myhtmlSession.openURI(Settings.logouturl, None)
        if response == None:
            logging.info("Logout FAILED")

        logging.info("Logout Succeed")


    def get(self):
        self.autologin()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('DNS refressed!')

app = webapp2.WSGIApplication([('/cron/autologin', CronController)], debug=True)
logging.debug("loaded cron")

