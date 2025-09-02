from ..models.Item import Item
from ..utils.validation import inputs_exist

from sqlalchemy import select

"""
All database interfacing for the Image table should be down through these functions.

@param id: the id of the requested image
@param title/new_title: A string representing the new title (MAX: 32 chars)
@param price/new_price: A floating point number representinv the price of the item
@param img/new_img: A string representing the full path from project root to the image (MAX: 255 chars)

All function can through ValueError

"""

def get_items(session):
    inputs_exist(session)
    with session() as s:
        with s.begin():
            stmt = select(Item)
            items = s.scalars(stmt).all()
    return items

def get_item(session, id: int):
    inputs_exist(session, id)
    with session() as s:
        with s.begin():
            stmt = select(Item).filter_by(id=id)
            item = s.scalar(stmt)

    if not item:
        raise ValueError("Item doesn't exist")

    return item

def isitem(session, id: int):
    inputs_exist(session, id)
    with session() as s:
        with s.begin():
            stmt = select(Item).filter_by(id=id)
            item = s.scalar(stmt)

    return bool(item)

def create_item(session, title: str, img: str, price: float, stock: int):
    inputs_exist(session, title, img, price)
    with session() as s:
        with s.begin():
            a = Item(title=title, img=img, price=price, stock=stock)
            s.add(a)

def delete_item(session, id: int):
    inputs_exist(session, id)
    with session() as s:
        with s.begin():
            item = s.get(Item, id)

            if not item:
                raise ValueError("No such item exists")

            s.delete(item)

def edit_item_price(session, id: int, new_price: float):
    inputs_exist(session, id, new_price)
    with session() as s:
        with s.begin():
            item = s.get(Item, id)

            if not item:
                raise ValueError("No such item exists")

            item.price = new_price
        
def edit_item_title(session, id: int, new_title: str):
    inputs_exist(session, id, new_title)
    with session() as s:
        with s.begin():
            item = s.get(Item, id)

            if not item:
                raise ValueError("No such item exists")

            item.title = new_title

def edit_item_stock(session, id: int, new_stock: int):
    inputs_exist(session, id, new_stock)
    with session() as s:
        with s.begin():
            item = s.get(Item, id)

            if not item:
                raise ValueError("No such item exists")

            item.stock = new_stock

def edit_item_img(session, id: int, new_img: str):
    inputs_exist(session, id, new_img)
    with session() as s:
        with s.begin():
            item = s.get(Item, id)

            if not item:
                raise ValueError("No such item exists")

            item.img = new_img

