import models
import peewee
from typing import List

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"

def cheapest_dish() -> models.Dish:
    """You want ot get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    query = (
        models.Dish.select().order_by(models.Dish.price_in_cents).limit(1).first()
    )
    return query


def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """

    vegetarian_dishes = []
    for dish in models.Dish.select():
        ingredient_list = []
        for ingredient in dish.ingredients:
            ingredient_list.append(ingredient.is_vegetarian)
        if all(ingredient_list):
            vegetarian_dishes.append(dish)

    return vegetarian_dishes


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """
    query = (
        models.Restaurant.select(
            models.Restaurant, peewee.fn.AVG(models.Rating.rating)
        )
        .join(models.Rating)
        .group_by(models.Restaurant)
        .order_by(peewee.fn.AVG(models.Rating.rating).desc())
        .first()
    )

    return query


def add_rating_to_restaurant() -> None:
    models.Rating.create(restaurant="Flavortown", rating=2, comment="Heel vies")


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """

    query = (
       models.Restaurant.select()
       .join(models.Dish)
       .join(models.DishIngredient)
       .join(models.Ingredient)
       .group_by(models.Restaurant)
       .where(
           (models.Restaurant.opening_time <= "19:00") & 
           (models.Restaurant.closing_time > "19:00"))
    )

    date_possible = []
    for restaurant in query:
        for dish in restaurant.dish_set.select():
            ingredient_list = []
            for ingredient in dish.ingredients:
                ingredient_list.append(ingredient.is_vegan)
            if all(ingredient_list):
                date_possible.append(restaurant)
    
    for x in date_possible:
        print(x.name)

    return date_possible
        


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    new_ingredient = models.Ingredient.get_or_create(
        name='suiker',
        defaults={
            'is_vegetarian': True,
            'is_vegan': True,
            'is_glutenfree': True,
        }
    )

    kaas = models.Ingredient.get_or_create(
        name='cheese',
        defaults={
            'is_vegetarian': True,
            'is_vegan': False,
            'is_glutenfree': True,
        }
    )

    new_dish = models.Dish.create(
        name="kaasdingen",
        served_at=models.Restaurant.select().first(),
        price_in_cents=3000,
    )

    new_dish.ingredients.add(kaas)
    new_dish.ingredients.add(new_ingredient)

    return new_dish


def main():
    cheapest_dish()
    vegetarian_dishes()
    best_average_rating()
    add_rating_to_restaurant()
    dinner_date_possible()
    add_dish_to_menu()


if __name__ == "__main__":
    main()