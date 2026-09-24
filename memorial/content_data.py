import re

from django.conf import settings

from .maps import google_maps_directions_url, google_maps_place_url
from .models import GalleryImage, HomePageContent, LifeChapter, Tribute, VisitLocation

DEFAULT_HOME_PAGE = {
    "intro_lead": (
        "Beloved patriarch, farmer, elder, and keeper of stories. This memorial gathers the "
        "funeral programme, life story, and words of those who loved him."
    ),
    "portrait_caption": "He walked gently, but left deep footprints.",
    "programme_title": "Funeral programme",
    "programme_lead": (
        "Burial and homegoing service — Thursday, 25 September 2026 at "
        "PCEA Mbogori Church, Chogoria (Mbogori Marigwe)."
    ),
    "programme_timeline": """Thursday, 25 September 2026 : Burial day
7:00 AM : Departure from home – Mbogori
8:00 AM : Arrival at mortuary — viewing of the body
9:00 AM : Departure from Chogoria
10:00 AM : Arrival at PCEA Mbogori Church, Chogoria
10:30 AM : Funeral service and burial""",
    "programme_service": """Hymn song
Opening prayer
Welcome remarks by chairman
Family representative to welcome the people
Eulogy
Tributes
Family representative (song)
Recognition/speeches
Representative from Meru
Tharaka Nithi County
Embu county
Nairobi County
Any other County
Sermon
Prayer for the family
Laying of wealth
Vote of thanks
Refreshments""",
    "programme_closing": "Guests leave at their own leisure.",
}

DEFAULT_LIFE_CHAPTERS = [
    (
        1930,
        1,
        "Early Life and Family Background",
        """The late Fredrick Guantai Mugira was born in 1930 at Kiamwere village, Nkunjumu Sub-location, Kiangua Location, Meru County. He later moved to Kiangua and finally settled at Mbogori Marigwe village.

He was the son of the late Mugira Kujoga and the late Thamaru Kagoki. He was brother to the late Margaret Muthoni, Japhet Kaburu and Jane Kanini. He was brother-in-law to Muthoni, Nyaga, Shadrack, Jenifer, Eustace, Justus and Kellen Nkuene.""",
    ),
    (
        1945,
        2,
        "Education",
        "Fredrick grew up in the village and attended Kiangu Intermediate School.",
    ),
    (
        1964,
        3,
        "Marriage and Family Life",
        """Guantai married his beloved wife, the late Hellen Mukwamwebia Guantai in 1964. They were blessed with the following children: Dores, Kainyu, the late David Kiria, Silviah, Kagendo, the late Lucy Wanja, Mary Karimi and Patrick Mugambi.

He was father-in-law to Silas Mutwiri, Ida Kagendo, George Mbae and Nancy Muthoni. He was grandfather to Elsie and Martin, Doreen and Mutugi, Karen, Mwende, Mark, Fred, Kimathi, Kawira, Job, Raphael and Dan. He was great-grandfather to Kendi, Muthomi, Kanana, Jayden, Mwandiki, Mwende and Kathomi.""",
    ),
    (
        1965,
        4,
        "Faith and Church Life",
        "He was a full member of PCEA Mbogori Church and a very active member of Marigwe District.",
    ),
    (
        2024,
        5,
        "Social Life and Community",
        """Guantai was a caring person who loved peace. He interacted with everybody and welcomed people to his home for a cup of tea. He wanted people to be united and live together — in 2024 he called all the members of the Mugira family and ensured that we have known one another.

He also loved saying "SAWA" and noburia Murungu akenda. He served the community and was founder member of Mbogori Primary School, Mbogori Tea Collection Centre, Marigwe tea buying center and Thambu water project, among other projects.""",
    ),
    (
        2026,
        6,
        "Work, Health, and Homegoing",
        """Guantai was a prominent coffee, tea and dairy farmer. He was also in the timber business in the 1980s.

Guantai enjoyed good and steady health up to 2020 (COVID-19), when he started ailing. He was admitted at St. Theresa Hospital, then continued attending clinics and was admitted in Chogoria Hospital, then Kenyatta National Hospital and Kenyatta University Referral and Teaching Hospital, where he was until 17th September 2026, when he was promoted to glory at 6:00 a.m.""",
    ),
]

DEFAULT_TRIBUTES = [
    (
        "The In-laws",
        "In-laws",
        """You were much more than a father-in-law to us; you were a mentor, a second father, and a quiet anchor for our whole family. From the very first day we joined this family, you welcomed us with open arms, endless patience, and a warmth that made us feel instantly safe and loved.

We see your goodness, your strength, and your gentle heart every single day in the persons we love most—your children. The way they care for others, stand tall in hard times, and love with their whole heart is the greatest reflection of the man who raised them.

Though your absence leaves a heavy ache in our chests, your wisdom, your laughter, and the beautiful memories we shared will stay with us forever. Thank you for the life you lived, the lessons you taught, and the incredible love you gave so freely. Rest in peace.""",
    ),
    (
        "Loved ones",
        "To Ntagu",
        """Ntagu, you brought a special light into my life with your big heart and deep love. Staying by your side in the hospital was my way of giving back the care and warmth you always showed me. Even in hard times, your strength stayed with me. I will miss you forever, but your love will always stay in my heart. Rest in peace.

Ntagu, you loved me with all your heart, and I felt that care in every moment we shared together. Sitting by your bed, holding your hand, and taking care of you became my sacred duty out of love. Your pain is gone now, but the sweet memory of you will stay with me always.""",
    ),
    (
        "Elsie",
        "Grandchild",
        """Today I honour a remarkable man — my dear grandpa, the man who was my first and truest guardian. It is hard to put into words the depth of love and gratitude I feel for you.

You were not just a grandfather; you were a steady hand, a listening ear, a protector of my dreams, and a beacon of strength through all of life's storms. You taught me so much, not just through your words, but through your unwavering example. Your wisdom, your kindness, and your gentle spirit have shaped me in ways I can never fully express.

Thank you for every lesson and for every moment of protection. The world feels a little dimmer without you, but the light of your love will forever guide my way. I will carry you in my heart always. Rest in eternal peace, Grandie.""",
    ),
    (
        "The Grandchildren",
        "Grandchildren",
        """Jûjû, shosh, Babu, jûjû wa mûbuto — he answered to all with love and a smile. Grandpa was many things to his grandchildren, but the one thing we can all agree on, and that is most memorable to us all, was his generosity and unequaled love for us.

His actions made sure each one of us felt loved, cared for, and appreciated. Most of us hear his name and associate it with honey and meat because that is who he was to us. Every time after harvesting honey in the forest we were assured that he would divide it for us and keep it. Even when we were in school, we were assured that when we came home for the holidays, a small mkebe ya kimbo full of honey or a plate kept specifically for you would be waiting.

For most of us, we learnt how to stir honey into the morning tea mug to boka with leftover food from supper. Celebrations were a ritual we knew he would not skip. A cow or goat slaughtered meant that we would have soup made from the head and feet while he tried to teach us the basics of what was supposed to go into the soup to make it medicinal.

For us, back then it seemed like he would always be there to dispense wisdom — the stories seated around a fire in the dark in his gâru while the pot of soup bubbled away. Stories of a time gone by and wisdom for the ages. Juju was generous with all that he had and made sure we all got a portion.

As we grew older, he learnt to accommodate us as adults. He would advise, encourage, and cheer us on in every step of life. He would accept us and correct us with love. When we visited, he would encourage us to go into the shamba and carry what was in season: bananas, arrowroots, and his famous yams.

A fond memory is finding him seated in the dirt with his trousers caked in mud at the knees, holding a stick sharpened on one end, smiling with his recent harvest of yams next to him. He would divide them for each family and leave some for himself to roast and share with whichever grandkid was around.

His work ethic was unbeatable. He believed in doing things the right way and ensuring they were done how he wanted. Up until his old age, he would go to the shamba every day to ensure the work was being done the right way. Every day early in the morning he would go to mûuro to take care of his cows and land. For us, that meant being sent to take him lunch — a treat in itself since we would eat endless sugarcane that he peeled for us, loquats in season that he picked for us, and him patiently enduring endless questions on why the river had no fish.

Grandpa valued education and encouraged us to pursue it to the highest levels we could. He celebrated every major milestone with us, encouraged us when we lost hope, and became our biggest cheerleader. Woe unto you if you tried to debate politics with him. He was knowledgeable in ways that challenged you. He respected your opinion but would not hesitate to disagree with it. You would leave the conversation having learnt something new and having had your opinions challenged in the best possible way.

Juju will be dearly missed by us all. We rejoice in the hope that he is in a better place, free from the troubles of this world. We take his lessons with us to carry us through life and his memories to be treasured forever. Go well, Grandpa.""",
    ),
    (
        "His Children",
        "Children",
        """Dad, leaving us leaves a profound space in our lives, but the strength, wisdom, and warmth you shared remain an enduring part of who we are today. As we gather to honour you, we remember a man who was the true pillar of our family — a man who was both our mother and our father for the last eighteen years.

You were a leader who led by example, nurtured our growth, and taught us how to walk through life with integrity. Dad was, above all else, our mentor, a natural guide who invested deeply in our lives, teaching us not just how to succeed, but how to live a life of true character.

You lived by principles that never wavered. You championed hard work, showing us through your own tireless actions that dedication and perseverance are the foundations of a good life. You spoke the truth, kept your promises, and taught us that a person's word is their bond — be a truthful person.

Dad had a rare, beautiful love for visitors. Our home under your care was always a place of warmth, open doors, and abundant hospitality. No one was a stranger to you for long. You were the bridge to our roots. In the last two years you made it your personal mission to ensure we knew our history. You went out of your way to introduce us to our distant relatives — our people in Giaki — keeping our family bond strong, united, and wide-reaching.

You looked at each of us, saw our unique potential, and patiently nurtured us into the people we are today. As we say our final goodbyes, we take comfort in knowing that your lessons are etched into our daily choices. We will hold tightly to the beautiful community and family you built.

Dad, you are a man who gave so much of himself to others; you are never truly gone. Rest in peace, Dad.""",
    ),
    (
        "His Sister",
        "Sister",
        """We are here today to honour a man who did not just live his life for himself, but also for others. When I look back at my life, I know exactly who to thank for the foundation I stand on. It was my brother Guantai.

At a very tender age you stepped in, together with your late wife, our beloved Hellen, and opened your hearts and your home to me. Together, you became my protectors, my providers, and my safe harbour. You treated me as your own child, ensuring I never felt the weight of the world, because you carried it for me.

You made it your mission to see me succeed and educated me to the highest level I could reach. Every word of encouragement was a brick you laid to build my future. You poured your own hard work into my dreams, and any success I have today belongs entirely to you.

I find comfort knowing that you are now reunited with Hellen. You were a team in life, you were a team in raising me, and your legacy lives on through the life you built for me.

To my brother: thank you for picking me up. Thank you for educating me. Thank you for loving me when I needed it most. You gave me everything, and I will spend the rest of my days living a life that honours your sacrifice. Rest in peace, my brother. You will never be forgotten.""",
    ),
]

LIFE_STORY_CHAPTER_META = [
    {"icon_id": "roots", "short_label": "Origins", "symbol": "🌱"},
    {"icon_id": "book", "short_label": "School days", "symbol": "📖"},
    {"icon_id": "heart", "short_label": "Family", "symbol": "💛"},
    {"icon_id": "faith", "short_label": "Faith", "symbol": "✝"},
    {"icon_id": "community", "short_label": "Community", "symbol": "🤝"},
    {"icon_id": "legacy", "short_label": "Legacy", "symbol": "🕊"},
]

def ensure_visit_locations():
    """Create visit rows from settings so public pages match the admin location editor."""
    for key, data in settings.MEMORIAL_VISIT.items():
        VisitLocation.objects.get_or_create(
            slug=data.get("slug", key),
            defaults={
                "title": data["title"],
                "subtitle": data["subtitle"],
                "place_name": data["place_name"],
                "maps_query": data["maps_query"],
                "order": 0 if key == "church" else 1,
            },
        )


def get_life_chapters():
    return LifeChapter.objects.order_by("order", "year")


def seed_default_life_chapters():
    if LifeChapter.objects.exists():
        return 0
    for year, order, title, body in DEFAULT_LIFE_CHAPTERS:
        LifeChapter.objects.create(year=year, title=title, body=body, order=order)
    return len(DEFAULT_LIFE_CHAPTERS)


def _split_name_list(fragment):
    names = re.split(r",\s*|\s+and\s+", fragment)
    return [n.strip() for n in names if n.strip()]


def _chapter_tags(chapter):
    body = chapter.body
    lower = body.lower()
    if "children:" in lower:
        match = re.search(r"children:\s*(.+?)(?:\.\n|\.$|\n)", body, re.IGNORECASE | re.DOTALL)
        if match:
            return {"label": "Children", "names": _split_name_list(match.group(1))}
    return None


def _chapter_callout(chapter):
    if "SAWA" not in chapter.body:
        return None
    return {
        "word": "SAWA",
        "note": "All is well — a greeting he gave freely.",
        "meru": "Noburia Murungu akenda — may God go with you.",
    }


def build_life_story_items(chapters):
    chapter_list = list(chapters)
    items = []
    for index, chapter in enumerate(chapter_list):
        meta = LIFE_STORY_CHAPTER_META[index] if index < len(LIFE_STORY_CHAPTER_META) else LIFE_STORY_CHAPTER_META[-1]
        paragraphs = [p.strip() for p in chapter.body.split("\n\n") if p.strip()]
        items.append(
            {
                "chapter": chapter,
                "meta": meta,
                "paragraphs": paragraphs,
                "tags": _chapter_tags(chapter),
                "callout": _chapter_callout(chapter),
                "is_finale": index == len(chapter_list) - 1,
            }
        )
    return items


def sync_default_tributes(*, replace=False):
    """Load DEFAULT_TRIBUTES; replace=True clears existing rows first."""
    from django.utils import timezone

    if replace:
        Tribute.objects.all().delete()
    elif Tribute.objects.exists():
        return 0

    now = timezone.now()
    count = len(DEFAULT_TRIBUTES)
    for index, (author_name, relationship, message) in enumerate(DEFAULT_TRIBUTES):
        tribute = Tribute.objects.create(
            author_name=author_name,
            relationship=relationship,
            message=message,
            is_approved=True,
        )
        # First entry in DEFAULT_TRIBUTES appears first on the public page (-created_at).
        tribute.created_at = now - timezone.timedelta(minutes=index)
        tribute.save(update_fields=["created_at"])
    return count


def _tribute_display_meta(relationship):
    key = (relationship or "").strip().lower()
    if "in-law" in key:
        return {"accent": "rose", "symbol": "💐", "label": "In-laws"}
    if "ntagu" in key:
        return {"accent": "gold", "symbol": "💛", "label": "To Ntagu"}
    if key == "grandchild":
        return {"accent": "sky", "symbol": "✨", "label": "Grandchild"}
    if "grandchild" in key:
        return {"accent": "coral", "symbol": "🍯", "label": "Grandchildren"}
    if "child" in key:
        return {"accent": "emerald", "symbol": "🌿", "label": "Children"}
    if "sister" in key:
        return {"accent": "violet", "symbol": "🕊", "label": "Sister"}
    return {"accent": "teal", "symbol": "♥", "label": relationship or "Tribute"}


def _tribute_excerpt(message, limit=160):
    text = " ".join((message or "").split())
    if len(text) <= limit:
        return text
    snippet = text[:limit].rsplit(" ", 1)[0]
    return snippet + "…"


def build_tribute_items(tributes):
    items = []
    for tribute in tributes:
        meta = _tribute_display_meta(tribute.relationship)
        items.append(
            {
                "tribute": tribute,
                "meta": meta,
                "excerpt": _tribute_excerpt(tribute.message),
                "filter_key": meta["label"].lower().replace(" ", "-"),
            }
        )
    return items


def get_approved_tributes():
    return Tribute.objects.filter(is_approved=True).order_by("-created_at")


GALLERY_ROTATE_SESSION_KEY = "gallery_display_offset"
GALLERY_PREVIEW_SESSION_KEY = "gallery_preview_offset"


def normalize_gallery_orders():
    """Renumber gallery rows 0…n so duplicate order values do not freeze sort by id."""
    photos = list(GalleryImage.objects.order_by("order", "id"))
    updates = []
    for index, photo in enumerate(photos):
        if photo.order != index:
            photo.order = index
            updates.append(photo)
    if updates:
        GalleryImage.objects.bulk_update(updates, ["order"])
    return len(updates)


def get_gallery_photos():
    """Stable sort order (dashboard and maintenance)."""
    return GalleryImage.objects.order_by("order", "id")


def _gallery_ordered_list():
    return list(get_gallery_photos())


def _rotate_gallery_list(photos, offset):
    if len(photos) < 2:
        return photos
    offset = offset % len(photos)
    if offset == 0:
        return photos
    return photos[offset:] + photos[:offset]


def get_gallery_photos_display(request):
    """
    Public gallery order: rotate on each visit so the same photos are not always first.
    """
    photos = _gallery_ordered_list()
    if len(photos) < 2 or request is None:
        return photos

    offset = int(request.session.get(GALLERY_ROTATE_SESSION_KEY, 0))
    request.session[GALLERY_ROTATE_SESSION_KEY] = (offset + 1) % len(photos)
    request.session.modified = True
    return _rotate_gallery_list(photos, offset)


def get_gallery_preview(request, limit=4):
    """Home page gallery strip — separate rotation from full gallery page."""
    photos = _gallery_ordered_list()
    if not photos:
        return []
    limit = min(limit, len(photos))
    if len(photos) < 2 or request is None:
        return photos[:limit]

    offset = int(request.session.get(GALLERY_PREVIEW_SESSION_KEY, 0)) % len(photos)
    request.session[GALLERY_PREVIEW_SESSION_KEY] = (offset + 1) % len(photos)
    request.session.modified = True
    return [photos[(offset + i) % len(photos)] for i in range(limit)]


def get_visit_destinations():
    ensure_visit_locations()
    locations = VisitLocation.objects.order_by("order", "slug")
    if locations.exists():
        destinations = []
        for loc in locations:
            destinations.append(
                {
                    "slug": loc.slug,
                    "title": loc.title,
                    "subtitle": loc.subtitle,
                    "place_name": loc.place_name,
                    "maps_query": loc.maps_query,
                    "key": loc.slug,
                    "maps_url": google_maps_place_url(loc.maps_query),
                    "directions_url": google_maps_directions_url(loc.maps_query),
                }
            )
        return destinations

    destinations = []
    for key, data in settings.MEMORIAL_VISIT.items():
        destinations.append(
            {
                **data,
                "key": key,
                "maps_url": google_maps_place_url(data["maps_query"]),
                "directions_url": google_maps_directions_url(data["maps_query"]),
            }
        )
    return destinations


def parse_programme_timeline(text):
    items = []
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        if ":" in line:
            time_part, _, label = line.partition(":")
            items.append({"time": time_part.strip(), "label": label.strip()})
        else:
            items.append({"time": "", "label": line})
    return items


def parse_programme_service(text):
    return [line.strip() for line in (text or "").splitlines() if line.strip()]


def get_home_page_content():
    instance = HomePageContent.objects.first()
    if instance:
        return instance
    return HomePageContent.objects.create(**DEFAULT_HOME_PAGE)


def resolve_visit_maps_query(place_slug):
    ensure_visit_locations()
    loc = VisitLocation.objects.filter(slug=place_slug).first()
    if loc:
        return loc.maps_query
    locations = settings.MEMORIAL_VISIT
    if place_slug in locations:
        return locations[place_slug]["maps_query"]
    return None
