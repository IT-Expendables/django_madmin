from django.db import models
from django.conf import settings


class Article(models.Model):
    '''文章'''
    STATUS_NONE = 0
    STATUS_ONLINE = 1
    STATUS_OFFLINE = 2
    STATUS_TOP = 3
    STATUS_CHOICES = (
        (STATUS_NONE, '草稿'),
        (STATUS_OFFLINE, '已下线'),
        (STATUS_ONLINE, '已发布'),
        (STATUS_TOP, '置顶'),
    )

    title = models.CharField('标题', max_length=1024)
    summary = models.CharField('摘要', max_length=1024, blank=True, null=True)
    author = models.CharField('作者', max_length=64, blank=True, null=True)
    post_time = models.DateTimeField('发布时间')
    content = models.TextField('内容')
    cover_urls = models.CharField('封面', max_length=2048, blank=True, null=True)

    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=STATUS_NONE)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, verbose_name='创建者')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = '文章'


class Episode(models.Model):
    """单集"""

    article = models.ForeignKey(Article, models.Case, verbose_name='剧集')

    video = models.CharField("视频", max_length=1000)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = '单集'
        verbose_name_plural = '单集列表'
