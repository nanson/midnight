from django.contrib import admin
from django.forms import ModelForm

from midnight_main.admin import BaseAdmin, BaseAdminTree
from midnight_news.models import Section, News, NewsComment
from midnight_main.widgets import AdminImageWidget
from django.utils.translation import ugettext_lazy as _


class SectionAdmin(BaseAdminTree):

    fieldsets = [
        (None, {'fields':  ['parent', 'active', 'title', 'slug', 'sort']}),
        ('SEO', {'fields':  ['metatitle', 'keywords', 'description']}),
    ]

    prepopulated_fields = {"slug": ("title",)}

    list_display = ('title', 'id', 'slug', 'active', 'sort', 'public_link')

    list_editable = ('sort', )

    search_fields = ('id', 'title', 'slug',)

    def public_link(self, obj):
        url = obj.get_absolute_url()
        return '<a target="_blank" href="%s">%s</a>' % (url, url)

    public_link.allow_tags = True

    public_link.short_description = 'Url'

admin.site.register(Section, SectionAdmin)


class NewsForm(ModelForm):

    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'image': AdminImageWidget,
        }


class NewsAdmin(BaseAdmin):

    fieldsets = [
        (None, {'fields':  ['active', 'title', 'slug', 'date', 'sections', 'image', 'annotation', 'text', 'comments']}),
        ('SEO', {'fields':  ['metatitle', 'keywords', 'description']}),
    ]

    prepopulated_fields = {"slug": ("title",)}

    list_display = ('title', 'id', 'slug', 'active', 'date', 'public_link')

    list_filter = ('sections', 'active')

    search_fields = ('id', 'title', 'slug',)

    form = NewsForm

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('sections')

    def public_link(self, obj):
        url = obj.get_absolute_url()
        return '<a target="_blank" href="%s">%s</a>' % (url, url)

    public_link.allow_tags = True

    public_link.short_description = 'Url'

admin.site.register(News, NewsAdmin)


class NewsCommentAdmin(BaseAdminTree):

    exclude = ('author',)

    list_display = ('id', 'username', 'email', 'text', 'news_obj',)

    search_fields = ('id', 'username', 'email',)

    def news_obj(self, comment):
        return '<a href="%s">%s</a>' % (comment.obj.get_absolute_url(), comment.obj.title)

    news_obj.allow_tags = True
    news_obj.short_description = _('News')

admin.site.register(NewsComment, NewsCommentAdmin)
