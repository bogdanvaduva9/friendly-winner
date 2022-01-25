import json
from dataclasses import dataclass


@dataclass
class RatingObject:
    text: str = None
    rating: int = None
    rating_id: int = None

    def __repr__(self):
        return f"{self.text}\n{self.rating}\n{self.rating_id}"


def create_ratings(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        content = json_file.read()

    train_json = json.loads(content)
    ratings = []
    for item in train_json:
        rating = RatingObject(text=item.get('text', ""),
                              rating_id=item.get('id', -1),
                              rating=item.get('rating', -1))
        ratings.append(rating)

    return ratings
