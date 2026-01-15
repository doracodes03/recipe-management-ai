from .models import Recipe

SEED_RECIPES = [
    Recipe(
        name="Chicken Stir Fry",
        ingredients="chicken, onion, garlic, soy sauce",
        instructions="Stir fry chicken with garlic and onion. Add vegetables and soy sauce.",
        cuisine="Asian",
        prep_time=25,
        diet_type="non-veg"
    ),
    Recipe(
        name="Begun Bhaja",
        ingredients="eggplant (aubergine), turmeric powder, chili powder, salt, mustard oil",
        instructions="Slice eggplant, coat with spices, shallow fry until golden.",
        cuisine="Bengali",
        prep_time=10,
        diet_type="vegan"
    ),
    Recipe(
        name="Red Lentil Dahl",
        ingredients="red lentils, coconut milk, turmeric, cumin, spinach",
        instructions="Boil lentils, add spices and coconut milk, simmer gently.",
        cuisine="Indian",
        prep_time=30,
        diet_type="vegan"
    ),
    Recipe(
        name="Classic Margherita Pizza",
        ingredients="pizza dough, tomato sauce, mozzarella, basil leaves",
        instructions="Bake pizza dough with sauce and cheese until crisp.",
        cuisine="Italian",
        prep_time=40,
        diet_type="veg"
    ),
    Recipe(
        name="Lemon Garlic Salmon",
        ingredients="salmon fillets, garlic, butter, lemon juice, asparagus",
        instructions="Pan sear salmon with garlic butter and lemon.",
        cuisine="American",
        prep_time=20,
        diet_type="non-veg"
    ),
    Recipe(
        name="Rajma Chawal",
        ingredients="kidney beans, rice, tomatoes, ginger-garlic paste, garam masala",
        instructions="Cook rajma curry and serve with steamed rice.",
        cuisine="North Indian",
        prep_time=45,
        diet_type="veg"
    ),
    Recipe(
        name="Mediterranean Quinoa Salad",
        ingredients="quinoa, cucumber, cherry tomatoes, feta cheese, olive oil, lemon",
        instructions="Mix cooked quinoa with vegetables and dressing.",
        cuisine="Mediterranean",
        prep_time=15,
        diet_type="veg"
    ),
    Recipe(
        name="Pork Tacos",
        ingredients="pork, taco shells, lettuce, cheddar cheese, salsa",
        instructions="Cook pork with spices and assemble tacos.",
        cuisine="Mexican",
        prep_time=20,
        diet_type="non-veg"
    ),
    Recipe(
        name="Milk Tea",
        ingredients="tea leaves, milk, water, sugar",
        instructions="Boil tea leaves, add milk and sugar, simmer.",
        cuisine="Indian",
        prep_time=10,
        diet_type="veg"
    ),
]
