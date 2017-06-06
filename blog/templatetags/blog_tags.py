from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


"""
simple_tag：处理数据并返回一个字符串（string）
inclusion_tag：处理数据并返回一个渲染过的模板（template）
assignment_tag：处理数据并在上下文（context）中设置一个变量（variable）
"""
register = template.Library()

@register.simple_tag()

def total_posts():
    return Post.published.count()


@register.simple_tag()
def sharp():
    a = Post.objects.all()[0]
    b = a.tags.values_list('name',flat = True)
    return b


@register.inclusion_tag('blog/post/latest_posts.html')

def show_latest_posts(count = 5):
    latest_posts = Post.published.order_by('publish')[:count]
    return {'latest_posts':latest_posts}


@register.assignment_tag()

def get_most_commented_posts(count = 5):
    return Post.published.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]

@register.filter(name = 'markdown')

def markdown_format(text):
    return mark_safe(markdown.markdown(text))


