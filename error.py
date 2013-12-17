import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class ErrorPage(webapp.RequestHandler):
    
    def get(self):
        logging.info("Error page")
        self.response.out.write('<h1>Page not found!</h1>')
        
        
application = webapp.WSGIApplication([('/.*', ErrorPage)
                                      ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()