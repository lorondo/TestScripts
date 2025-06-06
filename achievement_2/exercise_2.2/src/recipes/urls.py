from django.urls import path
from .views import RecipeListView, RecipeDetailView  
from .views import home
from . import views

urlpatterns = [
   path('', home, name='recipes_home'),
   path('recipes/', RecipeListView.as_view(), name='recipe_list'),
   path('list/<pk>', RecipeDetailView.as_view(), name='detail'),
   path('search/', views.ingredient_search, name='ingredient_search'),
]
