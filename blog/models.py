from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset().filter(status='published')

#get_queryset()是返回执行过的查询集（QuerySet）的方法。我们通过使用它来包含我们定制的过
#滤到完整的查询集（QuerySet）中。我们定义我们定制的管理器（manager）然后添加它到Post 模型
#（model）中。我们现在可以来执行它。例如，我们可以返回所有标题开头为Who的并且是已经发布的帖子:

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                                related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                                choices=STATUS_CHOICES,
                                default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                              self.publish.strftime('%m'),
                              self.publish.strftime('%d'),
                              self.slug])
    
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    


class Comment(models.Model):
    post = models.ForeignKey(Post,related_name = 'comments')
    name = models.CharField(max_length = 80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = True)

    class Meta():
        ordering = ('created',) 
    
    def __str__(self):
        return 'comment by {} on {}'.format(self.name,self.post)
    
#通过使用 comment.post就可以从一条评论来取到对应的帖子
#通过使用post.comments.all()来取回一个帖子所有的评论
    



















