from sqlalchemy.orm import Session

from . import models, schemas
from typing import Union

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# def delete_item(db: Session, item_id: int):
#     import pdb; pdb.set_trace()
#     db.query(models.Item).delete(models.Item.id == item_id)
#     # db.delete(items.id)
#     # print(items)
#     # db.commit()
#     # db.refresh()
#     return "success"


def get_item(db: Session, id: int):
    return db.query(models.Item).get(id)


def get_ad(db: Session, id: int):
    return db.query(models.Ad).get(id)


def update_item(db: Session, item: Union[int, models.Item], data: schemas.ItemUpdate):
    if isinstance(item, int):
        item = get_item(db, item)
    if item is None:
      return None
    for key, value in data:
        setattr(item, key, value)
    db.commit()
    return item


def update_ad(db: Session, ad: Union[int, models.Ad], data: schemas.AdUpdate):
    if isinstance(ad, int):
        ad = get_ad(db, ad)
    if ad is None:
      return None
    for key, value in data:
        setattr(ad, key, value)
    db.commit()
    return ad


def drop_item(db: Session, item_id: int):
    import pdb
    db.query(models.Item).filter(models.Item.id == item_id).delete()
    db.commit()
    return None


def drop_ad(db: Session, ad_id: int):
    import pdb
    db.query(models.Ad).filter(models.Ad.id == ad_id).delete()
    db.commit()
    return "successfully deleted"


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # fake_hashed_password = user.password + "notreallyhashed"
    fake_hashed_password = user.password
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, username=user.username, disabled=user.disabled)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_user_ad(db: Session, ad: schemas.AdCreate, user_id: int):
    db_item = models.Ad(**ad.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_ads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ad).offset(skip).limit(limit).all()


