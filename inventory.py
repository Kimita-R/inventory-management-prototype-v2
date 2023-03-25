from tabulate import tabulate
#========The beginning of the class==========

# Definition of Shoe Class 
class Shoe:

    # Initialise a new instance of the Shoe Class
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Return the cost of the shoe
    def get_cost(self):
        return int(self.cost)

    # Return the stock quantity of the shoe   
    def get_quantity(self):
       return int(self.quantity)

    # Return a string representation of the shoe
    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


#=============Shoe list===========
# Store list of shoes
shoe_list = []

#==========Functions outside the class==============

# Read shoe data stored in inventory.txt file
def read_shoes_data():
    

    try:
        with open("inventory.txt", "r") as file:
            #Skip the first line of the file - as this is the file header and contains no shoe data
            next(file)

            # Iterate through each line in the file
            for line in file:
                
                # For each line split the line string by ","
                # Since the format of the file is known we can split the string into the variables needed to initialise a new Shoe object
                # i.e. Country, Code, Product, Cost and Quantity
                country, code, product, cost, quantity = line.split(",")

                # Create a new instance of Shoe and add to the shoe_list
                shoe_list.append(Shoe(country.strip(),code.strip(),product.strip(),cost.strip(),quantity.strip()))
                
        return True

    # Error handling - show error if no valid file is found
    except FileNotFoundError as e:
        print(f"File Not Found - {e}")
        return False


# Capture data of a new shoe and append to the shoe_list
def capture_shoes():

    # Get data from user input of new shoe
    print("To capture a new shoe please enter the following information: ")
    product_name = input("Product Name: ")

    # Product SKU should be unique - in order to search for shoes
    # Variables for unique code checks 
    is_product_code_unique = False 
    duplicate_code = 0

    # Run loop until a unique code is entered
    while is_product_code_unique == False:

        product_code = input("Product Code: ")

        # Iterate through shoe_list and check that code is unique
        # If not display error message, break out of loop and ask user to reenter a SKU code
        for shoe in shoe_list:
            duplicate_code = 0
            if product_code == shoe.code:
                duplicate_code += 1 
                print("The product code you entered already exists - please enter a unique SKU code")
                break
        
        # If code is unique - set is_product_code_unique to True and end loop
        if duplicate_code == 0:
            is_product_code_unique = True

   
    cost = input("Cost Price: ")
    stock_quantity = input("Stock Quantity: ")
    country = input("Country: ")

    # Create a new instance of Shoe and append to the shoe_list
    shoe_list.append(Shoe(country, product_code, product_name, cost, stock_quantity))


    # Write the updated shoe list to the inventory file
    with open("inventory.txt", "w") as file:

        #Skip the first line of the file - as this is the file header, do not overwrite
        file.write(f"Country,Code,Product,Cost,Quantity\n")

        for shoe in shoe_list:
            file.write(f"{shoe.__str__()}\n")

    print("==== NEW SHOE SUCCESSFULLY ADDED ==== ")



# Print all shoes in the shoe_list
def view_all():

    #Create empty list table - to hold the data for the display table
    table = []

    #Iterate through shoe_list
    for shoe in shoe_list:

        # For each shoe in shoe_list use the __str__ method to get the string representation of the Shoe
        # Split the string by "," and store in a list shoe_param
        shoe_param = shoe.__str__().split(",")

        # Add each new shoe_param to the table list - i.e. to create a list of lists
        table.append(shoe_param)
        
    # Use the tabulate method to print a summary table of all shoes in the shoe_list
    print(tabulate(table, headers=["Country","Code", "Product", "Cost", "Quantity"]))


# View and restock shoe in shoe_list with the lowest quantity
def re_stock():

    # Initialise stock_quantity to the quantity value of the first shoe in shoe_list
    stock_quantity = int(shoe_list[0].quantity)

    # Initialise variable restock_item - as a holder for the shoe object with the lowest stock quantity
    restock_item = None

    #Iterate through shoe_list
    for shoe in shoe_list:

        # If stock_quantity is greater than the quantity of shoe
        # stock_quantity is replaced by current shoe quantity
        # Update the restock_item with this shoe
        if stock_quantity > int(shoe.quantity):
            stock_quantity = int(shoe.quantity)
            restock_item = shoe
    

    # Display shoe with the lowest stock and its corresponding stock quantity
    # Give the user the option to restock the shoe
    print(f'''Would you like to restock {restock_item.product}, location: {restock_item.country}, current stock: {restock_item.quantity}? ''')
    user_selection = input(f'''
    1 - Yes
    2 - No
    ''')

    # If user chooses to restock item 
    if user_selection == "1":

        # Get the restock quantity from the user
        restock_quantity = int(input("Please enter the restock quantity: "))

        
        # Interate through shoe_list
        for shoe in shoe_list:
            if restock_item.code == shoe.code:
                shoe.quantity = str(int(shoe.quantity) + restock_quantity)
            
        with open("inventory.txt", "w") as file:

            #Skip the first line of the file - as this is the file header, do not overwrite
            file.write(f"Country,Code,Product,Cost,Quantity\n")

            for shoe in shoe_list:
                file.write(f"{shoe.__str__()}\n")

        print("===== NEW STOCK SUCCESSFULLY ADDED =====")
            
    # If user selects 'No' do nothing and return to main menu
    elif user_selection == "2":
        pass


# Search for shoe using shoe code
def search_shoe():

    # Variable to store shoe with matching code
    matching_shoe = None

    # Ask user to input a code until a matching product is found
    while matching_shoe == None:

        # Get user to enter a shoe code
        user_input = input("Please enter the product code: ")
    
        #Iterate through shoe list
        for shoe in shoe_list:

            # If shoe.code == user_input matching shoe has been found
            # Set matching_shoe to current shoe in for loop
            # Print shoe details to user
            if shoe.code == user_input:
                matching_shoe = shoe.__str__().split(",")
                print(f'''
                ===== Product Details =====
                Country: {matching_shoe[0]}
                Code: {matching_shoe[1]}
                Product: {matching_shoe[2]}
                Cost: {matching_shoe[3]}
                Quantity: {matching_shoe[4]}''')
                break
        
        # If no product code is invalid/not found display error and ask user to re-enter code
        if matching_shoe == None:
            print("ERROR - Product code not found. Please try again")
        

# Display current stock value of each shoe in shoe_list
def value_per_item():

    # List table to store shoe display data
    table = []

    # Iterate through shoe list
    for shoe in shoe_list:
        # Split each string so that stock value can be added to shoe_param list
        shoe_param = shoe.__str__().split(",")

        # Calculate stock value of shoe
        shoe_value = shoe.get_quantity() * shoe.get_cost()

        # Add shoe_value to shoe_param list and add shoe_param to table list
        shoe_param.append(str(shoe_value))
        table.append(shoe_param)
        

    # Print table summary of the stock value of each shoe
    print(f"===== STOCK VALUE PER ITEM =====")
    print(tabulate(table, headers=["Country","Code", "Product", "Cost", "Quantity", "Stock Value"]))


# Display shoe with the highest stock quantity
def highest_qty():

    # Set stock_quantity to the quantity of the first shoe in shoe_list
    stock_quantity = int(shoe_list[0].quantity)

    # Store the shoe with the highest stock quantity
    sale_item = None

    # Iterate through shoe_list
    for shoe in shoe_list:

        #If stock_quantity is < than shoe.quantity
        # stock_quantity is set to shoe.quantity
        # update sale_item to shoe
        if stock_quantity < int(shoe.quantity):
            stock_quantity = int(shoe.quantity)
            sale_item = shoe

 
    # Print the item details of the product marked for sale
    shoe_details = sale_item.__str__().split(",")
    print(f'''
        ===== ITEM MARKED FOR SALE =====
        Country: {shoe_details[0]}
        Code: {shoe_details[1]}
        Product: {shoe_details[2]}
        Cost: {shoe_details[3]}
        Quantity: {shoe_details[4]}''')
 
  

#==========Main Menu=============

file_successfully_read = read_shoes_data() 

menu_selection = ""
while menu_selection != "0" and file_successfully_read == True:

    menu_selection = input(f'''
===== MAIN MENU =====
Select an option below:
1 - Add new shoe
2 - View All Stock
3 - Restock
4 - Search for item
5 - Stock Value per item
6 - Sale items
0 - Quit
''')

    # Allow user to enter data and add new shoe to shoe_list
    if menu_selection == "1":
        capture_shoes()
    
    # View all stock
    elif menu_selection == "2":
        view_all()

    # View and restock shoe with lowest quanity
    elif menu_selection == "3":
        re_stock()

    # Search for shoe using product code
    elif menu_selection == "4":
        search_shoe()

    # View stock value per shoe
    elif menu_selection == "5":
        value_per_item()

    # Show shoe with the highest quantity and mark for sale
    elif menu_selection == "6":
        highest_qty()

    # Quit program 
    elif menu_selection == "0":
        quit()
    
    # Print error message if user enters an invalid option
    else: 
        print("Oops, invalid selection, please try again.")
   





