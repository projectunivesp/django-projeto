from django.shortcuts import render, get_list_or_404,get_object_or_404
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator
from utils.pagination import make_pagination
from recipes.models import Recipe

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 3))


def home(request):
    recipes = Recipe.objects.filter(
        is_published = True
        ).order_by('-id')
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })

def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id = category_id,
            is_published = True
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes.first().category.name} - Category |',
    })

def recipe(request, id):
    recipe = get_object_or_404 (Recipe,
            id = id,
            is_published = True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })

def search(request):
    search_term = request.GET.get('search', '').strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) |
        Q(description__icontains = search_term),
    )
    recipes = recipes.order_by('-id')
    recipes = recipes.filter(is_published = True)

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    
    return render(request, 'recipes/pages/search.html',
        {'page_title': f'Search for "{search_term}"',
         'search_term': search_term,
         'recipes': page_obj,
         'pagination_range': pagination_range,
         'additional_url_query': f'&q={search_term}'
         
    })