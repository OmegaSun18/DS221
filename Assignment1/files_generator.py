#This python file generates test cases for the main.cpp file
import random


#Write a function to create n product names where n is a parameter, and return a list of product names as ints
def generate_product_names(n):
    products = []
    for i in range(n):
        products.append(i)
    return products

#Write a function to create n customer ids, where n is a parameter, and return a list of customer ids. all customer ids are ints, and start from 100
def generate_customer_ids(n):
    customers = []
    for i in range(n):
        customers.append(i + 100)
    return customers

#Write a function to create n hashtag names, where n is a parameter, and return a list of hashtag names as strings
def generate_hashtag_names(n):
    hashtags = []
    for i in range(n):
        hashtags.append("hashtag" + str(i))
    return hashtags

#Write a function to create a list of tuples where each tuple contains a product name followed by a list of hashtags. The number of hashtags for each product is n, where n is a parameter and the hashtags are randomly selected from the list of hashtags
#if n is -1 then the number of hashtags is randomly selected between 2 and 8
#The output should be a list of tuples where each tuple contains a product name and a list of hashtags
#Sample output:
#[(1, ['hashtag1', 'hashtag2']), (2, ['hashtag3', 'hashtag4']), ...]
def generate_product_hashtags(products, hashtags, n):
    product_hashtags = []
    for product in products:
        if n == -1:
            num_hashtags = random.randint(2, 8)
        else:
            num_hashtags = n
        product_hashtags.append((product, random.sample(hashtags, num_hashtags)))
    return product_hashtags

#Write a function to create a list of purchases made by a customer. Each customer buys something once. The total number of purchases is n, where n is a parameter. The products are randomly selected from the list of products. Each entry in the list is a tuple containing the customer id and the product name. The customer ids are randomly selected from the list of customer ids, but each customer id must be present in the final list at least once.
def generate_customer_purchases(customers, products, n):
    customer_purchases = []
    for customer in customers:
        product = random.choice(products)
        customer_purchases.append((customer, product))
    for i in range(n - len(customers)):
        customer = random.choice(customers)
        product = random.choice(products)
        customer_purchases.append((customer, product))
    #Sort the list of tuples by customer id
    customer_purchases.sort(key=lambda x: x[0])
    return customer_purchases


# Write a function to create a csv file with product names and prices. The function takes the parameters product_size and generates a csv file with the following format:
# product_id,product_price
# 1,100
# 2,200
# 3,300
# ...
#The product price is randomly selected between 100 and 1000
def generate_product_prices(product_size, file_name):
    products = generate_product_names(product_size)
    with open(file_name, "w") as file:
        file.write("product_id,product_price\n")
        for product in products:
            file.write(str(product) + "," + str(random.randint(100, 1000)) + "\n")

#write a function that takes in product list, hashtag list, and a parameter n. It creates a new list of length n where each entry is a tuple containing a product name and a hashtag name. The product name is randomly selected from the list of products and the hashtag name is randomly selected from the list of hashtags
def generate_product_hashtag_pairs(products, hashtags, n):
    product_hashtag_pairs = []
    for i in range(n):
        product = random.choice(products)
        hashtag = random.choice(hashtags)
        product_hashtag_pairs.append((product, hashtag))
    return product_hashtag_pairs


#Write a function to create an csv file with the following format:
# customer_id,product_id
# 101,1
# 101,6
# 102,2
# 103,1
# 103,4
# 104,2
# ....
#The function takes the parameters product_size, customer_size, hashtag_size, hashtag_per_product, and purchase_size. The function generates the product names, customer ids, hashtag names, product hashtags, and customer purchases. The function writes the customer purchases to a file named "exp1subexp1pur8customer.csv"
def generate_csv(product_size, customer_size, hashtag_size, hashtag_per_product, purchase_size, file_name):
    products = generate_product_names(product_size)
    customers = generate_customer_ids(customer_size)
    hashtags = generate_hashtag_names(hashtag_size)
    product_hashtags = generate_product_hashtags(products, hashtags, hashtag_per_product)
    customer_purchases = generate_customer_purchases(customers, products, purchase_size)
    #CSV File name should be file_name + customer.csv
    with open(file_name + "customer.csv", "w") as file:
        file.write("customer_id,product_id\n")
        for purchase in customer_purchases:
            file.write(str(purchase[0]) + "," + str(purchase[1]) + "\n")
    #Create another csv file with the product names and hashtags, the file is named "exp1subexp1pur8product.csv"
    #The file format is as follows:
    # product_id,hashtag
    # 1,hashtag1,hashtag2
    # 2,hashtag3,hashtag4
    # ...
    #The csv file name should be file_name + product.csv
    #And it should be sorted by product id
    with open(file_name + "product.csv", "w") as file:
        file.write("product_id,hashtag\n")
        for product in product_hashtags:
            file.write(str(product[0]) + "," + ",".join(product[1]) + "\n")


#Generate the csv files in a folder named "exp1"
#Write a function to generate the csv files in a folder named 'exp' + str(exp_num)
#The function should iterates through experiment number from 1 to 3 and subexperiment number from 1 to 4. The function should generate the csv files for each experiment and subexperiment
#EXPERIMENT 1
#Subexperiment 1: product_size = 5, customer_size = 6, hashtag_size = 10, hashtag_per_product = 2, iterate through purchase_size with values 8, 32, 128, 512, 2048
#Subexperiment 2: product_size = 5, customer_size = 6, hashtag_size = 10, hashtag_per_product = 4, iterate through purchase_size with values 8, 32, 128, 512, 2048
#Subexperiment 3: product_size = 10, customer_size =  6, hashtag_size = 10, hashtag_per_product = 2, iterate through purchase_size with values 8, 32, 128, 512, 2048
#Subexperiment 4: product_size = 10, customer_size =  6, hashtag_size = 10, hashtag_per_product = 4, iterate through purchase_size with values 8, 32, 128, 512, 2048
#EXPERIMENT 2
#Subexperiment 1: product_size = 5, hashtag_size = 10, hashtag_per_product = 2, iterate through customer_size with values 4, 8, 16, 32, 64 and for each customer_size iterate through purchase_size with values 8, 32, 128, 512, 2048. for customer_size = 16 and 32, iterate through purchase_size with values 32, 128, 512, 2048 and for customer_size = 64, iterate through purchase_size with values 128, 512, 2048
#Subexperiment 2: product_size = 5, hashtag_size = 10, hashtag_per_product = 4, iterate through customer_size with values 4, 8, 16, 32, 64 and for each customer_size iterate through purchase_size with values 8, 32, 128, 512, 2048. for customer_size = 16 and 32, iterate through purchase_size with values 32, 128, 512, 2048 and for customer_size = 64, iterate through purchase_size with values 128, 512, 2048
#Subexperiment 3: product_size = 10, hashtag_size = 10, hashtag_per_product = 2, iterate through customer_size with values 4, 8, 16, 32, 64 and for each customer_size iterate through purchase_size with values 8, 32, 128, 512, 2048. for customer_size = 16 and 32, iterate through purchase_size with values 32, 128, 512, 2048 and for customer_size = 64, iterate through purchase_size with values 128, 512, 2048
#Subexperiment 4: product_size = 10, hashtag_size = 10, hashtag_per_product = 4, iterate through customer_size with values 4, 8, 16, 32, 64 and for each customer_size iterate through purchase_size with values 8, 32, 128, 512, 2048. for customer_size = 16 and 32, iterate through purchase_size with values 32, 128, 512, 2048 and for customer_size = 64, iterate through purchase_size with values 128, 512, 2048
#EXPERIMENT 3
#Subexperiment 1: product_size = 5, hashtag_size = 10, hashtag_per_product = -1 (randomize between 2 and 8), iterate through customer_size with values 4, 8, 16, 32, 64 and for each customer_size iterate through purchase_size with values 8, 32, 128, 512, 2048. for customer_size = 16 and 32, iterate through purchase_size with values 32, 128, 512, 2048 and for customer_size = 64, iterate through purchase_size with values 128, 512, 2048
#Subexperiment 2: product_size = 10, hashtag_size = 10, hashtag_per_product = -1 (randomize between 2 and 8), iterate through customer_size with values 4, 8, 16, 32, 64 and for each customer_size iterate through purchase_size with values 8, 32, 128, 512, 2048. for customer_size = 16 and 32, iterate through purchase_size with values 32, 128, 512, 2048 and for customer_size = 64, iterate through purchase_size with values 128, 512, 2048
#Subexperiment 3: product_size = 20, hashtag_size = 10, hashtag_per_product = -1 (randomize between 2 and 8), iterate through customer_size with values 4, 8, 16, 32, 64 and for each customer_size iterate through purchase_size with values 8, 32, 128, 512, 2048. for customer_size = 16 and 32, iterate through purchase_size with values 32, 128, 512, 2048 and for customer_size = 64, iterate through purchase_size with values 128, 512, 2048

def generate_experiments():
    for exp_num in range(1, 6):
        for subexp_num in range(1, 5):
            if exp_num == 1:
                if subexp_num == 1:
                    generate_csv(5, 6, 10, 2, 8, "exp1\subexp1\pur8")
                    generate_csv(5, 6, 10, 2, 32, "exp1\subexp1\pur32")
                    generate_csv(5, 6, 10, 2, 128, "exp1\subexp1\pur128")
                    generate_csv(5, 6, 10, 2, 512, "exp1\subexp1\pur512")
                    generate_csv(5, 6, 10, 2, 2048, "exp1\subexp1\pur2048")
                elif subexp_num == 2:
                    generate_csv(5, 6, 10, 4, 8, "exp1\subexp2\pur8")
                    generate_csv(5, 6, 10, 4, 32, "exp1\subexp2\pur32")
                    generate_csv(5, 6, 10, 4, 128, "exp1\subexp2\pur128")
                    generate_csv(5, 6, 10, 4, 512, "exp1\subexp2\pur512")
                    generate_csv(5, 6, 10, 4, 2048, "exp1\subexp2\pur2048")
                elif subexp_num == 3:
                    generate_csv(10, 6, 10, 2, 8, "exp1\subexp3\pur8")
                    generate_csv(10, 6, 10, 2, 32, "exp1\subexp3\pur32")
                    generate_csv(10, 6, 10, 2, 128, "exp1\subexp3\pur128")
                    generate_csv(10, 6, 10, 2, 512, "exp1\subexp3\pur512")
                    generate_csv(10, 6, 10, 2, 2048, "exp1\subexp3\pur2048")
                elif subexp_num == 4:
                    generate_csv(10, 6, 10, 4, 8, "exp1\subexp4\pur8")
                    generate_csv(10, 6, 10, 4, 32, "exp1\subexp4\pur32")
                    generate_csv(10, 6, 10, 4, 128, "exp1\subexp4\pur128")
                    generate_csv(10, 6, 10, 4, 512, "exp1\subexp4\pur512")
                    generate_csv(10, 6, 10, 4, 2048, "exp1\subexp4\pur2048")
            elif exp_num == 2:
                if subexp_num == 1:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            #Check that purchase size is greater than customer size and generate the csv file
                            if purchase_size >= customer_size:
                                generate_csv(5, customer_size, 10, 2, purchase_size, "exp2\subexp1\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 2:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(5, customer_size, 10, 4, purchase_size, "exp2\subexp2\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 3:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(10, customer_size, 10, 2, purchase_size, "exp2\subexp3\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 4:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(10, customer_size, 10, 4, purchase_size, "exp2\subexp4\customer" + str(customer_size) + "pur" + str(purchase_size))
            elif exp_num == 3:
                if subexp_num == 1:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(5, customer_size, 10, -1, purchase_size, "exp3\subexp1\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 2:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(10, customer_size, 10, -1, purchase_size, "exp3\subexp2\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 3:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(20, customer_size, 10, -1, purchase_size, "exp3\subexp3\customer" + str(customer_size) + "pur" + str(purchase_size))
            elif exp_num == 4:
                #Repeat the same process as eperiment 3
                if subexp_num == 1:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(5, customer_size, 10, -1, purchase_size, "exp4\subexp1\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 2:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(10, customer_size, 10, -1, purchase_size, "exp4\subexp2\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 3:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(20, customer_size, 10, -1, purchase_size, "exp4\subexp3\customer" + str(customer_size) + "pur" + str(purchase_size))
            elif exp_num == 5:
                #Repeat the same process as eperiment 3
                if subexp_num == 1:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(5, customer_size, 10, -1, purchase_size, "exp5\subexp1\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 2:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(10, customer_size, 10, -1, purchase_size, "exp5\subexp2\customer" + str(customer_size) + "pur" + str(purchase_size))
                elif subexp_num == 3:
                    for customer_size in [4, 8, 16, 32, 64]:
                        for purchase_size in [8, 32, 128, 512, 2048]:
                            if purchase_size >= customer_size:
                                generate_csv(20, customer_size, 10, -1, purchase_size, "exp5\subexp3\customer" + str(customer_size) + "pur" + str(purchase_size))
                            

# generate_experiments()

#Write a function to generate the csv files 
def generate_csv_with_newhashtags(product_size, customer_size, hashtag_size, hashtag_per_product, purchase_size, newhashtags_size, file_name):
    products = generate_product_names(product_size)
    customers = generate_customer_ids(customer_size)
    hashtags = generate_hashtag_names(hashtag_size)
    product_hashtags = generate_product_hashtags(products, hashtags, hashtag_per_product)
    customer_purchases = generate_customer_purchases(customers, products, purchase_size)
    newhashtags = generate_product_hashtag_pairs(products, hashtags, newhashtags_size)
    #CSV File name should be file_name + customer.csv
    with open(file_name + "customer.csv", "w") as file:
        file.write("customer_id,product_id\n")
        for purchase in customer_purchases:
            file.write(str(purchase[0]) + "," + str(purchase[1]) + "\n")
    #Create another csv file with the product names and hashtags, the file is named "exp1subexp1pur8product.csv"
    #The file format is as follows:
    # product_id,hashtag
    # 1,hashtag1,hashtag2
    # 2,hashtag3,hashtag4
    # ...
    #The csv file name should be file_name + product.csv
    #And it should be sorted by product id
    with open(file_name + "product.csv", "w") as file:
        file.write("product_id,hashtag\n")
        for product in product_hashtags:
            file.write(str(product[0]) + "," + ",".join(product[1]) + "\n")

    #Create another csv file with the product names and new hashtags, the file is named "exp1subexp1pur8newhashtags.csv"
    #The file format is as follows:
    # product_id,hashtag
    # 1,hashtag1
    # 2,hashtag2
    # ...
    #The csv file name should be file_name + newhashtags.csv
    with open(file_name + "newhashtags.csv", "w") as file:
        file.write("product_id,hashtag\n")
        for newhashtag in newhashtags:
            file.write(str(newhashtag[0]) + "," + newhashtag[1] + "\n")

#Write a function to generate the csv files in a folder names 'exp6'
def generate_experiments_with_newhashtags():
    for subexp_num in range(1, 5):
        #Write the code to generate the csv files for each subexperiment
        if subexp_num == 1:
            generate_csv_with_newhashtags(10, 16, 10, 2, 64, 8, "exp6\subexp1\hash8")
            generate_csv_with_newhashtags(10, 16, 10, 2, 64, 16, "exp6\subexp1\hash16")
            generate_csv_with_newhashtags(10, 16, 10, 2, 64, 32, "exp6\subexp1\hash32")
        elif subexp_num == 2:
            generate_csv_with_newhashtags(20, 16, 10, 2, 64, 8, "exp6\subexp2\hash8")
            generate_csv_with_newhashtags(20, 16, 10, 2, 64, 16, "exp6\subexp2\hash16")
            generate_csv_with_newhashtags(20, 16, 10, 2, 64, 32, "exp6\subexp2\hash32")
        elif subexp_num == 3:
            generate_csv_with_newhashtags(10, 16, 20, 2, 64, 8, "exp6\subexp3\hash8")
            generate_csv_with_newhashtags(10, 16, 20, 2, 64, 16, "exp6\subexp3\hash16")
            generate_csv_with_newhashtags(10, 16, 20, 2, 64, 32, "exp6\subexp3\hash32")
        elif subexp_num == 4:
            generate_csv_with_newhashtags(20, 16, 20, 2, 64, 8, "exp6\subexp4\hash8")
            generate_csv_with_newhashtags(20, 16, 20, 2, 64, 16, "exp6\subexp4\hash16")
            generate_csv_with_newhashtags(20, 16, 20, 2, 64, 32, "exp6\subexp4\hash32")

generate_experiments_with_newhashtags()