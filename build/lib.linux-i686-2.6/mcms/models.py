from django.db import models
from tinymce import models as tinymce_models
from django.contrib.comments.moderation import CommentModerator, moderator
from thumbs import ImageWithThumbsField

########### All constants
NamePrefix =   (  (u'Mr', u'Mr'),
    (u'Ms', u'Ms'),
    (u'Dr', u'Dr'),
)

GenderChoices = ( (u'M', u'Male'),
                             (u'F', u'Female'),)
                             
##########

################################.
# Base content Type
class BaseContent(models.Model):
    """
    A base class for CMS content types.
    """
    
    title = models.CharField("Title/ Headline", max_length=100)
    summary = models.CharField("Byline/ Summary",blank=True, max_length=400)    
    url4SEO = models.SlugField("SEO friendly url, use only aplhabets and hyphen",max_length=60)
    createdOn = models.DateTimeField( auto_now_add=True)
    modifiedOn = models.DateTimeField(auto_now=True)
    listingOrder = models.PositiveSmallIntegerField("Listing order", default=0)
    panelColor = models.CharField("Panel color", max_length=8, blank = True)
    live = models.BooleanField("This is a active content",default=True)

    class Meta:
        abstract = True
        ordering = ['-listingOrder','-createdOn']
        

    


class Author(models.Model):
    """
    An author
    """
    prefix = models.CharField("Prefix",max_length=2,choices=NamePrefix)
    firstName = models.CharField("First name", max_length=100)
    lastName = models.CharField("Last name", max_length=100)
    gender = models.CharField("Gender", max_length=1,choices=GenderChoices)
    url4SEO = models.SlugField("SEO friendly url, use only aplhabets and hyphen",max_length=60)
    summary = models.CharField("summary",blank=True,max_length=200)
    profileText = models.TextField("Profile", blank=True,max_length=7500)
    image = ImageWithThumbsField(upload_to='%Y/%m/%d',blank=True,sizes=((90,120),(270,360),) )
    webURL = models.URLField("Web URL",verify_exists=False,blank=True,max_length="60")    
    createdOn = models.DateTimeField( auto_now_add=True)
    modifiedOn = models.DateTimeField(auto_now=True)
    

    def __unicode__(self):
        return u'%s. %s %s' % (self.prefix, self.firstName, self.lastName)
    
    
class BaseArticle(BaseContent):
    """
    A base article content type
    """
    
    body = tinymce_models.HTMLField("Text")
    
    image = ImageWithThumbsField(upload_to='%Y/%m/%d',blank=True,sizes=((120,120),(240,240),(400,400),) )
    imageCaption = models.CharField("Image caption", max_length=100,blank=True)
    
    attachmentTitle = models.CharField("Attachment file caption", max_length=100,blank=True)
    attachment = models.FileField(upload_to='%Y/%m/%d',blank=True)
        
    linkTitle = models.CharField("External Link heading", blank=True,max_length=100)
    linkSummary = models.CharField("External Link clickable text",blank=True, max_length=100)
    linkURL = models.URLField("External URL",verify_exists=False,blank=True,max_length="60")
    
    class Meta:
        abstract = True
        ordering = ['-listingOrder','-createdOn']
        
class Category(models.Model):
    """
    Content category
    """
    name = models.CharField("Category name", max_length=100)
    description = tinymce_models.HTMLField("Article text")
    icon = ImageWithThumbsField(upload_to='%Y/%m/%d',blank=True,sizes=((120,120),) )
    panelColor = models.CharField("Panel color", max_length=8, blank = True)
    
    def __unicode__(self):
        return u'%s' % (self.name)
        
class Team(models.Model):
    """
    Content category
    """
    name = models.CharField("Name", max_length=100)
    icon = ImageWithThumbsField(upload_to='%Y/%m/%d',blank=True,sizes=((120,120),) )
    description = tinymce_models.HTMLField("Summary")
    url4SEO = models.SlugField("SEO friendly url, use only aplhabets and hyphen",max_length=60)
    panelColor = models.CharField("Panel color", max_length=8, blank = True)
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
class Article(BaseArticle):
    """
    A simple article.
    """
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return u'%s' % (self.title)


class Event(BaseArticle):
    """
    A simple Event
    """
    startDate = models.DateTimeField()
    endDate = models.DateTimeField(blank=True)
    
    class Meta:
        ordering = ['-listingOrder','-startDate','title']


    def __unicode__(self):
        return u'%s' % (self.title)
    
    
class Project(BaseContent): 
    """
    A simple project
    """
    logo = ImageWithThumbsField(upload_to='%Y/%m/%d',blank=True,sizes=((120,120),) )
    attachment = models.FileField(upload_to='%Y/%m/%d',blank=True)
    attachmentTitle = models.CharField("Attachment caption", max_length=100,blank=True)
    team = models.ForeignKey(Team)
    
    manager = models.ManyToManyField(Author)
    


    def __unicode__(self):
        return u'%s' % (self.title)

class ProjectArticle(BaseArticle):
    """
    A simple Project article.
    """
    project = models.ForeignKey(Project)
    
    
    def __unicode__(self):
        return u'%s - %s' % (self.project, self.title)
    



class Publication(BaseArticle):
    """
    A simple Publication.
    """
    
    PUBLICATION_TYPE = (
        (u'white-paper', u'White paper'),
        (u'booklet', u'Booklet'),
        (u'hand-book-guide', u'Hand book/ Guide'),
        (u'research-paper', u'Research paper'),
        (u'journal', u'Journal'),
    )
    authors = models.ManyToManyField(Author)
    pubType = models.CharField("Publication Type",max_length=20, choices=PUBLICATION_TYPE)
    publisher = models.CharField("Publisher", max_length=100)
    price = models.CharField("Publication cost",blank=True, max_length=20)    
    buyURL = models.URLField("Link for buying publication",blank=True,verify_exists=False, max_length=200)
    


    def __unicode__(self):
        return u'%s - %s' % (self.pubType, self.title)
        


class Resource(BaseArticle):
    """
    A simple Resource toolkit.
    """
    RESOURCE_TYPE = (
        (u'tool-Kit', u'Tool-kit'),
        (u'manual', u'Manual'),
        (u'online', u'Online'),
        (u'generic', u'Generic'),
    )
    resourceType = models.CharField(max_length=20, choices=RESOURCE_TYPE)
    
    


    def __unicode__(self):
        return u'%s' % (self.title)
        
        
class ProjectArticleModerator(CommentModerator):
    auto_close_field = 'createdOn'
    close_after = 15
    enable_field = 'enable_comments'
    

class PublicationModerator(CommentModerator):
    auto_close_field = 'createdOn'
    close_after = 30
    enable_field = 'enable_comments'

moderator.register(ProjectArticle, ProjectArticleModerator)
moderator.register(Publication, PublicationModerator)



