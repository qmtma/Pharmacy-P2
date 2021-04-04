

#  writing string to the file
import csv


def write_function(file_name , str_info):
    out = open(file_name, "a")
    out.write(str_info + '\n')
    out.close()
 
 # display medicines which have a quantity less than a given quantity
def display_medicines_per_qty(file_name, q):
    print("\nMedicines with available stock less than", q, ":")
    count = 0
    lines = read_file(file_name)
    for record in lines:
        record_list = record.strip().split(";")        
        base_qty = int(record_list[4])  # all the qty at index 4
        sold_qty = int(record_list[5]) # sold qty at index 5
        # Existing Quantity = all quantity - sold quantity
        Existing_qty = base_qty - sold_qty
        if Existing_qty < q:            
            # Display the Medicine that match condition
            print_medicine(record_list)
            count = count + 1
     
    if count == 0:
        # display a message when no product to show
        print(" -- No quantities less than ", q)

# display medicines which expir at next given number of months
def list_medicines_per_expiry(file_name, months_to_expir): 
    import datetime
    long_date = datetime.datetime.now() 
    print("\nProducts which expire within next", months_to_expir,"months:")
    count = 0 
    lines = read_file(file_name)
    for line in lines:
        record_list = line.strip().split(";")
        # retrieve current year        
        current_Year = long_date.year
        current_month = int(long_date.strftime("%m"))
        # retrieve the month & year from expiry date field
        ex_month = int(record_list[6][2:4])
        ex_year  = int(record_list[6][4:])

        if ex_year == current_Year:
            # param (month_num) is the month that at it the checked period ends
            month_num = current_month + months_to_expir
            if ex_month >=current_month and ex_month <= (month_num):
                print_medicine(record_list)
                count = count + 1
     
    if count == 0:
        # display a message when no product to show
        print(" -- No Medicines expire in next", months_to_expir, "months.")

# read inventory lines
def read_file(file_name):
    import os
    lines = []
    if os.path.exists(file_name):
        input_file = open(file_name,'r')
        # (enumerate function): read all lines and make a list of them
        for c , line in enumerate(input_file):
            c = 0
            lines.append(line)
        input_file.close()
    else:
        print("Error! the file not exist.")
    return lines

# Display medicine/Product information
def print_medicine(line_list):
    str = ""
    for x in line_list:
        if str == "":
            str = x
        else:
            str = str + "\t " + x
    print(str)

# printing the menu driven
def display_menu():
    print("\n")
    print("1-) Adding to the inventory")
    print("2-) List the inventory")
    print("3-) Update the inventory")    
    print("4-) Search and delete")
    print("5-) Billing")
    print("6-) Total sales display in histogram")
    print("7-) Exit the program\n")

# Update inventory function definition
def updateInventory(Med_ID):
    # TIP: keep this data visualization in mind
    # the next line shows a list of lists, for this program, each list inside the list is referred to as a row THUS:
    # [[2,PA1,Panadol,11.0,15,32,27102021],[1,AU3,Augmenting,34.0,167,98,01092021]]
    # (1,AU3,Augmenting,34.0,167,98,01092021) is a row and each element has an index, so row[0] corresponds to Type,.etc

    with open('inventory.txt') as csvFile:
        # opens inventory.txt for read, and runs the segment if it was opened successfully
        dataSelect = csv.reader(csvFile, delimiter=',') # dataSelect holds csv file data, in an array like type
        List = list(dataSelect) # force change data type into a list (results in a list of lists aka 2D array)
        for row in List: # looping through each dimention
            if row[1] == Med_ID: # if Med ID is found
                # print relevant data for user confirmation
                print(f" Type : {row[0]}\n ID : {row[1]}\n Name :{row[2]}\n Price : {row[3]}\n quantity : {row[4]}\n quantity sold :{row[5]}\n Expiry Date : {row[6]} ")
                print("Which value you are willing to edit?  (Select a number)")
                print("1. quantity")
                print("2. Expiry Date")
                choice = input()
                if choice == "1":
                    print("Enter New quantiry")
                    NewQuantity = input()
                    row[4] = NewQuantity # updates quantity value in the list
                    writeObject = csv.writer(open("inventory.txt","w", newline='')) # opens inventory.txt as write file
                    writeObject.writerows(List) # writes the Updated List into inventory.txt file
                if choice == "2":
                    print("Enter New Date without any separators")
                    NewDate = input()
                    row[6] = NewDate
                    writeObject = csv.writer(open("inventory.txt", "w", newline=''))
                    writeObject.writerows(List)
        csvFile.close()


    pass

# search and delete function definition
def searchAndDelete(medID, medType):
    # following the same method in UpdateInventory function
    with open("inventory.txt") as csvFile:
        dataMed = csv.reader(csvFile, delimiter=',')
        List = list(dataMed)
        for row in List:
            if row[0] == medType and row[1] == medID: # find a row which has bot Type & ID values equal to user input
                print("MED found")
                print(f" Type : {row[0]}\n ID : {row[1]}\n Name :{row[2]}\n Price : {row[3]}\n quantity : {row[4]}\n quantity sold :{row[5]}\n Expiry Date : {row[6]} ")
                print("are you sure you want to delete the data above? (y/n)")
                answer = input()
                if answer == 'y' or answer == 'Y':
                    rowIndex = List.index(row)
                    List.pop(rowIndex)
                    writeObject = csv.writer(open("inventory.txt", "w", newline=''))
                    writeObject.writerows(List)
                else: pass

    pass


def billing():
    print("Choose the Medicine")
    with open("inventory.txt") as csvFile:
        dataMed = csv.reader(csvFile, delimiter=',')
        List = list(dataMed)
        for row in List: # a loop through all the list printing ID,Price,quantity available of all products
            print(f" ID : {row[1]}  Price : {row[3]}  Quantity available : {row[4]}")
        for row in List: # Billing loop
            print("MED ID: ")
            medID = input()
            if medID == row[1]: # find med id entered by the user in the list
                print("type the Amount you want to buy:")
                medAmount = input() # get the amount the user is willing to buy
                AmountBuy = int(medAmount) # force user input to integer type
                AmountSell =  int(row[4])  # get amount available
                if AmountBuy <= AmountSell: # if amount desired by the user less than or equal stock proceed
                    print("Your Bill")
                    print(f"Medicine Name : {row[2]} \nQuantity purchased : {AmountBuy}\nPrice : {AmountBuy*float(row[3])}")
                    AmountSell -= AmountBuy # subtracts user input from amount available
                    row[4] = str(int(row[4])-AmountBuy) # updates quantity available of the med
                    row[5] = str(int(row[5])+AmountBuy) # updates quantity sold of the med
                    writeObject = csv.writer(open("inventory.txt", "w", newline=''))
                    writeObject.writerows(List)
                    break
                else:
                    print("amount desired exceeds out stock")
                    print("submit new request \n")
                    continue
            else:
                print("Medicine Not Available")
                pass
    pass


def histoGramDisplay():
    # remember to use "pip install matplotlib"
    # Tip: Listprice here hold a 2D list serving as the DataBase or Frequency counter.
    # this segment will create price list similar to this:
    # [name1,name1,name1,name1,name1,name1
    # name2,name2,name2,name2,name2,name2]

    import matplotlib.pyplot as plt
    ListPrice = [] # initializing empty list which will hold amount sold
    ListName = [] # empty list which will hold med names
    with open('inventory.txt')as csvFile:
        read = csv.reader(csvFile, delimiter=',')
        for row in read: # executing this loop for each row separately
            i=0 # loop control
            range = int(row[5]) # histogram max data range
            while i<range:
                i+=1
                ListPrice.append(row[2]) # appends med name to the price list once each iteration till range is reached
            ListName.append(row[2]) # append med name to Name list
        plt.hist(ListPrice, bins=ListName, ) # plots the histogram
        plt.show() # shows the histogram
    pass


def main():
    # choices constants
    ADDING = 1
    SHOWING = 2
    UPDATING = 3
    SEARCH_DELETE = 4
    BILLING = 5
    HISTOGRAM_DISPLAY = 6
    EXITING = 7

    file_name = "inventory.txt"

    display_menu()
    choice = int(input("Enter your choice: "))
    if choice not in range(1,8):
        choice = int(input("Enter your choice: "))

    while choice != EXITING: # while the choice not 7
        if choice == ADDING: # choice# 1
            print("Adding a new medicine:")
            print("The type of medicine/product 1 (POM) , 2 (P) or 3(GSL)")
            m_type = int(input("Please Enter 1,2 or 3: "))
            while m_type not in [1,2,3]:                
                m_type = int(input("Please Enter 1,2 or 3: "))
            
            m_name = str(input("Please Enter the Name of the medicine: "))

            # take first two letters from the name, then adding a number as a suggest
            suggested_id = m_name[:2].upper()+"1"
            # prepare the message to show for the user
            prompt = "Enter Medicine ID (suggested id is "+ suggested_id + "):"
            id = str(input(prompt)).upper()
            if id[:2] != m_name[:2].upper() :
                id = str(input(prompt)).upper()

            price = float(input("Please Enter Price: "))
            quantity = int(input("Please Enter quantity: "))
            sold_quantity = int(input("Enter sold quantity : "))

            date_expiry = str(input("Please Enter the Expiry (20102021 for 20/10/2021): "))
            while len(date_expiry) != 8 :
                date_expiry = str(input("Please Enter the Expiry (20102021 for 20/10/2021): "))

            medicine_details =str(m_type)+';'+id+';'+ m_name +';'+str(price)+';'+str(quantity) +';'\
                    + str(sold_quantity) +';' + date_expiry

            # write medicine/product info to the file
            write_function(file_name , medicine_details)
            print("\n+++ medicine/product saved successfully!+++")

        elif choice == SHOWING: # choice# 2
            print("\nShow the inventory\n")
            print("-choose (E) to show medicines which expir last 3 months of year: ")
            print("-choose (L) to show medicines which stock available less than 10: ")
            input_ = str(input("Enter your option: ")).lower()
            while input_ not in ["e", "l"]:
                input_ = str(input("Enter your option: ")).lower()
            if input_ == "e":
                list_medicines_per_expiry(file_name , 3)
            else:
                display_medicines_per_qty(file_name , 10)

        elif choice == UPDATING: # choice# 3
            print("please type the MED ID you desire to edit")
            Med_ID = input()
            updateInventory(Med_ID) #update inventory function with Med ID as parameter
        elif choice == SEARCH_DELETE: # choice# 4
            print("Please Type in the TYPE number")
            medType = input()
            print("Please enter the ID of a medicine")
            medID = input()
            searchAndDelete(medID,medType)
        elif choice == BILLING: # choice# 5
            billing()
        elif choice == HISTOGRAM_DISPLAY: # choice# 6
            histoGramDisplay()


        display_menu()
        choice = int(input("Enter your option: "))
        if choice not in range(1,8):
            choice = int(input("Enter your option: "))
        
    if choice == EXITING:
        print("\nExiting the program!, see you later ... \n")

main()
