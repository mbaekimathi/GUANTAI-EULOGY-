from django import forms
from django.forms import modelformset_factory

from .models import (
    GalleryImage,
    HomePageContent,
    LifeChapter,
    MemorialQuote,
    Tribute,
    VisitLocation,
)


class TributeForm(forms.ModelForm):
    class Meta:
        model = Tribute
        fields = ("author_name", "relationship", "message")
        widgets = {
            "author_name": forms.TextInput(
                attrs={
                    "placeholder": "Your full name",
                    "autocomplete": "name",
                }
            ),
            "relationship": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Grandson, Friend, Neighbor",
                    "autocomplete": "off",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Share a memory, prayer, or word of comfort…",
                    "rows": 5,
                }
            ),
        }

    def save(self, commit=True):
        tribute = super().save(commit=False)
        tribute.is_approved = False
        if commit:
            tribute.save()
        return tribute


class MemorialAdminLoginForm(forms.Form):
    username = forms.CharField(
        label="Login",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "class": "login-field__control",
                "placeholder": "987654321",
                "autocomplete": "username",
                "inputmode": "numeric",
                "autofocus": True,
                "spellcheck": "false",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "login-field__control",
                "placeholder": "Enter password",
                "autocomplete": "current-password",
            }
        ),
    )


class HomePageContentForm(forms.ModelForm):
    class Meta:
        model = HomePageContent
        fields = (
            "intro_lead",
            "portrait_image",
            "portrait_caption",
            "programme_title",
            "programme_lead",
            "programme_timeline",
            "programme_service",
            "programme_closing",
        )
        widgets = {
            "intro_lead": forms.Textarea(attrs={"rows": 3}),
            "portrait_image": forms.ClearableFileInput(
                attrs={"accept": "image/*", "class": "form-field__file"}
            ),
            "portrait_caption": forms.TextInput(
                attrs={"placeholder": "Caption under the portrait on home"}
            ),
            "programme_title": forms.TextInput(attrs={"placeholder": "Funeral programme"}),
            "programme_lead": forms.Textarea(attrs={"rows": 2}),
            "programme_timeline": forms.Textarea(
                attrs={
                    "rows": 8,
                    "placeholder": "7:00 AM : Departure from home",
                }
            ),
            "programme_service": forms.Textarea(
                attrs={
                    "rows": 14,
                    "placeholder": "One line per part of the service",
                }
            ),
            "programme_closing": forms.TextInput(
                attrs={"placeholder": "e.g. Guests leave at their own leisure."}
            ),
        }


class MemorialQuoteForm(forms.ModelForm):
    class Meta:
        model = MemorialQuote
        fields = ("text", "attribution", "is_active")
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Featured quote shown on the home page",
                }
            ),
            "attribution": forms.TextInput(
                attrs={"placeholder": "Optional — who said it"}
            ),
        }


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ("image", "caption")
        widgets = {
            "caption": forms.TextInput(attrs={"placeholder": "Optional caption"}),
        }


class GalleryImageEditForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ("caption", "image")
        widgets = {
            "caption": forms.TextInput(attrs={"placeholder": "Optional caption"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False
        self.fields["image"].help_text = "Leave empty to keep the current photo."


class VisitLocationForm(forms.ModelForm):
    class Meta:
        model = VisitLocation
        fields = ("slug", "title", "subtitle", "place_name", "maps_query", "order")
        widgets = {
            "maps_query": forms.TextInput(
                attrs={"placeholder": "Address or place name for Google Maps"}
            ),
            "order": forms.NumberInput(attrs={"min": 0}),
        }


class TributeAdminForm(forms.ModelForm):
    class Meta:
        model = Tribute
        fields = ("author_name", "relationship", "message", "is_approved")
        widgets = {
            "author_name": forms.TextInput(
                attrs={"placeholder": "Author name", "autocomplete": "off"}
            ),
            "relationship": forms.TextInput(
                attrs={
                    "placeholder": "Relationship (optional)",
                    "autocomplete": "off",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Tribute message",
                    "rows": 10,
                }
            ),
        }


TributeAdminFormSet = modelformset_factory(
    Tribute,
    form=TributeAdminForm,
    extra=1,
    can_delete=True,
    max_num=500,
)


class LifeChapterForm(forms.ModelForm):
    class Meta:
        model = LifeChapter
        fields = ("year", "title", "body", "order")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Chapter title"}),
            "body": forms.Textarea(attrs={"rows": 5}),
            "year": forms.NumberInput(attrs={"min": 1800, "max": 2100}),
            "order": forms.NumberInput(attrs={"min": 0}),
        }


LifeChapterAdminFormSet = modelformset_factory(
    LifeChapter,
    form=LifeChapterForm,
    extra=1,
    can_delete=True,
)
