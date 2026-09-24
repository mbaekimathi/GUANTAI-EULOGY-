from django.db import models


class LifeChapter(models.Model):
    """Milestone in the honoree's life, shown on timeline pages."""

    year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "year"]

    def __str__(self):
        return f"{self.year} — {self.title}"


class Tribute(models.Model):
    """Guest message submitted through the memorial site."""

    author_name = models.CharField(max_length=120)
    relationship = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Tribute from {self.author_name}"


class HomePageContent(models.Model):
    """Editable hero copy and funeral programme on the public home page."""

    intro_lead = models.TextField()
    portrait_image = models.ImageField(
        upload_to="home/portraits/",
        blank=True,
        help_text="Photo shown in the hero portrait on the public home page.",
    )
    portrait_caption = models.CharField(max_length=300)
    programme_title = models.CharField(max_length=200)
    programme_lead = models.TextField(blank=True)
    programme_timeline = models.TextField(
        help_text="One event per line, e.g. 7:00 AM : Departure from home",
    )
    programme_service = models.TextField(
        help_text="Order of service — one item per line.",
    )
    programme_closing = models.CharField(max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Home page content"

    def __str__(self):
        return "Home page content"


class MemorialQuote(models.Model):
    """Rotating quotes or scripture for footer and home."""

    text = models.TextField()
    attribution = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text[:60]


class EulogyContent(models.Model):
    """Editable eulogy text shown on the public eulogy page."""

    hero_lead = models.TextField()
    body = models.TextField(
        help_text="Separate paragraphs with a blank line.",
    )
    closing_prayer = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Eulogy content"

    def __str__(self):
        return "Eulogy content"

    def body_paragraphs(self):
        return [p.strip() for p in self.body.split("\n\n") if p.strip()]


class GalleryImage(models.Model):
    """Photo in the memorial gallery."""

    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Gallery image {self.pk}"


class VisitLocation(models.Model):
    """Church, family home, or other visit destinations for maps."""

    slug = models.SlugField(max_length=40, unique=True)
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=200)
    place_name = models.CharField(max_length=200)
    maps_query = models.CharField(max_length=500)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "slug"]

    def __str__(self):
        return self.title
