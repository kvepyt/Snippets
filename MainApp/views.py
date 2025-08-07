from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    # Создаем пустую форму при запросе GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    # Получаем данные из формы и на их основе создаем новый сниппет, сохраняя его в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets-list")  # URL для списка сниппитов
        return render(request, 'pages/add_snippet.html', context={"form": form})
    return HttpResponseNotAllowed(["POST"], "You must make POST request to add snippet.")


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
    }
    return render(request, 'pages/view_snippets.html', context)


def snippets_detail(request, snippet_id: int):
    """ Get snippet by id from db."""
    context = {'pagename': 'Просмотр Сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return render(request, "errors.html", context | {"error": f"Snippet with id={snippet_id} not found"})
    else:
        context['snippet'] = snippet

        return render(request, "pages/snippets_detail.html", context)


def snippet_delete(request, snippet_id: int):
    """ Delete snippet by id from db."""

    if request.method == "GET" or request.method == "POST":
        # Найти snippet no snippet_id или вернуть ошибку 404
        snippet = get_object_or_404(Snippet, id=snippet_id)
        snippet.delete()  # Удаляем сниппет из базы
    return redirect("snippets-list")


def snippet_edit(request, snippet_id: int):
    """ Edit snippet by id from db."""
    pass


"""
    if request.method == "GET" or request.method == "POST":
        # Найти snippet no snippet_id или вернуть ошибку 404
        snippet = get_object_or_404(Snippet, id=snippet_id)
        snippet.edit()  # Удаляем сниппет из базы
    return redirect("snippets-list")
"""
