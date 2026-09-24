from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .admin_auth import (
    credentials_valid,
    is_memorial_admin,
    memorial_admin_login,
    memorial_admin_logout,
    require_memorial_admin,
)
from .content_data import (
    ensure_visit_locations,
    get_gallery_photos,
    normalize_gallery_orders,
    get_home_page_content,
    get_life_chapters,
)
from .forms import (
    GalleryImageEditForm,
    GalleryImageForm,
    HomePageContentForm,
    LifeChapterAdminFormSet,
    MemorialAdminLoginForm,
    MemorialQuoteForm,
    TributeAdminFormSet,
    VisitLocationForm,
)
from .models import (
    GalleryImage,
    HomePageContent,
    LifeChapter,
    MemorialQuote,
    Tribute,
    VisitLocation,
)


@require_http_methods(["GET"])
def dashboard_home(request):
    if not is_memorial_admin(request):
        return redirect("memorial:dashboard_login")
    return render(
        request,
        "memorial/dashboard/home.html",
        {"page_title": "Admin Dashboard"},
    )


@require_http_methods(["GET", "POST"])
def dashboard_login(request):
    if is_memorial_admin(request):
        return redirect("memorial:dashboard_home")

    next_url = request.GET.get("next") or request.POST.get("next") or ""
    form = MemorialAdminLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"].strip()
        password = form.cleaned_data["password"]
        if credentials_valid(username, password):
            memorial_admin_login(request)
            messages.success(request, "Welcome. You are signed in to the admin dashboard.")
            if next_url.startswith("/"):
                return redirect(next_url)
            return redirect("memorial:dashboard_home")
        messages.error(request, "Invalid login or password. Please try again.")

    return render(
        request,
        "memorial/dashboard/login.html",
        {
            "page_title": "Employee Login",
            "form": form,
            "next": next_url,
        },
    )


@require_http_methods(["POST"])
def dashboard_logout(request):
    memorial_admin_logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("memorial:dashboard_login")


@require_memorial_admin
@require_http_methods(["GET", "POST"])
def dashboard_home_update(request):
    quote_instance = MemorialQuote.objects.filter(is_active=True).first()
    if quote_instance is None:
        quote_instance = MemorialQuote.objects.order_by("id").first()

    home_instance = get_home_page_content()

    if request.method == "POST":
        quote_form = MemorialQuoteForm(
            request.POST,
            instance=quote_instance,
            prefix="quote",
        )
        home_form = HomePageContentForm(
            request.POST,
            request.FILES,
            instance=home_instance,
            prefix="home",
        )
        if quote_form.is_valid() and home_form.is_valid():
            quote_form.save()
            saved_home = home_form.save()
            HomePageContent.objects.exclude(pk=saved_home.pk).delete()
            messages.success(request, "Home page updated successfully.")
            return redirect("memorial:dashboard_home_update")
    else:
        quote_form = MemorialQuoteForm(instance=quote_instance, prefix="quote")
        home_form = HomePageContentForm(instance=home_instance, prefix="home")

    return render(
        request,
        "memorial/dashboard/home_update.html",
        {
            "page_title": "Home Page Update",
            "quote_form": quote_form,
            "home_form": home_form,
        },
    )


@require_memorial_admin
@require_http_methods(["GET", "POST"])
def dashboard_life_story(request):
    queryset = get_life_chapters()
    formset = LifeChapterAdminFormSet(
        request.POST or None,
        queryset=queryset,
        prefix="chapters",
    )
    if request.method == "POST" and formset.is_valid():
        formset.save()
        messages.success(request, "Life story chapters updated successfully.")
        return redirect("memorial:dashboard_life_story")

    return render(
        request,
        "memorial/dashboard/life_story.html",
        {
            "page_title": "Life Story Update",
            "formset": formset,
        },
    )


@require_memorial_admin
@require_http_methods(["GET", "POST"])
def dashboard_tributes(request):
    queryset = Tribute.objects.order_by("-created_at")
    formset = TributeAdminFormSet(
        request.POST or None,
        queryset=queryset,
        prefix="tributes",
    )
    if request.method == "POST":
        if formset.is_valid():
            formset.save()
            messages.success(request, "Tributes updated successfully.")
            return redirect("memorial:dashboard_tributes")
        messages.error(
            request,
            "Could not save. Check each tribute below for errors, then try again.",
        )

    return render(
        request,
        "memorial/dashboard/tributes.html",
        {
            "page_title": "Tributes Update",
            "formset": formset,
        },
    )


@require_memorial_admin
@require_http_methods(["GET", "POST"])
def dashboard_gallery(request):
    if request.method == "POST":
        if "delete_id" in request.POST:
            photo = get_object_or_404(GalleryImage, pk=request.POST["delete_id"])
            photo.image.delete(save=False)
            photo.delete()
            normalize_gallery_orders()
            messages.success(request, "Photo removed from the gallery.")
            return redirect("memorial:dashboard_gallery")

        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            normalize_gallery_orders()
            messages.success(request, "Photo added to the gallery.")
            return redirect("memorial:dashboard_gallery")
        return render(
            request,
            "memorial/dashboard/gallery.html",
            {
                "page_title": "Gallery Update",
                "upload_form": form,
                "photos": get_gallery_photos(),
            },
        )

    return render(
        request,
        "memorial/dashboard/gallery.html",
        {
            "page_title": "Gallery Update",
            "upload_form": GalleryImageForm(),
            "photos": get_gallery_photos(),
        },
    )


@require_memorial_admin
@require_http_methods(["GET", "POST"])
def dashboard_gallery_edit(request, pk):
    photo = get_object_or_404(GalleryImage, pk=pk)
    if request.method == "POST":
        form = GalleryImageEditForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            updated = form.save(commit=False)
            if not form.cleaned_data.get("image"):
                updated.image = photo.image
            updated.save()
            messages.success(request, "Photo updated.")
            return redirect("memorial:dashboard_gallery")
    else:
        form = GalleryImageEditForm(instance=photo)

    return render(
        request,
        "memorial/dashboard/gallery_edit.html",
        {
            "page_title": "Edit photo",
            "photo": photo,
            "edit_form": form,
        },
    )


@require_memorial_admin
@require_http_methods(["GET", "POST"])
def dashboard_location(request):
    ensure_visit_locations()
    locations = list(VisitLocation.objects.order_by("order", "slug"))

    forms_list = []
    if request.method == "POST":
        for loc in locations:
            form = VisitLocationForm(
                request.POST,
                instance=loc,
                prefix=f"loc-{loc.pk}",
            )
            forms_list.append((loc, form))
        if all(f.is_valid() for _, f in forms_list):
            for _, f in forms_list:
                f.save()
            messages.success(request, "Visit locations updated successfully.")
            return redirect("memorial:dashboard_location")
    else:
        for loc in locations:
            forms_list.append((loc, VisitLocationForm(instance=loc, prefix=f"loc-{loc.pk}")))

    return render(
        request,
        "memorial/dashboard/location.html",
        {
            "page_title": "Location Update",
            "location_forms": forms_list,
        },
    )
