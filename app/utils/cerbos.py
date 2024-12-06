import datetime
from flask import g
from sqlalchemy.inspection import inspect
from cerbos.engine.v1.engine_pb2 import Resource
from cerbos.sdk.grpc.client import CerbosClient
from google.protobuf.struct_pb2 import Value, Struct
from cerbos.engine.v1.engine_pb2 import Principal
from app.extensions import db
from sqlalchemy.orm import joinedload

def get_value(v):
    if isinstance(v, str):
        return Value(string_value=v)
    elif isinstance(v, bool):
        return Value(bool_value=v)
    elif isinstance(v, (int, float)):
        return Value(number_value=v)
    elif isinstance(v, datetime.datetime):
        return Value(number_value=v.timestamp())
    elif hasattr(v, "__dict__"): 
        obj_struct = Struct()
        for key, value in inspect(v).attrs.items():
            obj_struct[key] = get_value(value.value)
        return Value(struct_value=obj_struct)
    elif isinstance(v, dict):
        return Value(struct_value=v)
    elif isinstance(v, list):
        return Value(list_value=v)
    return Value(null_value=Value.NULL_VALUE)


def get_principal(user) -> Principal:
    return Principal(
        id=str(user.id),
        roles={str("admin" if user.is_admin else "user")},
    )

def get_resource_from_model(model, instance) -> Resource:
    attributes = dict()

    def get_related_attributes(related_instance):
        related_attributes = {}
        for key in related_instance.__table__.c:
            key = str(key).split(".")[1]
            try:
                related_attributes[key] = getattr(related_instance, str(key))
            except:
                continue
        return get_value(related_attributes)

    for n in model.__table__.c:
        if n.name == "user_id" and instance.user:
            attributes["user"] = get_related_attributes(instance.user)
        elif n.name == "post_id" and instance.post:
            attributes["post"] = get_related_attributes(instance.post)
        else:
            attributes[n.name] = get_value(getattr(instance, n.name))

    return Resource(
        id=str(instance.id),
        kind=model.__name__.lower(),
        attr=attributes,
    )


def check_permission(action, model, instance):
    """Helper function to check permissions with Cerbos for any model."""
    resource = get_resource_from_model(model, instance)

    print(resource)
    
    with CerbosClient("localhost:3593") as c:
        principal = get_principal(g.user)

        return c.is_allowed(action, principal, resource)

def check_permission_for_resource(action, resource):
    principal = get_principal(g.user)

    with CerbosClient("localhost:3593") as c:
        return c.is_allowed(action, principal, resource)
    