from django.shortcuts import render, reverse, HttpResponseRedirect
from cookbook.models import Recipe, Author, Favorite
from cookbook.forms import RecipeAddForm, AuthorAddForm, LoginForm, RecipeEditForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse('homepage')))
    form = LoginForm()
    html = 'addform.html'
    return render(request, html, {'form': form})


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def index(request):
    user = request.user
    try:
        profile = Author.objects.get(user=user)
    except:
        profile = None
    data = Recipe.objects.all()
    return render(request, 'index.html', {'data': data, 'profile': profile})


def author_detail(request, id):
    person = Author.objects.get(id=id)
    user = User.objects.get(id=person.user.id)
    recipe = Recipe.objects.filter(author=person)
    fav = Favorite.objects.filter(user=user)
    print(len(fav))
    return render(request, 'author.html', {'person': person, 'recipe': recipe, 'fav': fav})


def recipe_detail(request, id):
    recipe = Recipe.objects.get(id=id)

    if request.user.is_authenticated:
        try:
            user = User.objects.get(id=request.user.id)
            fav = Favorite.objects.get(recipe=recipe, user=user)
            print("favorite")
        except:
            print("not favorite")
            fav = None
    else:
        fav = None

    return render(request, 'recipe.html', {'recipe': recipe, 'fav': fav})


@login_required
def recipeadd(request):
    html = 'addform.html'

    if request.method == 'POST':
        form = RecipeAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                description=data['description'],
                req_time=data['req_time'],
                instructions=data['instructions'],
                author=data['author']
            )
            return HttpResponseRedirect('/')

    form = RecipeAddForm()
    return render(request, html, {'form': form})


@login_required
def recipeedit(request, id):
    html = 'editform.html'

    recipe = Recipe.objects.get(id=id)
    if request.method == "POST":
        form = RecipeEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data["title"]
            recipe.description = data["description"]
            recipe.req_time = data["req_time"]
            recipe.instructions = data["instructions"]
            recipe.author = data["author"]

            recipe.save()
            url = ('/recipe/{}').format(id)
            return HttpResponseRedirect(url)

    form = RecipeEditForm(initial={
        "title": recipe.title,
        "description": recipe.description,
        "req_time": recipe.req_time,
        "instructions": recipe.instructions,
        "author": recipe.author,
    })
    return render(request, html, {"form": form, "recipe": recipe})


@login_required
def authoradd(request):
    html = 'addform.html'

    # if request.user.is_staff:
    #     if request.method == 'POST':
    #         form = AuthorAddForm(request.POST)
    #         form.save()
    #         return HttpResponseRedirect('/')

    # form = AuthorAddForm()
    if request.user.is_staff:
        if request.method == "POST":
            form = AuthorAddForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = User.objects.create_user(
                    username=data["username"],
                    password=data['password']
                )
                Author.objects.create(
                    name=data['name'],
                    bio=data['bio'],
                    user=user
                )
                return HttpResponseRedirect('/')
        form = AuthorAddForm
        return render(request, html, {'form': form})
    else:
        print("user is not staff")
    return render(request, html, {'form': form})


@login_required
def addfavorite(request, id):
    user = request.user
    recipe = Recipe.objects.get(id=id)

    Favorite.objects.get_or_create(
        user=user,
        recipe=recipe,
        star=True
    )

    print(len(Favorite.objects.all()))

    url = ('/recipe/{}').format(id)
    return HttpResponseRedirect(url)
