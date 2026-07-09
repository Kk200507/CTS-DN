"""
Django URLs Module.

This file maps URL paths to the views that handle them.
It demonstrates static paths, dynamic integer paths, class-based view routing, and path naming.
"""

from django.urls import path
from . import views

# app_name enables namespaces when referencing URLs in templates (e.g., 'library:book-detail')
app_name = "library"

urlpatterns = [
    # 1. Static URL Path
    # Maps 'domain.com/library/authors/' to the function-based view 'author_list_view'
    path("authors/", views.author_list_view, name="author-list"),

    # 2. Dynamic URL Path with integer parameter
    # Matches URLs like 'domain.com/library/books/12/' and passes 'book_id=12' to the view
    path("books/<int:book_id>/", views.BookDetailView.as_view(), name="book-detail"),

    # 3. Static Home/Welcome Page View (Class-Based View routing)
    # CBVs must call the `.as_view()` method in url patterns
    path("welcome/", views.WelcomePageView.as_view(), name="welcome"),
]
