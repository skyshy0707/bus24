
def route_wiki_url(value: str):
    if "wikiroutes.info/idea" in value:
        return value
    
    raise ValueError("Invalid route url")

def capacity(value: int):
    if value > 10:
        return value
    raise ValueError(f"Incorrect capacity for bus: {value}")


