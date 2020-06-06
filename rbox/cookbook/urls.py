
from django.urls import path
from cookbook import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('author/<int:id>/', views.author_detail, name='author'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe'),
    path('recipeadd/', views.recipeadd, name='recipeadd'),
    path('authoradd/', views.authoradd, name='authoradd'),
    path('login/', views.loginview, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('editform/<int:id>', views.recipeedit, name="edit"),
    path('favorite/<int:id>', views.addfavorite, name='fav')
]
