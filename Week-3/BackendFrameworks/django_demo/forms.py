"""
Django Forms Module.

This file handles user inputs and forms. It demonstrates how Django's ModelForm
automatically maps a Model's fields to an HTML form, validates types, and runs custom validations.
"""

from django import forms
from django.utils import timezone
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form based directly on the Book Model.
    
    Demonstrates:
    - Automatic field generation matching DB schema.
    - Custom widgets (e.g. DateInput).
    - Custom field-level validation.
    """
    
    class Meta:
        model = Book
        # Specify fields to display in the HTML form
        fields = ["title", "summary", "publish_date", "author"]
        
        # Override default HTML widgets for form rendering
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter book title"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "publish_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "author": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_publish_date(self):
        """
        Custom validation for the 'publish_date' field.
        
        Rule: A book's publication date cannot be set in the future.
        """
        publish_date = self.cleaned_data.get("publish_date")
        
        # If the date is in the future, raise a ValidationError
        if publish_date and publish_date > timezone.now().date():
            raise forms.ValidationError("The publication date cannot be in the future.")
            
        # Always return the cleaned data
        return publish_date
        
    def clean(self):
        """
        Custom validation covering multiple fields.
        
        Rule: The title of the book cannot be in the summary.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        summary = cleaned_data.get("summary")
        
        if title and summary and title.lower() in summary.lower():
            raise forms.ValidationError(
                "The summary should not contain the exact title of the book to avoid redundancy."
            )
            
        return cleaned_data
