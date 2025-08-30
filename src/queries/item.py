from ..models.Item import Item
from ..app import get_session

from sqlalchemy import select

"""
All database interfacing for the Image table should be down through these functions.

@param id: the id of the requested image
@param title/new_title: A string representing the new title (MAX: 32 chars)
@param price/new_price: A floating point number representinv the price of the item
@param img/new_img: A string representing the full path from project root to the image (MAX: 255 chars)


"""

def get_items():
    with get_session().begin() as s:
        stmt = select(Item)
        items = s.scalars(stmt).all()
    return items

def create_item(title: str, img: str, price: float):
    with get_session().begin() as s:
        a = Item(title=title, img=img, price=price)
        s.add(a)

def delete_item(id: int):
    with get_session().begin() as s:
        item = s.get(Item, id)

        if not item:
            raise ValueError("No such item exists")

        s.delete(item)

def edit_item_price(id: int, new_price: float):
    with get_session().begin() as s:
        item = s.get(Item, id)

        if not item:
            raise ValueError("No such item exists")

        item.price = new_price
        
def edit_item_title(id: int, new_title: str):
    with get_session().begin() as s:
        item = s.get(Item, id)

        if not item:
            raise ValueError("No such item exists")

        item.title = new_title

def edit_item_img(id: int, new_img: str):
    with get_session().begin() as s:
        item = s.get(Item, id)

        if not item:
            raise ValueError("No such item exists")

        item.img = new_img

