from tabulate import tabulate
#========The beginning of the class==========

# Definition of product Class 
class Product:

    # Initialise a new instance of the product Class
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Return the cost of the product
    def get_cost(self):
        return int(self.cost)

    # Return the stock quantity of the product   
    def get_quantity(self):
       return int(self.quantity)

    # Return a string representation of the product
    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


#=============Product list===========
# Store list of products
product_list = []

#==========Functions outside the class==============

# Read product data stored in inventory.txt file
def read_products_data():
    

    try:
        with open("inventory.txt", "r") as file:
            #Skip the first line of the file - as this is the file header and contains no product data
            next(file)

            # Iterate through each line in the file
            for line in file:
                
                # For each line split the line string by ","
                # Since the format of the file is known we can split the string into the variables needed to initialise a new Product object
                # i.e. Country, Code, Product, Cost and Quantity
                country, code, product, cost, quantity = line.split(",")

                # Create a new instance of Product and add to the product_list
                product_list.append(Product(country.strip(),code.strip(),product.strip(),cost.strip(),quantity.strip()))
                
        return True

    # Error handling - show error if no valid file is found
    except FileNotFoundError as e:
        print(f"File Not Found - {e}")
        return False


# Capture data of a new product and append to the product_list
def capture_products():

    # Get data from user input of new product
    print("To capture a new product please enter the following information: ")
    product_name = input("Product Name: ")

    # Product SKU should be unique - in order to search for products
    # Variables for unique code checks 
    is_product_code_unique = False 
    duplicate_code = 0

    # Run loop until a unique code is entered
    while is_product_code_unique == False:

        product_code = input("Product Code: ")

        # Iterate through product_list and check that code is unique
        # If not display error message, break out of loop and ask user to reenter a SKU code
        for product in product_list:
            duplicate_code = 0
            if product_code == product.code:
                duplicate_code += 1 
                print("The product code you entered already exists - please enter a unique SKU code")
                break
        
        # If code is unique - set is_product_code_unique to True and end loop
        if duplicate_code == 0:
            is_product_code_unique = True

   
    cost = input("Cost Price: ")
    stock_quantity = input("Stock Quantity: ")
    country = input("Country: ")

    # Create a new instance of Product and append to the product_list
    product_list.append(Product(country, product_code, product_name, cost, stock_quantity))


    # Write the updated product list to the inventory file
    with open("inventory.txt", "w") as file:

        #Skip the first line of the file - as this is the file header, do not overwrite
        file.write(f"Country,Code,Product,Cost,Quantity\n")

        for product in product_list:
            file.write(f"{product.__str__()}\n")

    print("==== NEW SHOE SUCCESSFULLY ADDED ==== ")



# Print all products in the product_list
def view_all():

    #Create empty list table - to hold the data for the display table
    table = []

    #Iterate through product_list
    for product in product_list:

        # For each product in product_list use the __str__ method to get the string representation of the Product
        # Split the string by "," and store in a list product_param
        product_param = product.__str__().split(",")

        # Add each new product_param to the table list - i.e. to create a list of lists
        table.append(product_param)
        
    # Use the tabulate method to print a summary table of all products in the product_list
    print(tabulate(table, headers=["Country","Code", "Product", "Cost", "Quantity"]))


# View and restock product in product_list with the lowest quantity
def re_stock():

    # Initialise stock_quantity to the quantity value of the first product in product_list
    stock_quantity = int(product_list[0].quantity)

    # Initialise variable restock_item - as a holder for the product object with the lowest stock quantity
    restock_item = None

    #Iterate through product_list
    for product in product_list:

        # If stock_quantity is greater than the quantity of product
        # stock_quantity is replaced by current product quantity
        # Update the restock_item with this product
        if stock_quantity > int(product.quantity):
            stock_quantity = int(product.quantity)
            restock_item = product
    

    # Display product with the lowest stock and its corresponding stock quantity
    # Give the user the option to restock the product
    print(f'''Would you like to restock {restock_item.product}, location: {restock_item.country}, current stock: {restock_item.quantity}? ''')
    user_selection = input(f'''
    1 - Yes
    2 - No
    ''')

    # If user chooses to restock item 
    if user_selection == "1":

        # Get the restock quantity from the user
        restock_quantity = int(input("Please enter the restock quantity: "))

        
        # Interate through product_list
        for product in product_list:
            if restock_item.code == product.code:
                product.quantity = str(int(product.quantity) + restock_quantity)
            
        with open("inventory.txt", "w") as file:

            #Skip the first line of the file - as this is the file header, do not overwrite
            file.write(f"Country,Code,Product,Cost,Quantity\n")

            for product in product_list:
                file.write(f"{product.__str__()}\n")

        print("===== NEW STOCK SUCCESSFULLY ADDED =====")
            
    # If user selects 'No' do nothing and return to main menu
    elif user_selection == "2":
        pass


# Search for product using product code
def search_product():

    # Variable to store product with matching code
    matching_product = None

    # Ask user to input a code until a matching product is found
    while matching_product == None:

        # Get user to enter a product code
        user_input = input("Please enter the product code: ")
    
        #Iterate through product list
        for product in product_list:

            # If product.code == user_input matching product has been found
            # Set matching_product to current product in for loop
            # Print product details to user
            if product.code == user_input:
                matching_product = product.__str__().split(",")
                print(f'''
                ===== Product Details =====
                Country: {matching_product[0]}
                Code: {matching_product[1]}
                Product: {matching_product[2]}
                Cost: {matching_product[3]}
                Quantity: {matching_product[4]}''')
                break
        
        # If no product code is invalid/not found display error and ask user to re-enter code
        if matching_product == None:
            print("ERROR - Product code not found. Please try again")
        

# Display current stock value of each product in product_list
def value_per_item():

    # List table to store product display data
    table = []

    # Iterate through product list
    for product in product_list:
        # Split each string so that stock value can be added to product_param list
        product_param = product.__str__().split(",")

        # Calculate stock value of product
        product_value = product.get_quantity() * product.get_cost()

        # Add product_value to product_param list and add product_param to table list
        product_param.append(str(product_value))
        table.append(product_param)
        

    # Print table summary of the stock value of each product
    print(f"===== STOCK VALUE PER ITEM =====")
    print(tabulate(table, headers=["Country","Code", "Product", "Cost", "Quantity", "Stock Value"]))


# Display product with the highest stock quantity
def highest_qty():

    # Set stock_quantity to the quantity of the first product in product_list
    stock_quantity = int(product_list[0].quantity)

    # Store the product with the highest stock quantity
    sale_item = None

    # Iterate through product_list
    for product in product_list:

        #If stock_quantity is < than product.quantity
        # stock_quantity is set to product.quantity
        # update sale_item to product
        if stock_quantity < int(product.quantity):
            stock_quantity = int(product.quantity)
            sale_item = product

 
    # Print the item details of the product marked for sale
    product_details = sale_item.__str__().split(",")
    print(f'''
        ===== ITEM MARKED FOR SALE =====
        Country: {product_details[0]}
        Code: {product_details[1]}
        Product: {product_details[2]}
        Cost: {product_details[3]}
        Quantity: {product_details[4]}''')
    
    # Allow the user to change the price of an item marked for sale
    change_price = input(" Would you like to mark down this item for sale ? Yes/No: ").lower()
    if change_price == 'yes':
        new_price = input("Please enter the new price: ")
        
        for index, product in enumerate(product_list):
        #for product in product_list:
            if product == sale_item: 
                product_list[index] = Product(product_details[0],product_details[1],product_details[2],new_price,product_details[4])
                print(f"product - {product}") 
                print(f"sale_item - {sale_item}") 

        # Write the updated product list to the inventory file
        with open("inventory.txt", "w") as file:

            #Skip the first line of the file - as this is the file header, do not overwrite
            file.write(f"Country,Code,Product,Cost,Quantity\n")

            for product in product_list:
                file.write(f"{product.__str__()}\n")
  

#==========Main Menu=============

file_successfully_read = read_products_data() 

menu_selection = ""
while menu_selection != "0" and file_successfully_read == True:

    menu_selection = input(f'''
===== MAIN MENU =====
Select an option below:
1 - Add new product
2 - View All Stock
3 - Restock
4 - Search for item
5 - Stock Value per item
6 - Sale items
0 - Quit
''')

    # Allow user to enter data and add new product to product_list
    if menu_selection == "1":
        capture_products()
    
    # View all stock
    elif menu_selection == "2":
        view_all()

    # View and restock product with lowest quanity
    elif menu_selection == "3":
        re_stock()

    # Search for product using product code
    elif menu_selection == "4":
        search_product()

    # View stock value per product
    elif menu_selection == "5":
        value_per_item()

    # Show product with the highest quantity and mark for sale
    elif menu_selection == "6":
        highest_qty()

    # Quit program 
    elif menu_selection == "0":
        quit()
    
    # Print error message if user enters an invalid option
    else: 
        print("Oops, invalid selection, please try again.")
   





