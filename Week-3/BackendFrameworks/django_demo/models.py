"""
Django Models Module.

This file defines the database structure for our Django demo using the Django Object-Relational Mapper (ORM).
Models are Python classes that inherit from `django.db.models.Model` and map directly to database tables.
"""

from django.db import models
from django.utils import timezone


class Author(models.Model):
    """
    Represents an Author of a book.
    
    Demonstrates:
    - Standard CharField and TextField.
    - Automatic auto-incrementing ID primary key (provided by default).
    - String representation method.
    """
    first_name = models.CharField(max_length=50, help_text="Author's first name")
    last_name = models.CharField(max_length=50, help_text="Author's last name")
    biography = models.TextField(blank=True, help_text="Brief biographical sketch")
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        Returns a human-readable representation of the Author.
        Django uses this in the admin panel and debug tools.
        """
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    """
    Represents a Book published by an Author.
    
    Demonstrates:
    - One-to-Many Relationship: Each Book has one Author, but an Author can have multiple Books.
    - Foreign Key configuration with onDelete rules.
    - Date field defaults.
    """
    title = models.CharField(max_length=150, help_text="Title of the book")
    summary = models.TextField(help_text="Short plot or topic summary")
    publish_date = models.DateField(default=timezone.now, help_text="Publication date")
    
    # One-to-Many relationship using ForeignKey.
    # on_delete=models.CASCADE ensures that if the Author is deleted, all their books are also deleted.
    # related_name allows backwards querying: author.books.all()
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name="books",
        help_text="The author of this book"
    )

    def __str__(self):
        """
        Returns the title of the book.
        """
        return self.title
