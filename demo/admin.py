from django.contrib import admin
from django.utils.html import format_html_join
from .models import Article


def online(self, request, queryset):
    qs = queryset.filter(status__in=[Article.STATUS_NONE, Article.STATUS_OFFLINE])
    count = qs.update(status=Article.STATUS_ONLINE)
    self.message_user(request, '已发布{}篇文章'.format(count))


def offline(self, request, queryset):
    qs = queryset.filter(status__in=[Article.STATUS_ONLINE, Article.STATUS_TOP])
    count = qs.update(status=Article.STATUS_OFFLINE)
    self.message_user(request, '已下线{}篇文章'.format(count))


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'post_time', 'creator', '_operate')
    list_display_links = ('title', )
    list_filter = ('status', )
    list_per_page = 30
    readonly_fields = ('creator', 'created_time')
    search_fields = ('title', )
    online.short_description = "发布"
    offline.short_description = "下线"
    actions = (online, offline)

    def _operate(self, obj):
        datas = []
        offline = obj.status in [Article.STATUS_NONE, Article.STATUS_OFFLINE]
        datas.append(('online' if offline else 'offline', obj.id, '发布' if offline else '下线', ))
        top = obj.status == Article.STATUS_TOP
        datas.append(('cancel_top' if top else 'top', obj.id, '取消置顶' if top else '置顶', ))
        return format_html_join(
            ' | ',
            '<a href="javascript:void(0);" class="mix-list-action" data-mixact="{}", data-id={}>{}</a>',
            datas
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        print(request.resolver_match.url_name)
        return super().changelist_view(request, extra_context)
