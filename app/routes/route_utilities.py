from flask import abort, make_response, request
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model: 
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model

def add_model(cls, model_data):
    try: 
        model = cls.from_dict(model_data)
    except KeyError as e:
        response = {"message": f"Invalid data: missing key {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(model)
    db.session.commit()

    return model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    
    query = db.select(cls)

    if filters: 
        for key, value in filters.items():
            if hasattr(cls, key):
                query = query.where(getattr(cls,key).ilike(f"%{value}%"))

    query = query.order_by(cls.id)
    models = db.session.scalars(query)
    response = [model.to_dict() for model in models]

    return response


# class Cat:
#     name = "Meoward"
#     age = 12
#     fur_length = "short"

# attribute_list = ["name", "fur_length", "meow_volume"]

# def has_all_attributes(cls, attributes):
#     for attribute in attributes:
#         if not hasattr(cls, attribute):
#             return False

#     return True

# # The statement below will print `False` since `Cat`
# # does not contain the attribute `meow_volume`
# print(has_all_attributes(Cat, attribute_list)) 
# print(hasattr(Cat, "name") )
# print(getattr(Cat,"name"))
