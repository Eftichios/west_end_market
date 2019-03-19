import os
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamC_project.settings')

import django
django.setup()


from west_end_market.models import Category, Listing, Comment, User


def populate():

    users = {"user_1": {"username": "JohnPope", "email": "JohnPope@email.com"},
             "user_2": {"username": "ChristopherSmith", "email": "ChristopherSmith@email.com"},
             "user_3": {"username": "PeterBrown", "email": "PeterBrown@email.com"},
             "user_4": {"username": "James", "email": "James@email.com"},
             "user_5": {"username": "Veronica", "email": "Veronica@email.com"},
             "user_6": {"username": "Maria", "email": "Maria@email.com"},
             "user_7": {"username": "Victor", "email": "Victor@email.com"},
             "user_8": {"username": "Batman", "email": "Batman@email.com"}}

    school = [{"id": "sch1",
                     "title": "Introduction to Linear Algebra",
                     "description": "Used book but in very good condition",
                     "price": 50,
                     "category": "school",
                     "user": "JohnPope",
                     "date": timezone.now(),
                     "picture": "JohnPope/linear.jpg",
                     "postcode": "PC SCH1"},

              {"id": "sch2",
                     "title": "Introduction to Calculus",
                     "description": "Brand new book",
                     "price": 70,
                     "category": "school",
                     "user": "ChristopherSmith",
                     "date": timezone.now(),
                     "picture": "ChristopherSmith/calculus.jpg",
                     "postcode": "PC SCH2"},

              {"id": "sch3",
                     "title": "How to tango with django",
                     "description": "Brand new book",
                     "price": 20,
                     "category": "school",
                     "user": "PeterBrown",
                     "date": timezone.now(),
                     "picture": "PeterBrown/django.jpg",
                     "postcode": "PC SCH3"}]

    electronics = [{"id": "ele1",
                          "title": "Brand new anker bluetooth earphones",
                          "description": "Anker Bluetooth Headphones, SoundBuds Slim Lightweight Wireless Headphones, IPX5 Sweatproof Sports Headphones with Mic and 7 Hrs Play Time for Running, Cycling, Gym, Travelling and More",
                          "price": 20,
                          "category": "electronics",
                          "user": "James",
                          "date": timezone.now(),
                          "picture": "James/earphones.jpg",
                          "postcode": "PC ELE1"},

                   {"id": "ele2",
                          "title": "Used Xiaomi MI A1, in very good contition!",
                          "description": "64GB Black dual camera 5.5in",
                          "price": 115,
                          "category": "electronics",
                          "user": "Veronica",
                          "date": timezone.now(),
                          "picture": "Veronica/xiaomi.jpg",
                          "postcode": "PC ELE2"},

                   {"id": "ele3",
                          "title": "Used laptop HP EliteBook 745",
                          "description": "Windows 10, 6GB RAM, 256GB SSD storage...",
                          "price": 580,
                          "category": "electronics",
                          "user": "Maria",
                          "date": timezone.now(),
                          "picture": "Maria/laptop.jpg",
                          "postcode": "PC ELE3"}]

    clothing = [{"id": "clo1",
                       "title": "Black leather jacket for women",
                       "description": "Never worn, it was too small for me so im selling it. Perfect condition",
                       "price": 140,
                       "category": "clothing",
                       "user": "Maria",
                       "date": timezone.now(),
                       "picture": "Maria/jacket.jpg",
                       "postcode": "PC CLO1"},

                {"id": "clo2",
                       "title": "Tommy Hilfiger men's jeans",
                       "description": "Has some signs of wear but other than that it perfectly presentable",
                       "price": 65,
                       "category": "clothing",
                       "user": "ChristopherSmith",
                       "date": timezone.now(),
                       "picture": "ChristopherSmith/jeans.jpg",
                       "postcode": "PC CLO2"},

                {"id": "clo3",
                       "title": "Nike Air Jordan 1 Retro Og",
                       "description": "Brand new air jordan shoes, received as a gift and they are still in the box.",
                       "price": 100,
                       "category": "clothing",
                       "user": "PeterBrown",
                       "date": timezone.now(),
                       "picture": "PeterBrown/shoes.jpg",
                       "postcode": "PC CLO3"}]

    homeware = [{"id": "hom1",
                       "title": "DC Collectibles: Batman",
                       "description": "One of my favourites but my girlfriend told me to get rid of all my toys.",
                       "price": 20,
                       "category": "homeware",
                       "user": "Batman",
                       "date": timezone.now(),
                       "picture": "Batman/batman.jpg",
                       "postcode": "PC HOM1"},

                {"id": "hom2",
                       "title": "large ikea wooden desk (80x160)",
                       "description": "Has some scratches and marks that can't be removed but it's legs are strong.",
                       "price": 50,
                       "category": "homeware",
                       "user": "Victor",
                       "date": timezone.now(),
                       "picture": "Victor/desk.jpg",
                       "postcode": "PC HOM2"},

                {"id": "hom3",
                       "title": "Heavily used rice 1L cooker",
                       "description": "Not in a good condition but I want to get rid of it as I am moving out",
                       "price": 10,
                       "category": "homeware",
                       "user": "Veronica",
                       "date": timezone.now(),
                       "picture": "Veronica/rice.jpg",
                       "postcode": "PC HOM3"}]

    sports = [{"id": "spo1",
                     "title": "Bicycle",
                     "description": "A bit of a struggle when going uphill but other than that the bicycle is in a very good condition",
                     "price": 50,
                     "category": "sports",
                     "user": "James",
                     "date": timezone.now(),
                     "picture": "James/bicycle.jpg",
                     "postcode": "PC SPO1"},

              {"id": "spo2",
                     "title": "20 KG Black Cast Iron Dumbbell Spinlock Set",
                     "description": "locks are in perfect condition",
                     "price": 25,
                     "category": "sports",
                     "user": "JohnPope",
                     "date": timezone.now(),
                     "picture": "JohnPope/dumbbell.jpg",
                     "postcode": "PC SPO2"},

              {"id": "spo3",
                     "title": "HardCastle Flat Gym Bench",
                     "description": "Has been cleaned. In a decent condition",
                     "price": 20,
                     "category": "sports",
                     "user": "JohnPope",
                     "date": timezone.now(),
                     "picture": "JohnPope/bench.jpg",
                     "postcode": "PC SPO3"}]

    other = [{"id": "oth1",
                    "title": "Acoustic guitar",
                    "description": "Bought it a couple of weeks ago to learn but I gave up",
                    "price": 50,
                    "category": "other",
                    "user": "Victor",
                    "date": timezone.now(),
                    "picture": "Victor/guitar.jpg",
                    "postcode": "PC OTH1"},

             {"id": "oth2",
                    "title": "tickets for Disney On Ice - Platinum 12 APR 2019",
                    "description": "locks are in perfect condition",
                    "price": 25,
                    "category": "other",
                    "user": "Maria",
                    "date": timezone.now(),
                    "picture": "Maria/disney.jpg",
                    "postcode": "PC OTH2"},

             {"id": "oth3",
                    "title": "Limited Edition Brown Suede-look Crosley Record / Vinyl Player",
                    "description": "In excelent condition and in fully working order, however the needle may need changing soon as it sometimes struggles with older records",
                    "price": 40,
                    "category": "other",
                    "user": "ChristopherSmith",
                    "date": timezone.now(),
                    "picture": "ChristopherSmith/vinyl.jpg",
                    "postcode": "PC OTH3"}]

    cats = {"school": {"listings": school, "total": len(school)},
            "electronics": {"listings": electronics, "total": len(electronics)},
            "clothing": {"listings": clothing, "total": len(clothing)},
            "homeware": {"listings": homeware, "total": len(homeware)},
            "sports": {"listings": sports, "total": len(sports)},
            "other": {"listings": other, "total": len(other)}}

    comments = {"sch1": [{"comment": "I am interested!", "user": "Maria"},
                         {"comment": "Hey Maria, you can send me an email so we can discuss the details", "user": "JohnPope"}],
                "sch2": [{"comment": "Just send you an email", "user": "Veronica"},
                         {"comment": "I really need this book, I can make a you a better offer.", "user": "PeterBrown"}],
                "sch3": [{"comment": "Comment by user Batman here", "user": "Batman"},
                         {"comment": "Reply by user James", "user": "James"}],
                "ele1": [{"comment": "I am interested!", "user": "ChristopherSmith"},
                         {"comment": "Hey Christopher, you can send me an email so we can discuss the details", "user": "James"}],
                "ele2": [{"comment": "Just send you an email", "user": "PeterBrown"},
                         {"comment": "I really need this book, I can make a you a better offer. Check your email.", "user": "JohnPope"}],
                "ele3": [{"comment": "Comment by user here", "user": "Batman"},
                         {"comment": "Reply by user", "user": "James"}],
                "clo1": [{"comment": "Comment on clothing item 1", "user": "JohnPope"},
                         {"comment": "Another comment on clothing item 1", "user": "ChristopherSmith"}],
                "clo2": [{"comment": "Comment on clothing item 2", "user": "PeterBrown"},
                         {"comment": "Another comment on clothing item 2", "user": "James"}],
                "clo3": [{"comment": "Comment on clothing item 3", "user": "Veronica"},
                         {"comment": "Another comment on clothing item 3", "user": "Maria"}],
                "hom1": [{"comment": "Comment on homeware item 1", "user": "Victor"},
                         {"comment": "Another comment on homeware item 1", "user": "Batman"}],
                "hom2": [{"comment": "Comment on homeware item 2", "user": "JohnPope"},
                         {"comment": "Another comment on homeware item 2", "user": "ChristopherSmith"}],
                "hom3": [{"comment": "Comment on homeware item 3", "user": "PeterBrown"},
                         {"comment": "Another comment on homeware item 3", "user": "James"}],
                "spo1": [{"comment": "Comment on sports item 1", "user": "Veronica"},
                         {"comment": "Another comment on sports item 1", "user": "Maria"}],
                "spo2": [{"comment": "Comment on sports item 2", "user": "Victor"},
                         {"comment": "Another comment on sports item 2", "user": "Batman"}],
                "spo3": [{"comment": "Comment on sports item 3", "user": "JohnPope"},
                         {"comment": "Another comment on sports item 3", "user": "ChristopherSmith"}],
                "oth1": [{"comment": "Comment on others item 1", "user": "PeterBrown"},
                         {"comment": "Another comment on others item 1", "user": "James"}],
                "oth2": [{"comment": "Comment on others item 2", "user": "Veronica"},
                         {"comment": "Another comment on others item 2", "user": "Maria"}],
                "oth3": [{"comment": "Comment on others item 3", "user": "Victor"},
                         {"comment": "Another comment on others item 3", "user": "Batman"}]
                }

    for user, user_data in users.items():
        u = User.objects.get_or_create(username=user_data["username"], email=user_data["email"])[0]
        u.save()

    for cat, cat_data in cats.items():
        c = add_category(cat, cat_data["total"])
        for l in cat_data["listings"]:
            u = User.objects.get(username=l["user"])
            a = add_listing(l["id"], l["title"], l["description"], l["price"], c, u, l["date"], l["picture"], l["postcode"])
            if l["id"] in comments:
                for com in comments[l["id"]]:
                    u = User.objects.get(username=com["user"])
                    add_comment(com["comment"], u, a)

    for c in Category.objects.all():
        for l in Listing.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(l)))


def add_category(name, listings):
    c = Category.objects.get_or_create(name=name, listings=listings)[0]
    c.save()
    return c


def add_listing(id, title, description, price, category, user, date, picture, postcode):
    l = Listing.objects.get_or_create(id=id, title=title, description=description, price=price, category=category, user=user, date=date, picture=picture, postcode=postcode)[0]
    l.save()
    return l


def add_comment(comment, user, listing):
    co = Comment.objects.get_or_create(comment=comment, user=user, listing=listing)[0]
    co.save()
    return co


if __name__ == '__main__':
    print("Starting west_end_market population script...")
    populate()
