def get_item(item_id: str, data: list[dict]) -> dict | None:
    for item in data:
        if item["id"] == int(item_id):
            return item
    return None
