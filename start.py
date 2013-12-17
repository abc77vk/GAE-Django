import logging
import os

from google.appengine.api import users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from Purchase import Purchase


webapp.template.register_template_library('mytags.testtag')



def getUser(handler,uri='/'):
    user = users.get_current_user()
    if user:
        logging.info('User=' + str(user))
        return user
    else:
        handler.redirect(users.create_login_url(uri))
        
        
class AddNewPurchase(webapp.RequestHandler):
    
    def post(self):
        user = getUser(self, '/addpurchase')
        title = unicode(self.request.get('title'))
        description = unicode(self.request.get('description'))
        priority = unicode(self.request.get('priority'))
        logging.info('Post request')
        logging.info('Message from form title:' + title)
        logging.info('Message from form description:' + description)
        logging.info('Message from form priority:' + priority)
        purchase = Purchase(user=user,title=title,description=description, priority = int(priority))
        purchase.put()
        self.redirect('/addpurchase')
        
                    

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        param = {'user' : user}
        if user is None:
            path = os.path.join(os.path.dirname(__file__), 'view/hello.html')
        else:
            path = os.path.join(os.path.dirname(__file__), 'view/main.html')
        self.response.out.write(template.render(path, param))
        
class AddPurchase(webapp.RequestHandler):
    
    def get(self):
        user = getUser(self,self.request.uri)
        param = {'addmark':'yes', 'user' : user}
        path = os.path.join(os.path.dirname(__file__), 'view/add_purchase.html')
        self.response.out.write(template.render(path, param))
        
class ShowPurchases(webapp.RequestHandler):
    
    def get(self):
        logging.info('ShowPurchases::get()')
        user = getUser(self,self.request.uri)
        q = Purchase.all()
        q.filter('user', user)
        q.order('-priority')
        purchases = q.fetch(100)
        param = {'user' : user, 'purchases' : purchases}
        path = os.path.join(os.path.dirname(__file__), 'view/show_purchases.html')
        self.response.out.write(template.render(path, param))
        
class Logout(webapp.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        if user: self.redirect(users.create_logout_url('/'))
        else: self.redirect('/')
        
class Login(webapp.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        if user is None: self.redirect(users.create_login_url('/'))
        else: self.redirect('/')
      
      
def removeElement(key):
    logging.info('transaction started')
    purchase = Purchase.get(key)
    if purchase: purchase.delete()
    logging.info('transaction finished')
      
      
class RemoveElement(webapp.RequestHandler):
    
    def get(self):
        elementKey = self.request.get('element')
        db.run_in_transaction(removeElement,elementKey)
        logging.info('next action - redirect')  
        self.redirect('/showpurchases')

        
        
application = webapp.WSGIApplication([('/', MainPage),
                                      ('/index.html', MainPage),
                                      ('/addpurchase', AddPurchase),
                                      ('/showpurchases', ShowPurchases),
                                      ('/logout', Logout),
                                      ('/login', Login),
                                      ('/addnewpurchase', AddNewPurchase),
                                      ('/remove',RemoveElement)
                                      ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
