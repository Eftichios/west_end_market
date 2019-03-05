import os
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamC_project.settings')

import django
django.setup()


from west_end_market.models import Category, Listing, Comment, User


def populate():

    users = {"user_1": {"username": "John Pope"},
             "user_2": {"username": "Christopher Smith"},
             "user_3": {"username": "Peter Brown"},
             "user_4": {"username": "James"},
             "user_5": {"username": "Veronica"},
             "user_6": {"username": "Maria"}}

    school = [{"id": "s1",
                     "title": "Introduction to Linear Algebra",
                     "description": "Used book but in very good condition",
                     "price": 50,
                     "category": "school",
                     "user": "John Pope",
                     "date": timezone.now(),
                     "picture": "dog.jpg",
                     "postcode": "PCSCH1"},

                    {"id": "s2",
                     "title": "Introduction to Calculus",
                     "description": "Brand new book",
                     "price": 70,
                     "category": "school",
                     "user": "Christopher Smith",
                     "date": timezone.now(),
                     "picture": "dog.jpg",
                     "postcode": "PCSCH2"},

                    {"id": "s3",
                     "title": "How to tango with django",
                     "description": "Brand new book",
                     "price": 20,
                     "category": "school",
                     "user": "Peter Brown",
                     "date": timezone.now(),
                     "picture": "dog.jpg",
                     "postcode": "PCSCH3"}]

    electronics = [{"id": "e1",
                     "title": "Brand new anker bluetooth earphones ",
                     "description": "Anker Bluetooth Headphones, SoundBuds Slim Lightweight Wireless Headphones, IPX5 Sweatproof Sports Headphones with Mic and 7 Hrs Play Time for Running, Cycling, Gym, Travelling and More",
                     "price": 20,
                     "category": "electronics",
                     "user": "James",
                    "date": timezone.now(),
                    "picture": "dog.jpg",
                     "postcode": "PCELE1"},

                    {"id": "e2",
                     "title": "Used Xiaomi MI A1, in very good contition!",
                     "description": "64GB Black dual camera 5.5in",
                     "price": 115,
                     "category": "electronics",
                     "user": "Veronica",
                     "date": timezone.now(),
                     "picture": "dog.jpg",
                     "postcode": "PCELE1"},

                    {"id": "e3",
                     "title": "Used laptop HP EliteBook 745",
                     "description": "Windows 10, 6GB RAM, 256GB SSD storage...",
                     "price": 580,
                     "category": "electronics",
                     "user": "Maria",
                     "date": timezone.now(),
                     "picture": "dog.jpg",
                     "postcode": "PCELE1"}]

    cats = {"school": {"listings": school, "total": len(school)},
            "electronics": {"listings": electronics, "total": len(electronics)}}

    comments = {"s1": [{"comment": "Nice item!", "user": "Maria"}, {"comment": "Looking good", "user": "John Pope"}],
                "s2": [{"comment": "Hello", "user": "Veronica"}, {"comment": "How are you?", "user": "Peter Brown"}]}

    for user, user_data in users.items():
        u = User.objects.get_or_create(username=user_data["username"])[0]
        u.save()

    for cat, cat_data in cats.items():
        c = add_category(cat, cat_data["total"])
        for l in cat_data["listings"]:
            u = User.objects.get(username=l["user"])
            a = add_listing(l["title"], l["description"], l["price"], c, u, l["date"], l["picture"], l["postcode"])
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


def add_listing(title, description, price, category, user, date, picture, postcode):
    l = Listing.objects.get_or_create(title=title, description=description, price=price, category=category, user=user, date=date, picture=picture, postcode=postcode)[0]
    l.save()
    return l


def add_comment(comment, user, listing):
    co = Comment.objects.get_or_create(comment=comment ,user=user, listing=listing)[0]
    co.save()
    return co


if __name__ == '__main__':
    print("Starting west_end_market population script...")
    populate()
