from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='snippets-add'),
    path('snippets/list', views.snippets_page, name='snippets-list'),
    path('snippets/<int:snippet_id>',
         views.snippets_detail, name='snippets-detail'),
    path('snippets/<int:snippet_id>/delete',
         views.snippets_delete, name='snippets-delete'),
    path('snippets/<int:snippet_id>/edit',
         views.snippets_edit, name='snippets-edit'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
