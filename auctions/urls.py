from django.urls import path

from . import views
        
app_name = "auction"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_view, name="create_view"),
    path("listing/<int:list_id>",views.listing,name="listing"),
    path("add-comment/<int:item_id>",views.add_comment, name="add_comment"),
    path("add-watchlist/<int:item_id>",views.add_watchlist,name="add_watchlist"),
    path("remove-watchlist/<int:item_id>", views.remove_watchlist,name ="remove_watchlist"),
    path("close-listing/<item_id>",views.close_listing, name="close_listing"),
    path("watchlists",views.watchlist_view,name="watchlist_view"),
    path("categories",views.categories,name="categories"),
    path("category-view/<int:list_id>",views.category_view, name="category_view"),
]
