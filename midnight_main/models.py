# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ForeignKey
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User, UserManager, AbstractUser
from django.conf import settings
from ckeditor.fields import RichTextField


class AppUser(AbstractUser):
    """
    Пользователь приложения
    """

    phone = models.CharField(blank=True, max_length=10, verbose_name=_('Phone'))

    image = ImageField(upload_to='users', verbose_name=_('Image'), blank=True)

    objects = UserManager()


class Base(models.Model):
    """
    Базовая модель
    """

    active = models.BooleanField(default=True, verbose_name=_('Active'))

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), null=True, blank=True, related_name='+')

    created_at = models.DateTimeField(auto_now_add=True)

    update_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


class BaseTree(MPTTModel):
    """
    Базовая древовидная модель
    """

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, verbose_name=_('Parent'))

    active = models.BooleanField(default=True, verbose_name=_('Active'))

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), null=True, blank=True, related_name='+')

    created_at = models.DateTimeField(auto_now_add=True)

    update_at = models.DateTimeField(auto_now=True)

    def get_path(self):
        if hasattr(self, 'slug'):
            return '/'.join([item.slug for item in self.get_ancestors(include_self=True)])
        else:
            return None

    def has_childs(self):
        count = self.children.count()
        return count > 0

    class Meta:
        abstract = True


class BaseComment(BaseTree):
    """
    Базовая модель для комментариев
    """

    username = models.CharField(max_length=255, verbose_name=_('Username'))

    email = models.EmailField(max_length=255, blank=True, verbose_name=_('Email'))

    text = models.TextField(verbose_name=_('Comment'))

    def __str__(self):
        return self.username

    class MPTTMeta:

        order_insertion_by = ['created_at']

    class Meta:

        abstract = True


class BreadCrumbsMixin(object):
    """
    Примись для формирования хлебных крошек древовидных объектов
    """
    def get_breadcrumbs(self, self_url=False):
        crumbs = [{'label': item.title, 'url': item.get_absolute_url()} for item in self.get_ancestors()]
        if self_url:
            crumbs += [{'label': self.title, 'url': self.get_absolute_url()}]
        else:
            crumbs += [{'label': self.title}]
        return crumbs


class Page(BreadCrumbsMixin, BaseTree):
    """
    Модель текстовых страниц
    """

    MAIN_SLUG = "main"

    PAGE_TPL_CHOICES = (
        ('midnight_main/pages/pages.html', _('Simple page')),
        ('midnight_main/pages/guestbook.html', _('Guestbook')),
    )

    title = models.CharField(max_length=500, verbose_name=_('Title'))

    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))

    text = RichTextField(blank=True, verbose_name=_('Text'))

    sort = models.IntegerField(default=500, verbose_name=_('Sort'))

    comments = models.BooleanField(default=False, verbose_name=_('Comments'))

    tpl = models.CharField(max_length=255, default=PAGE_TPL_CHOICES[0][0], verbose_name=_('Template'), choices=getattr(settings, 'MIDNIGHT_MAIN_PAGE_TPL_CHOICES', PAGE_TPL_CHOICES))

    metatitle = models.CharField(max_length=2000, blank=True, verbose_name=_('MetaTitle'))

    keywords = models.CharField(max_length=2000, blank=True, verbose_name=_('Keywords'))

    description = models.CharField(max_length=2000, blank=True, verbose_name=_('Description'))

    def get_absolute_url(self):
        return reverse('midnight_main:page_detail', kwargs={'path': self.get_path()})

    def __str__(self):
        return self.title

    class MPTTMeta:

        order_insertion_by = ['sort']

    class Meta:

        verbose_name = _('Page')

        verbose_name_plural = _('Pages')


class IncludeArea(Base):
    """
    Модель текстовых включаемых областей
    """

    title = models.CharField(max_length=500, verbose_name=_('Title'))

    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))

    text = RichTextField(blank=True, verbose_name=_('Text'))

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = _('IncludeArea')

        verbose_name_plural = _('IncludeAreas')


class Menu(BaseTree):
    """
    Модель меню
    """

    TARGET_CHOICES = (
        ('_self', _('Self window')),
        ('_blank', _('Blank window')),
    )

    is_current = False

    title = models.CharField(max_length=255, verbose_name=_('Title'))

    link = models.CharField(max_length=2000, blank=True, verbose_name=_('Link'))

    slug = models.SlugField(max_length=255, blank=True, verbose_name=_('Slug'))

    target = models.CharField(max_length=32, blank=True, verbose_name=_('Target'), choices=TARGET_CHOICES)

    cls = models.CharField(max_length=255, blank=True, verbose_name=_('Cls'))

    sort = models.IntegerField(default=500, verbose_name=_('Sort'))

    def get_absolute_url(self):
        return self.link

    def __str__(self):
        return self.title

    class MPTTMeta:

        order_insertion_by = ['sort']

    class Meta:

        verbose_name = _('Menu')

        verbose_name_plural = _('Menu')


class PhotoAlbum(Base):
    """
    Модель фото альбома
    """

    title = models.CharField(max_length=500, verbose_name=_('Title'))

    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))

    text = RichTextField(blank=True, verbose_name=_('Text'))

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = _('PhotoAlbum')

        verbose_name_plural = _('PhotoAlbums')


class Photo(Base):
    """
    Модель фотографии
    """

    title = models.CharField(max_length=500, verbose_name=_('Title'))

    image = ImageField(upload_to='photos', verbose_name=_('Image'))

    album = models.ForeignKey(PhotoAlbum, verbose_name=_('PhotoAlbum'))

    sort = models.IntegerField(default=500, verbose_name=_('Sort'))

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = _('Photo')

        verbose_name_plural = _('Photos')


class PageComment(BaseComment):
    """
    Модель комментария к текстовой странице
    """

    obj = ForeignKey(Page)

    class Meta:

        verbose_name = _('PageComment')

        verbose_name_plural = _('PageComments')
