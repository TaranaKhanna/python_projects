#Exercise 1

def print_recipe(recipe):

    for i in range(len(recipe)):
        max_key = max(recipe, key=recipe.get)
        print(f"{max_key}: {recipe[max_key]}")
        recipe.pop(max_key)

crepes = {'wheat flour': 250, 'milk': 50, 'egg': 4, 'butter': 50, 'salt': 1}
#print_recipe(crepes)

#Exercise 2

def read_recipe(recipe_file_name):
    recipe_dict = {}
    with open(recipe_file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if(len(line) == 0):     #ignore empty line if any
                continue
            line = line.split(',')

            ingredient = line[0]         #Extract the ingridient from a line as a string
            ingredient = ingredient.strip()
            amount = (line[len(line)-1])
            amount = int(amount)         #Extract the amount from a line as an integer
            if ingredient not in recipe_dict:
                recipe_dict[ingredient] = amount
            else:
                recipe_dict[ingredient] += amount

    return recipe_dict

#print(read_recipe('flan.txt'))
#print(read_recipe('crepes.txt'))

#Exercise 3

def write_recipe(recipe, recipe_fiel_name):
    with open(recipe_fiel_name, 'w') as file:
        for key, value in recipe.items():
            file.write(f"{key}, {value}\n")
    

flan = read_recipe('flan.txt')
#write_recipe(flan, 'flan2.txt')

#Exercise 4

def read_fridge(fridge_file_name):
    fridge_dict = read_recipe(fridge_file_name)

    return fridge_dict

#print(read_fridge('fridge1.txt'))

#Exercise 5

def is_cookable(recipe_file_name, fridge_file_name):
    recipe_requirements = read_recipe(recipe_file_name)
    fridge_items = read_fridge(fridge_file_name)
    flag = 0

    for key in recipe_requirements:
        if key not in fridge_items:
            return False
        if(recipe_requirements[key] <= fridge_items[key]):
            flag += 1
    if flag == len(recipe_requirements):
        return True
    else:
        return False
    
#print(is_cookable('crepes.txt','fridge1.txt'))

#Exercise 6

def add_recipes(recipes):
    for i in range(len(recipes)-1):
        recipe1 = recipes[i]
        recipe2 = recipes[i+1]
        for key in recipe1:
            if key not in recipe2:
                recipe2[key] = recipe1[key]
            else:
                recipe2[key] += recipe1[key]
    return recipe2
#print(add_recipes([read_recipe('crepes.txt'), read_recipe('flan.txt')]))

#Exercise 7

def create_shopping_list(recipe_file_names, fridge_file_name):
    recipe = []
    for i in range(len(recipe_file_names)):
        current_recipe = read_recipe(recipe_file_names[i])
        recipe.append(current_recipe)

    combined_recipe = add_recipes(recipe)       # a dictionary containing all ingredients and their amounts from all recipe files
    fridge_items = read_fridge(fridge_file_name)     # a dictionary containing all ingredients present in the fridge with their amounts

    shhopping_list = {}
    for key, value in combined_recipe.items():
        if (key not in fridge_items):
            shhopping_list[key] = value
        elif (value > fridge_items[key]):
            shhopping_list[key] = (value - fridge_items[key])
    return shhopping_list


#print(create_shopping_list(['crepes.txt', 'flan.txt'], 'fridge1.txt'))

#Exercise 8

def total_price(shopping_list, market_file_name):
    price = 0
    market_items = read_recipe(market_file_name)        # a dictionary containg all ingredients in the givne market with their amounts
    for ingredient, amount in shopping_list.items():
        price += market_items[ingredient]*amount 
    return price
        
todays_menu = ['crepes.txt', 'flan.txt', 'madeleines.txt']
what_we_need = create_shopping_list(todays_menu, 'fridge1.txt')

#print(total_price(what_we_need, 'market1.txt'))

#Exercise 9

def find_cheapest(shopping_list, market_file_names):
    lowest_price_market = ''
    lowest_price = 0
    for i in range(len(market_file_names)-1):
        market1_price = total_price(shopping_list, market_file_names[i])
        market2_price = total_price(shopping_list, market_file_names[i+1])
        if market1_price <= market2_price:
            lowest_price_market = market_file_names[i] 
            lowest_price = market1_price
        else:
            lowest_price_market = market_file_names[i+1]
            lowest_price = market2_price
    market_with_lowest_price = (lowest_price_market,) + (lowest_price,)
   
    return market_with_lowest_price

supermarkets = ['market1.txt', 'market2.txt', 'market3.txt']
#print(find_cheapest(what_we_need, supermarkets))

#Exercise 10


def update_fridge(fridge_file_name, recipe_file_names, market_file_names, new_fridge_file_name):
    shopping_list = create_shopping_list(todays_menu, fridge_file_name)     # a dictionary for shopping list
    
    for ingredient, amount in shopping_list.items():
        print(f"{ingredient}: {amount}")        # prints each ingredient and its amount from shopping list

    cheapest_market = find_cheapest(shopping_list, supermarkets)        # a tuple with cheapest market recomdation with total shopping cost
    print(f'market: {cheapest_market[0]}')
    print(f'Total cost: {cheapest_market[1]}')

    fridge_items_list = read_fridge(fridge_file_name)  # a dictionary for available items in the given fridge

    fridge_items_newlist = add_recipes([shopping_list, fridge_items_list])  # adds the bought items (with quantity) with the available fridge items 

    new_fridge_data = write_recipe(fridge_items_newlist, new_fridge_file_name)      # writes the updated fridge content to new fridge
    

#update_fridge('fridge1.txt', todays_menu, supermarkets, 'fridge_new.txt')