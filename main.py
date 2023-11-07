import models
import peewee
from typing import List

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def cheapest_dish() -> List[models.Dish]:
    """You want ot get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    query = (
        models.Dish.select().order_by(models.Dish.price_in_cents).limit(1)
    )
    query.execute()

cheapest_dish()

def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """

    query = (
        models.Dish.select()
        .join(models.DishIngredient)
        .join(models.Ingredient)
        .where(models.Ingredient.is_vegetarian == True)
    )

    for dish in query:
        print(dish.name)


# vegetarian_dishes()


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """
    query = (
        models.Restaurant.select()
        .join(models.Rating)
        .order_by(models.Rating).limit(1)
    )

    for restaurant in query:
        print(restaurant.name)

best_average_rating()


def add_rating_to_restaurant() -> None:
    restaurant = models.Restaurant.get(models.Restaurant.name == "Flavortown")
    query = (
        models.Rating.update(rating=3).where(models.Rating.restaurant == restaurant)
    )
    query.execute()
    new_rating = models.Rating.select().where(models.Rating.restaurant == restaurant)
    for rating in new_rating:
        print(rating.rating)

add_rating_to_restaurant()


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """
    ...


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    ...