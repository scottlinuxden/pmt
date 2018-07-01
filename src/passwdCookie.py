#-*- Mode: Python; tab-width: 4 -*-
import Cookie
import os
import sha

class authCookie:
    def __init__(self):
        self.cookie = None

    def _get(self):
        self.cookie = Cookie.SimpleCookie()
        if os.environ.has_key('HTTP_COOKIE'):
            self.cookie.load(os.environ['HTTP_COOKIE'])
        else:
            self.cookie = None
  #      try:
  #      self.cookie = Cookie.Cookie()
  #      self.cookie.load(os.environ['HTTP_COOKIE'])
  #      except KeyError:
  #          self.cookie = None

    def _set(self,username,password):
        self.get()
        if self.cookie == None:
            self.cookie = Cookie.SimpleCookie()
        self.cookie['username'] = username
        self.cookie['password'] = sha.new(password).digest()
        self.cookie['username']['expires'] = 60*60*24*100
        self.cookie['password']['expires'] = 60*60*24*100


    def get(self):
        self._get()
        if self.cookie != None:
            try:
                return (self.cookie['username'].value,
                        self.cookie['password'].value)
            except:
                return (None,None)

        else:
            return (None, None)

    def set(self,username,password):
        self._set(username,password)

    def outputToBrowser(self,genHeader=0):
        if genHeader:
            print "Content-type: text/html"
        if self.cookie != None:
            print self.cookie
        print

    def logout(self):
        self._get()
        if self.cookie != None:
            self._set("pending_delete","pending_delete")
            self.cookie['username']['expires'] = -60000
            self.cookie['password']['expires'] = -60000

if __name__ == "__main__":
    loginCookie = authCookie()
    loginCookie.set('rsdavis','test')
    loginCookie.outputToBrowser()
    (username,password) = loginCookie.get()
    loginCookie.logout()
    
