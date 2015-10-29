from django.forms import ModelForm
from main.models import *
from django.contrib import admin
from midnight.base_models import BaseAdmin, BaseAdminTree
from midnight.widgets import AdminImageWidget
from django.core.urlresolvers import reverse


class PageAdmin(BaseAdmin):

    fieldsets = [
        (None, {'fields':  ['title', 'slug', 'active', 'text']}),
        ('SEO', {'fields':  ['metatitle', 'keywords', 'description']}),
    ]

    list_display = ('title', 'id', 'slug', 'active', 'public_link')

    list_filter = ('active',)

    search_fields = ('id', 'title', 'slug',)

    def public_link(self, obj):
        url=reverse('main:page_detail', args=[obj.slug])
        return '<a target="_blank" href="%s">%s</a>' % (url, url)

    public_link.allow_tags = True

    public_link.short_description = 'Url'

admin.site.register(Page, PageAdmin)


class IncludeAreaAdmin(BaseAdmin):

    fields = ['title', 'slug', 'active', 'text']

    list_display = ('title', 'slug', 'active')

    list_filter = ('active',)

    search_fields = ('id', 'title', 'slug',)

admin.site.register(IncludeArea, IncludeAreaAdmin)


class MenuAdmin(BaseAdminTree):

    fields = ['parent', 'active', 'title', 'link', 'slug', 'target', 'cls', 'sort']

    list_display = ('title', 'id', 'link', 'active', 'sort')

    list_filter = ('active',)

    search_fields = ('id', 'title', 'slug',)

    list_editable = ('sort',)

admin.site.register(Menu, MenuAdmin)


class PhotoForm(ModelForm):

    class Meta:
        model = Photo
        fields = '__all__'
        widgets = {
            'image': AdminImageWidget,
        }


class PhotoInline(admin.TabularInline):

    exclude = ['author']

    model = Photo

    extra = 3

    form = PhotoForm

    ordering = ('sort',)


class PhotoAlbumAdmin(BaseAdmin):

    fields = ['title', 'slug', 'active', 'text']

    list_display = ('title', 'id', 'slug', 'active')

    inlines = [PhotoInline]

    list_filter = ('active',)

    search_fields = ('id', 'title', 'slug',)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.author = request.user
            instance.save()
        formset.save_m2m()


admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
