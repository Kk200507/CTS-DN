"""
Django Admin Customization Module.

This file registers models with Django's built-in Admin panel and customizes
how they are displayed, searched, and edited in the web interface.
"""

from django.contrib import admin
from .models import Author, Book


# ==================================================
# 1. Register model with default configuration
# ==================================================
# admin.site.register(Author)  # Basic registration without any custom UI panels.


# ==================================================
# 2. Register model with customized ModelAdmin
# ==================================================

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Custom Admin view for the Author model.
    """
    # Columns shown in the author list view
    list_display = ("first_name", "last_name", "date_of_birth")
    
    # Enable search by names in search box
    search_fields = ("first_name", "last_name")
    
    # Filter list options by Date of Birth on the sidebar
    list_filter = ("date_of_birth",)
    
    # Fields to group in the author creation/edit form
    fieldsets = (
        ("Personal Information", {
            "fields": ("first_name", "last_name", "date_of_birth")
        }),
        ("Biography & Notes", {
            "fields": ("biography",),
            "classes": ("collapse",),  # Collapses section by default
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Custom Admin view for the Book model.
    """
    # Display details and foreign key relationships in list table
    list_display = ("title", "author", "publish_date")
    
    # Search by book title and the related author name (using double underscores '__')
    search_fields = ("title", "author__first_name", "author__last_name")
    
    # Enable filter sidebar by publication date and author association
    list_filter = ("publish_date", "author")
    
    # Order books in list by publication date descending
    ordering = ("-publish_date",)
    
    # Auto-complete field to optimize choosing author from dropdown if DB has millions of records
    raw_id_fields = ("author",)
