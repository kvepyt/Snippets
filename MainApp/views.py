from django.http import Http404, HttpResponseNotAllowed
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import CommentForm, SnippetForm, UserRegistrationForm
from MainApp.models import Snippet


def index_page(request):
    context = {"pagename": "PythonBin"}
    return render(request, "pages/index.html", context)


@login_required
def add_snippet_page(request):
    # Создаем пустую форму при запросе GET
    if request.method == "GET":
        form = SnippetForm()
        context = {"pagename": "Добавление нового сниппета", "form": form}
        return render(request, "pages/add_snippet.html", context)
    # Получаем данные из формы и на их основе создаем новый сниппет, сохраняя его в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)  # получаем экземпляр класса Snippet
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets-list")  # URL для списка сниппитов
        return render(request, "pages/add_snippet.html", context={"form": form})
    return HttpResponseNotAllowed(
        ["POST"], "You must make POST request to add snippet."
    )


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {
        "pagename": "Просмотр сниппетов",
        "snippets": snippets,
    }
    return render(request, "pages/view_snippets.html", context)


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {"pagename": "Просмотр моих сниппетов", "snippets": snippets}
    return render(request, "pages/view_snippets.html", context)


def snippet_detail(request, snippet_id: int):
    """Get snippet by id from db."""
    context = {"pagename": "Просмотр Сниппета"}
    current_user = request.user

    try:
        snippet = Snippet.objects.get(id=snippet_id)
        snip_user = snippet.user
    except ObjectDoesNotExist:
        return render(
            request,
            "errors.html",
            context | {"error": f"Snippet with id={snippet_id} not found"},
        )
    else:
        if (not snippet.public) and (snip_user != current_user):
            # and snippet. == request.user: and snippet.user == request.user
            return render(
                request,
                "errors.html",
                context
                | {
                    "error": f"Snippet  with id={snippet_id} is not available!!! Your User ({current_user}) has no rights to Private Snippet of {snip_user}!  "
                },
            )
        else:
            context["snippet"] = snippet
            context["comment_form"] = CommentForm()
            return render(request, "pages/snippet_detail.html", context)


def snippet_delete(request, snippet_id: int):
    """Delete snippet by id from db."""

    if request.method == "GET" or request.method == "POST":
        # Найти snippet no snippet_id или вернуть ошибку 404
        snippet = get_object_or_404(
            Snippet.objects.filter(user=request.user), id=snippet_id
        )
        snippet.delete()  # Удаляем сниппет из базы
    return redirect("snippets-list")


def snippet_edit(request, snippet_id: int):
    """Edit snippet by id from db."""
    context = {"pagename": "Изменение Сниппета"}
    snippet = get_object_or_404(
        Snippet.objects.filter(user=request.user), id=snippet_id
    )
    # Создаем форму на основе данных снипета при запросе GET
    if request.method == "GET":
        form = SnippetForm(instance=snippet)
        return render(request, "pages/add_snippet.html", context | {"form": form})
    # Получаем данные из формы и на их основе обновляем сниппет, сохраняя его в БД
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.public = data_form.get("public", False)
        snippet.save()
        return redirect("snippets-list")  # URL для списка сниппетов


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #        print("username =", username)
        #        print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                "pagename": "PythonBin",
                "errors": ["Wrong username or password"],
            }
            return render(request, "pages/index.html", context)
    return redirect("home")


def logout(request):
    auth.logout(request)
    return redirect(to="home")


def create_user(request):
    context = {"pagename": "Регистрация нового пользователя"}
    # Создаем пустую форму при запросе GET
    if request.method == "GET":
        form = UserRegistrationForm()
    # Получаем данные из формыи и на их основе создаем нового пользователя, сохраняя его в БД
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")  # URL для списка сниппитов
    context["form"] = form
    return render(request, "pages/registration.html", context)


def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
        # return redirect(f"/snippets/{snippet_id}")
        return redirect("snippet-detail", snippet_id=snippet.id)
    raise Http404
