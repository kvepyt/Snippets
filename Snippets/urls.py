from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from MainApp import views

urlpatterns = [
    path("", views.index_page, name="home"),
    path("admin/", admin.site.urls),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.create_user, name="register"),
    path("comment/add", views.comment_add, name="comment-add"),
    path(
        "snippets/",
        include(
            [
                path("add", views.add_snippet_page, name="snippets-add"),
                path("list", views.snippets_page, name="snippets-list"),
                path("my", views.my_snippets, name="my-snippets"),
                path(
                    "<int:snippet_id>/",
                    include(
                        [
                            path("", views.snippet_detail, name="snippet-detail"),
                            path(
                                "delete",
                                views.snippet_delete,
                                name="snippet-delete",
                            ),
                            path("edit", views.snippet_edit, name="snippet-edit"),
                        ]
                    ),
                ),
            ]
        ),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
