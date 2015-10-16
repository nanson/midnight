from main.models import *
from django.contrib import admin
from midnight.base_models import BaseAdmin, BaseAdminTree


class PageAdmin(BaseAdmin):

    fieldsets = [
        (None, {'fields':  ['title', 'slug', 'active', 'text']}),
        ('SEO', {'fields':  ['metatitle', 'keywords', 'description']}),
    ]

    list_display = ('title', 'slug', 'active')


admin.site.register(Page, PageAdmin)


class IncludeAreaAdmin(BaseAdmin):

    fields = ['title', 'slug', 'active', 'text']

    list_display = ('title', 'slug', 'active')

    pass

admin.site.register(IncludeArea, IncludeAreaAdmin)


class MenuAdmin(BaseAdminTree):

    fields = ['parent', 'active', 'title', 'link', 'slug', 'target', 'cls', 'sort']

    list_display = ('title', 'link', 'active', 'sort')

    pass

admin.site.register(Menu, MenuAdmin)


class PhotoInline(admin.TabularInline):

    exclude = ['author']

    model = Photo

    extra = 3


class PhotoAlbumAdmin(BaseAdmin):

    fields = ['title', 'slug', 'active', 'text']

    list_display = ('title', 'slug', 'active')

    inlines = [PhotoInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.author = request.user
            instance.save()
        formset.save_m2m()


admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
