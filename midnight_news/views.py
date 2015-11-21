from django.shortcuts import render, get_object_or_404
from django.template import Template, Context
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from midnight_main.components import MetaSeo
from midnight_news.models import News, Section


def index(request, slug=None):

    section = None

    if slug is None:
        q = News.objects.published()
        meta = MetaSeo()
        meta.metatitle = _('News')
        crumbs = [{'label': _('News')}]
    else:
        section = Section.objects.get(slug=slug)

        if section is None:
            raise Http404('Section with slug "%s" not found' % slug)

        crumbs = section.get_breadcrumbs()

        meta = MetaSeo(section)

        q = News.objects.published().filter(sections__slug=slug)

    q = q.prefetch_related('sections').order_by('-date', '-id')

    models = q.all()

    pager = Paginator(models, getattr(settings, 'MIDNIGHT_NEWS_PAGE_SIZE', 20))

    page = request.GET.get('page')

    try:
        news = pager.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = pager.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = pager.page(pager.num_pages)

    return render(request, 'midnight_news/news/index.html', {'news': news, 'section': section, 'meta': meta, 'crumbs': crumbs})


def detail(request, section_slug, slug):

    item = get_object_or_404(News, slug=slug, active=True)

    section = get_object_or_404(Section, slug=section_slug, active=True)

    crumbs = section.get_breadcrumbs(True) + [{'label': item.title}]

    text = Template(item.text).render(Context())

    meta = MetaSeo(item)

    return render(request, 'midnight_news/news/detail.html', {'item': item, 'text': text, 'meta': meta, 'crumbs': crumbs})