def choices_to_objects(choices: iter):
    
    return [
        {
            "id": key,
            "value": key, 
            "label": value
        } for key, value in choices
    ]

def to_data_obj(data: dict):
    return type("Data", (), data)