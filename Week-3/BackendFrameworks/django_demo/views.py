"""
Django Views Module.

This file handles HTTP requests and returns HTTP responses.
It includes examples of both:
1. Function-Based Views (FBVs) - Simple and explicit.
2. Class-Based Views (CBVs) - Modular, reusable, and built-in features.
"""

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from .models import Author, Book


# ==========================================
# 1. Function-Based View (FBV) Example
# ==========================================

def author_list_view(request):
    """
    Function-Based View to list all authors.
    
    Demonstrates:
    - Querying the database using Django ORM.
    - Manually constructing a simple HTML string.
    - Returning a direct HttpResponse instead of rendering a file.
    """
    # Fetch all Author records from the database
    authors = Author.objects.all()
    
    # Check if request query param asks for plain text output
    output_format = request.GET.get('format', 'html')
    
    if output_format == 'txt':
        content = "\n".join([f"{a.first_name} {a.last_name}" for a in authors])
        return HttpResponse(content, content_type="text/plain")
        
    # Constructing inline HTML (for simple demonstration)
    html = "<h1>Authors Directory</h1><ul>"
    for author in authors:
        html += f"<li>{author.first_name} {author.last_name}</li>"
    html += "</ul>"
    
    return HttpResponse(html)


# ==========================================
# 2. Class-Based View (CBV) Example
# ==========================================

class BookDetailView(View):
    """
    Class-Based View to display details of a specific book.
    
    Demonstrates:
    - Handling HTTP GET requests inside an object-oriented class structure.
    - Fetching objects safely (returns 404 if not found).
    - Rendering a template file ('book_detail.html') and passing database context.
    """
    
    def get(self, request, book_id):
        """
        Handles the HTTP GET request.
        """
        # Retrieve the book by id or return 404 error if not exists
        book = get_object_or_404(Book, pk=book_id)
        
        # Define template context payload
        context = {
            "book": book,
            "author": book.author,
            "title": f"Book Details: {book.title}"
        }
        
        # Renders the template 'book_detail.html' with the context data and returns HttpResponse
        return render(request, "library/book_detail.html", context)


class WelcomePageView(TemplateView):
    """
    Simple CBV using Django's built-in TemplateView.
    
    Requires less boilerplate when views only render static or semi-static template pages.
    """
    template_name = "library/welcome.html"

    def get_context_data(self, **kwargs):
        """
        Inject custom context data into the page.
        """
        context = super().get_context_data(**kwargs)
        context["message"] = "Welcome to the Django MVT Demo App!"
        return context
