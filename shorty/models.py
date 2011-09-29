# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declared_attr

from shorty import db


class AutoInitModelMixin(object):
    """
    Mixin for populating models' columns automatically (no need to
    define an __init__ method) and set the default value if any.
    Also sets the model's id and __tablename__ automatically.
    """
    id = db.Column(db.Integer, primary_key=True)

    # use the lowercased class name as the __tablename__
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, *args, **kwargs):
        for attr in (a for a in dir(self) if not a.startswith('_')):
            attr_obj = getattr(self, attr)
            if isinstance(attr_obj, db.Column):
                if attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                else:
                    if hasattr(attr_obj, 'default'):
                        setattr(self, attr, attr_obj.default)


class ShortURL(db.Model, AutoInitModelMixin):
    long_url = db.Column(db.String(255), unique=True)
    url_code = db.Column(db.String(32), unique=True) #XXX: is this really needed?
    created = db.Column(db.DateTime)
    clicks = db.relationship("Click")


class Click(db.Model, AutoInitModelMixin):
    url_id = db.Column(db.Integer, db.ForeignKey('shorturl.id'))
    user_agent = db.Column(db.String(255))
    time = db.Column(db.DateTime)
    #TODO: locate originating country/city