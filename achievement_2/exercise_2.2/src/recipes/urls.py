from django.urls import path
from .views import RecipeListView, RecipeDetailView  
from .views import home

urlpatterns = [
   path('', home, name='recipes_home'),
   path('recipes/', RecipeListView.as_view(), name='recipe-list'),
   path('list/<pk>', RecipeDetailView.as_view(), name='detail'),
]
