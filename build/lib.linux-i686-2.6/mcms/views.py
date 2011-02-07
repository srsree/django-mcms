from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from mcms.models import *

#    import pdb; pdb.set_trace()

RECORDS_PER_PAGE = 15


def index(request):
    t = loader.get_template('index.html')
    msg_to_user = ''
    project = ''
    event = ''
    news = ''
    try:
        projectList = Project.objects.all().filter(live=True).order_by('?')[:1]
        project = projectList[0]
    except:
        msg_to_user += "No Project found. "
    #
    # Top news
    try:
        newsList = Article.objects.all().filter(live=True).filter(category__name='news').order_by('-createdOn','-listingOrder','title')[:1]
        news = newsList[0]
        
    except:
        msg_to_user += "No News found. "
        
    #
    # Top event
    try:
        eventList = Event.objects.all().filter(live=True).order_by('-listingOrder','-startDate','title')[:1]
        event = eventList[0]
    except:
        msg_to_user += "No Event found"
        
    c = Context({
        'project': project,'news': news,'event': event,'msg_to_user':msg_to_user,
    })
    return HttpResponse(t.render(c))

def getProjectList(active=True):
    t = loader.get_template('projects_listing.html')
    msg_to_user = ''
    try:
        latest_projects_list = Project.objects.all().filter(live=active).order_by('listingOrder','title')[:RECORDS_PER_PAGE]
        if active:
            pageTitle = "List of active projects"
        else:
            pageTitle = "Our completed projects"
    except:
        msg_to_user = "This section is being updated"
    c = Context({
        'latest_projects_list': latest_projects_list,'page_title':pageTitle,'msg_to_user':msg_to_user,'active':active
    })
    return HttpResponse(t.render(c))
    
def listOngoingProjects(request):
    return getProjectList()
    
def listArchiveProjects(request):
    return getProjectList(active=False)


    
def projectDetails(request, projSlug, projArticleSlug=''):
    project_articles = []
    proj = ''
    show_article = ''
    msg_to_user = ''
    t = loader.get_template('project_details.html')
    try:
        proj = Project.objects.get(url4SEO=projSlug)
        project_articles = ProjectArticle.objects.all().filter(live=True).filter(project = proj.id)
        
        if projArticleSlug:
            show_article = ProjectArticle.objects.get(url4SEO=projArticleSlug)
        else:
            show_article = project_articles[0]
             
    except:
        msg_to_user = 'Selected project or project article is still being updated!'
        
    c = Context({
        'project_articles': project_articles,'project':proj, 'show_article':show_article, 'msg_to_user':msg_to_user,
    })
    return HttpResponse(t.render(c))

def articleList(request,category=''):
    t = loader.get_template('article_listing.html')
    article_list = []
    
    msg_to_user = ''
    try:
        if category:
            article_list = Article.objects.all().filter(live=True).filter(category__name=category).order_by('-listingOrder')[:RECORDS_PER_PAGE]
    except:
        msg_to_user = 'Selected category\'s article are still being updated!'
        
    c = Context({
        'article_list': article_list,'category':category, 'msg_to_user':msg_to_user
    })
    return HttpResponse(t.render(c))
    
    
def articleDetails(request,category='',slug=''):
    t = loader.get_template('article_details.html')
    article_list = []
    article = ''
    msg_to_user =''
    try:
        if category:
            article_list = Article.objects.all().filter(live=True).filter(category__name=category)[:RECORDS_PER_PAGE]
            if len(article_list) <2:
                article_list = []
        if category and slug:
           article = Article.objects.get(url4SEO = slug)
    except:
        msg_to_user = 'Selected Category or article are still being updated!'
        
    c = Context({
        'article_list': article_list,'category':category, 'article':article,'msg_to_user':msg_to_user
    })
    return HttpResponse(t.render(c))



    
def eventList(request):
    event_list = []
    t = loader.get_template('event_listing.html')
    msg_to_user = ''
    #try:
    event_list = Event.objects.all().filter(live=True).order_by('-listingOrder','-startDate')[:RECORDS_PER_PAGE]
    #except:
    #msg_to_user = "Resource section is being updated"
    c = Context({
        'event_list': event_list,'msg_to_user':msg_to_user,
    })
    return HttpResponse(t.render(c))
    
    
def eventDetails(request,eventSlug=''):
    event = ''
    msg_to_user = ''
    t = loader.get_template('event_details.html')
    try:
        if eventSlug:
            event = Event.objects.get(url4SEO=eventSlug)
        else:
            event = Event.objects.all().filter(live=True).order_by('-listingOrder','startDate','title')[:1]
             
    except:
        msg_to_user = 'Selected event is still being updated!'
        
    c = Context({
        'event': event, 'msg_to_user':msg_to_user,
    })
    return HttpResponse(t.render(c))


def resources(request,resourceType='tool-kit'):
    resource_list = []
    t = loader.get_template('resource_listing.html')
    msg_to_user = ''
    pageTitle = ''
    try:
        resource_list = Resource.objects.all().filter(live=True).filter(resourceType=resourceType)[:RECORDS_PER_PAGE]
        pageTitle = u"List of "+resourceType+" resources"
    except:
        msg_to_user = "Resource section is being updated"
    c = Context({
        'resource_list': resource_list,'page_title':pageTitle,'msg_to_user':msg_to_user,'resourceType':resourceType
    })
    return HttpResponse(t.render(c))

def resourceDetails(request,resourceSlug='',resourceType='tool-kit'):
    resource = ''
    msg_to_user = ''
    t = loader.get_template('resource_details.html')
    try:
        if resourceSlug:
            resource = Resource.objects.get(url4SEO=resourceSlug)
        else:
            resource = Resource.objects.all().filter(live=True).filter(resourceType = resourceType)[:1]
             
    except:
        msg_to_user = 'Selected project or project article is still being updated!'
        
    c = Context({
        'resource': resource, 'msg_to_user':msg_to_user,
    })
    return HttpResponse(t.render(c))

def publications(request,pubType='white-paper'):
    publication_list = []
    t = loader.get_template('publication_listing.html')
    msg_to_user = ''
    pageTitle = ''
    try:
        publication_list = Publication.objects.all().filter(live=True).filter(pubType=pubType)[:RECORDS_PER_PAGE]
        pageTitle = u"List of "+pubType+" publication"
    except:
        msg_to_user = "Publication section is being updated"
    c = Context({
        'publication_list': publication_list,'page_title':pageTitle,'msg_to_user':msg_to_user,'pubType':pubType
    })
    return HttpResponse(t.render(c))


def publicationDetails(request,pubSlug='',pubType='white-paper'):
    publication = ''
    msg_to_user = ''
    t = loader.get_template('publication_details.html')
    try:
        if pubSlug:
            publication = Publication.objects.get(url4SEO=pubSlug)
        else:
            publication = Publication.objects.all().filter(live=True).filter(pubType = pubType)[:1]
             
    except:
        msg_to_user = 'Selected publication is still being updated!'
        
    c = Context({
        'publication': publication, 'msg_to_user':msg_to_user,
    })
    return HttpResponse(t.render(c))


