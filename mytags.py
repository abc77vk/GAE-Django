from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.inclusion_tag('view/index.html') 
def getName():
    return {'getName':'Custom tag'} 

