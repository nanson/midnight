from django import template
from main.models import Menu, PhotoAlbum, IncludeArea
from django.core.urlresolvers import reverse
import uuid
from midnight.tools import get_class_from_string

register = template.Library()


def show_menu(slug, **kwargs):

    try:
        menu = Menu.objects.published().get(slug=slug)
        return {'menu': menu, 'data': kwargs}
    except Menu.DoesNotExist:
        return None

register.inclusion_tag(file_name='main/tags/show_menu.html', name='show_menu')(show_menu)


def show_gallery(slug, size="100x100", crop="center", **kwargs):

    try:
        album = PhotoAlbum.objects.published().get(slug=slug)
        photos = album.photo_set.published().order_by('sort').all()
        return {'album': album, 'photos': photos, 'size': size, 'crop': crop, 'data': kwargs}
    except PhotoAlbum.DoesNotExist:
        return None

register.inclusion_tag(file_name='main/tags/show_gallery.html', name='show_gallery')(show_gallery)


@register.simple_tag()
def show_area(slug):

    try:
        area = IncludeArea.objects.published().get(slug=slug)
        return area.text
    except IncludeArea.DoesNotExist:
        return ""


def ajax_form(cls_name, view_name, modal=False, tag_id=None):
    if tag_id is None:
        tag_id = uuid.uuid4().hex[:6].lower()
    form = get_class_from_string(cls_name)()
    url = reverse(view_name)
    return {'form': form, 'url': url, 'modal': modal, 'id': tag_id}

register.inclusion_tag(file_name='main/tags/ajax_form.html', name='ajax_form')(ajax_form)


def user_info(context):
    request = context['request']
    return {'user': request.user}

register.inclusion_tag(file_name='main/tags/user_info.html', takes_context=True, name='user_info')(user_info)
