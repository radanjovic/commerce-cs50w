from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories/books", views.books, name="books"),
    path("categories/fashion", views.fashion, name="fashion"),
    path("categories/home", views.home, name="home"),
    path("categories/tech", views.tech, name="tech"),
    path("categories/tools", views.tools, name="tools"),
    path("categories/other", views.other, name="other"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist")
]
