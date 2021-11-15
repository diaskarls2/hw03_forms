from django.core.paginator import Paginator
from django.conf import settings


def get_paginator_context(queryset, page_number, page_size=settings.PAGE_SIZE):
    paginator = Paginator(queryset, page_size)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': paginator.get_page(page_number),
    }
