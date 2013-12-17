from google.appengine.ext.webapp import template

register = template.create_template_register()

@register.filter(name='getTitle')
def getTitle(purchase):
    return purchase.getTitle()

@register.filter(name='getDescription')
def getDescription(purchase):
    return purchase.getDescription()

@register.filter(name='getPriority')
def getPriority(purchase):
    return purchase.getPriority()

@register.filter(name='getData')
def getDataTime(purchase):
    return purchase.getDataTime()

register.filter(getTitle)
register.filter(getDescription)
register.filter(getPriority)
register.filter(getDataTime)

