from google.appengine.ext import db


class Purchase(db.Model):
    user = db.UserProperty(required=True)
    title = db.StringProperty(required=True)
    description = db.StringProperty(multiline=True)
    priority = db.IntegerProperty()
    data = db.DateTimeProperty(auto_now_add=True)
    
    def getTitle(self):
        return self.title
    
    def getDescription(self):
        return self.description
    
    def getPriority(self):
        return self.priority
    
    def getDataTime(self):
        return self.data
    
    