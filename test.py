from cerbos.engine.v1.engine_pb2 import Resource
from google.protobuf.struct_pb2 import Value, Struct

a = Resource(
		id=str("3"),
		kind="comment",
		attr={
			"name": Value(string_value="bro"),
			"obj": Value(struct_value={"mehn":"dunno bro"}),
			"somelist": Value(list_value=["fuck this shit man"])
		}
	)




    #  related_model = foreign_key.column.table

    #             attributes[str(related_model.name)] = get_value([column_value]) 


    #             continue


    #             related_key = (related_model.name, column_value)
                
    #             if related_key in foreign_key_cache:
    #                 related_instance = foreign_key_cache[related_key]
    #             else:
    #                 related_instance = db.session.query(related_model).filter(
    #                     foreign_key.column == column_value
    #                 ).first()
    #                 foreign_key_cache[related_key] = related_instance
                
    #             if related_instance:
    #                 related_resources.append(str(related_instance))


# working related instance

def get_resource_from_model(model, instance) -> Resource:
    attributes = {}
    inspector = inspect(model)
    
    for column in model.__table__.c:
        column_value = getattr(instance, column.name)
        
        if column.foreign_keys:
            related_resources = []
            for foreign_key in column.foreign_keys:
                related_model = foreign_key.column.table
                cache_key = (related_model.name, column_value)

                if cache_key in foreign_key_cache:
                    related_instance = foreign_key_cache[cache_key]
                else:
                    related_instance = db.session.query(related_model).filter(
                        foreign_key.column == column_value
                    ).first()
                    foreign_key_cache[cache_key] = related_instance
                
                if related_instance:
                    related_resources.append(str(related_instance))
                    
            attributes[column.name] = get_value(related_resources) if len(related_resources) > 1 else get_value(related_resources[0])
        else:
            attributes[column.name] = get_value(column_value) if column.name == "user_id" else get_value(column_value)

    return Resource(
        id=str(instance.id),
        kind=model.__name__.lower(),
        attr=attributes,
    )