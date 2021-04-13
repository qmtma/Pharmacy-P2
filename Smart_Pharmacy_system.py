

#  writing string to the file
import csv # importing csv library


def write_function(file_name , str_info): # files have 3 modes "r "\ "w" \ "a"
    out = open(file_name, "a") #
    out.write(str_info + '\n')
    out.close()
 
 # display medicines which have a quantity less than a given quantity
def display_medicines_per_qty(file_name, q):
    print("\nMedicines with available stock less than", q, ":")
    count = 0
    lines = read_file(file_name)
    for record in lines:
        record_list = record.strip().split(",")
        base_qty = int(record_list[4])  # index of quantity in file (index 4 in record list)
        sold_qty = int(record_list[5]) # index of sold quantity (index 5 in record list)
        # Existing Quantity = all quantity - sold quantity this results in availabe quantity
        Existing_qty = base_qty - sold_qty
        if Existing_qty < q:            # if its less than 10
            # Display the Medicine that match condition
            print_medicine(record_list)
            count = count + 1
     
    if count == 0:
        # display a message when no product to show
        print(" -- No quantities less than ", q)

# display medicines which expir at next given number of months
def list_medicines_per_expiry(file_name, months_to_expir): 
    import datetime # python library for date & time data
    long_date = datetime.datetime.now() # long_date = Now's date
    # datetime.datetime.now() months_to_expire = 3
    print("\nProducts which expire within next", months_to_expir,"months:")
    count = 0 # loop control variable
    lines = read_file(file_name) # lines = the return value of read_file function
    for line in lines:
        record_list = line.strip().split(",") # results in a list of lists (2D list )
        # retrieve current year        
        current_Year = long_date.year #
        current_month = int(long_date.strftime("%m")) # can be replaced with long_date.month
        # retrieve the month & year from expiry date field
        ex_month = int(record_list[6][2:4]) # list index 6 (date) items (2-3) month
        ex_year  = int(record_list[6][4:]) # list index 6 items 4-end

        if ex_year == current_Year:
            # param (month_num) is the month that at it the checked period ends
            month_num = current_month + months_to_expir # 4 + 3
            if ex_month >=current_month and ex_month <= (month_num): # expiry month > or equal current month & less month_num
                # if ( ex_month - current_month) <= 3:
                print_medicine(record_list)
                count = count + 1  #

     
    if count == 0:
        # display a message when no product to show
        print(" -- No Medicines expire in next", months_to_expir, "months.")

# read inventory lines
def read_file(file_name):
    import os # python defined library responsible for paths and directory related functions
    lines = []
    if os.path.exists(file_name): # checks if the file exists
        input_file = open(file_name,'r')
        # (enumerate function): read all lines and make a list of them
        for line in enumerate(input_file): # NUMBERING the lines for (we iterate for each element in an iterable data)
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
def update_inventory(Med_ID):
    # TIP: keep this data visualization in mind
    # the next line shows a list of lists, for this program, each list inside the list is referred to as a row THUS:
    # [[2,PA1,Panadol,11.0,15,32,27102021],[1,AU3,Augmenting,34.0,167,98,01092021]]
    # (1,AU3,Augmenting,34.0,167,98,01092021) is a row and each element has an index, so row[0] corresponds to Type,.etc

    with open('inventory.txt') as csvFile:  # opening the file and naming it csvFile (this name is optional)
        # opens inventory.txt for read, and runs the segment if it was opened successfully
        #csv.reader is a function defined in csv library

        dataSelect = csv.reader(csvFile, delimiter=',') # dataSelect holds csv file data, in an array like type
        # dataSElect of (IO file type ) which can not be manipulated
        List = list(dataSelect) # force change data type into a list (results in a list of lists aka 2D array)
        # List = [[2,PA1,Panadol,11.0,15,32,27102021],[1,AU3,Augmenting,34.0,167,98,01092021]]
        # row = [2,PA1,Panadol,11.0,15,32,27102021]
        for row in List: # looping through each dimention
            if row[1] == Med_ID: # if Med ID is found  ////
                # lines 113 & 114 are the search operation for the ID entered
                # by the user
                # print relevant data for user confirmation
                print(f" Type : {row[0]}\n ID : {row[1]}\n Name :{row[2]}\n Price : {row[3]}\n quantity : {row[4]}\n quantity sold :{row[5]}\n Expiry Date : {row[6]} ")
                print("Which value you are willing to edit?  (Select a number)")
                print("1. quantity")
                print("2. Expiry Date")
                choice = input()
                if choice == "1":
                    print("Enter New quantiry")
                    NewQuantity = input()
                    # changing the quantity (row[4]) to the input entered by the user (New Quantity)
                    row[4] = NewQuantity # updates quantity value in the list
                    # quantity in the row( line in the list where the ID was found) = user input

                    #csv.writer is defined is csv library responsible for writng csv files (seperated data files)
                    writeObject = csv.writer(open("inventory.txt","w", newline='')) # opens inventory.txt as write file
                    writeObject.writerows(List) # writes the Updated List into inventory.txt file
                    # writeObject is a file (IO data type)
                if choice == "2":
                    print("Enter New Date without any separators")
                    NewDate = input()
                    row[6] = NewDate  # row[6] is the date value of the row
                    writeObject = csv.writer(open("inventory.txt", "w", newline=''))
                    writeObject.writerows(List)
        csvFile.close()


    pass

# search and delete function definition
def search_delete(medID, medType):
    # following the same method in UpdateInventory function
    # line 149 - 156 is the same as lines 104 - 1118
    with open("inventory.txt") as csvFile:
        inventory = csv.reader(csvFile, delimiter=',')
        inventoryList = list(inventory)
        for row in inventoryList:
            if row[0] == medType and row[1] == medID: # find a row which has bot Type & ID values equal to user input
                print("MED found")
                print(f" Type : {row[0]}\n ID : {row[1]}\n Name :{row[2]}\n Price : {row[3]}\n quantity : {row[4]}"
                      f"\n quantity sold :{row[5]}\n Expiry Date : {row[6]} ")
                print("are you sure you want to delete the data above? (y/n)")
                answer = input().lower()# confirming correct search result
                if answer == 'y':
                    lineNo = inventoryList.index(row) # finding the index nu,ber of the line (row) in the list
                    inventoryList.pop(lineNo) # deleting the line
                    writeObject = csv.writer(open("inventory.txt", "w", newline='')) # newline = '' to prevent entering a new line
                    writeObject.writerows(inventoryList)
                else: pass

    pass


def bill():
    print("Choose the Medicine")
    with open("inventory.txt") as csvFile: # opens the inventory file in read mode
        inventory = csv.reader(csvFile, delimiter=',') # csv.reader call
        inventoryList = list(inventory) # force change type to list
        for row in inventoryList: # a loop through all the list printing ID,Price,quantity available of all products
            # fstring ( python method to print variables inside a string )
            print(f" ID : {row[1]}  Price : {row[3]}  Quantity available : {row[4]}")
        for row in inventoryList: # Billing loop
            print("MED ID: ")
            ID = input()
            if ID == row[1]: # find med id entered by the user in the list
                print("type the Amount you want to buy:")
                quantity = input() # get the amount the user is willing to buy
                purchaseQuantity = int(quantity) # force user input to integer type
                availableAmoint =  int(row[4])  # get amount available
                if purchaseQuantity <= availableAmoint: # if amount desired by the user less than or equal stock proceed
                    print("Your Bill")
                    print(f"Medicine Name : {row[2]} \nQuantity purchased : {purchaseQuantity}\n"
                          f"Price : {purchaseQuantity*float(row[3])}")

                    availableAmoint -= purchaseQuantity # subtracts user input from amount available
                    # substracts purchased quantity from the quantity
                    row[4] = str(int(row[4])-purchaseQuantity) # updates quantity available of the med
                    row[5] = str(int(row[5])+purchaseQuantity) # updates quantity sold of the med
                    writeObject = csv.writer(open("inventory.txt", "w", newline='')) # save the NEw data to the file
                    writeObject.writerows(inventoryList)
                    break
                else:
                    print("amount desired exceeds out stock")
                    print("submit new request \n")
                    continue
            else:
                print("Medicine Not Available")
                pass
    pass


def histogram():
    # remember to use "pip install matplotlib"
    # Tip: Listprice here hold a 2D list serving as the DataBase or Frequency counter.
    # this segment will create price list similar to this:
    # [name1,name1,name1,name1,name1,name1
    # name2,name2,name2,name2,name2,name2]

 # importing matplotlib which is a python library for plotting
    import matplotlib.pyplot as plt
    Prices = [] # initializing empty list which will hold amount sold
    Names = [] # empty list which will hold med names
    with open('inventory.txt')as csvFile: #opens inventory in read mode
        read = csv.reader(csvFile, delimiter=',')
        for row in read: # executing this loop for each row separately # repetition
            i=0 # loop control
            #  histogram max data range x and y axis
            range = int(row[5])   # sets the range to qunatity sold
            # this while loop is to set the statistics for each medicine
            while i<range:  # while i is less than range (quantity sold) keep appending to Prices
                i+=1
                Prices.append(row[2]) # appends med name to the price list once each iteration till range is reached
            Names.append(row[2]) # append med name to Name list
        plt.hist(Prices, bins=Names, ) # plots the histogram
        plt.show() # shows the histogram
    pass


def main():
    # choices constants variables = 1- 7
    ADDING = 1
    SHOWING = 2
    UPDATING = 3
    SEARCH_DELETE = 4
    BILLING = 5
    HISTOGRAM_DISPLAY = 6
    EXITING = 7

    file_name = "inventory.txt" # opening the file

    display_menu() # function call emnu display
    choice = int(input("Enter your choice: ")) # variable ()
    if choice not in range(1,8): # choice =<8 or choice <1
        #invalid enter a new choice
        choice = int(input("Enter your choice: "))

    while choice != EXITING: # while the choice not 7
        # no of iteration
        if choice == ADDING: # choice# 1
            print("Adding a new medicine:")
            print("The type of medicine/product 1 (POM) , 2 (P) or 3(GSL)")
            m_type = int(input("Please Enter 1,2 or 3: ")) #input value held by m_type
            while m_type not in [1,2,3]:                
                m_type = int(input("Please Enter 1,2 or 3: "))
            
            m_name = str(input("Please Enter the Name of the medicine: ")) # Name input
            print(m_name)
            # take first two letters from the name, then adding a number as a suggest
            suggested_id = m_name[:2].upper()+"1" # m_name
            # prepare the message to show for the user
            #force captilization (PA)
            prompt = "Enter Medicine ID (suggested id is "+ suggested_id + "):"
            id = str(input(prompt)).upper() # input()
            if id[:2] != m_name[:2].upper() : # first two letter of ID == forst two laetter of m_name
                id = str(input(prompt)).upper() # will happen only once
            price = float(input("Please Enter Price: ")) #  force conversion to float (eg: 2282.20)
            quantity = int(input("Please Enter quantity: ")) # integer
            sold_quantity = int(input("Enter sold quantity : "))

            date_expiry = str(input("Please Enter the Expiry (20102021 for 20/10/2021): "))
            while len(date_expiry) != 8 : # LOOP if date length is not 8
                # please re enter date
                date_expiry = str(input("Please Enter the Expiry (20102021 for 20/10/2021): "))
# med type
            medicine_details =str(m_type)+','+id+','+ m_name +','+str(price)+','+str(quantity) +','\
                    + str(sold_quantity) +',' + date_expiry
 #

            # write medicine/product info to the file
            write_function(file_name , medicine_details) # write_function (file_name, )
            print("\n+++ medicine/product saved successfully!+++")

        elif choice == SHOWING: # choice# 2
            print("\nShow the inventory\n")
            print("-choose (E) to show medicines which expir last 3 months of year: ")
            print("-choose (L) to show medicines which stock available less than 10: ")
            input_ = str(input("Enter your option: ")).lower() # force lower case
            while input_ not in ["e", "l"]:
                input_ = str(input("Enter your option: ")).lower() # checking that the user enter E or L
            if input_ == "e": # if user enter E
                list_medicines_per_expiry(file_name , 3)
            else: # one of two choices only eith an e or L

                display_medicines_per_qty(file_name , 10)  # Phase 1

        elif choice == UPDATING: # choice# 3  phase 2 starts
            print("please type the MED ID you desire to edit")
            Med_ID = input() # simple assignment of user input
            update_inventory(Med_ID) #update inventory function with Med ID as parameter
        elif choice == SEARCH_DELETE: # choice# 4
            print("Please Type in the TYPE number") # user will input med type
            medType = input()
            print("Please enter the ID of a medicine") # user will enter med ID
            medID = input()
            search_delete(medID,medType)
        elif choice == BILLING: # choice# 5
            bill()
        elif choice == HISTOGRAM_DISPLAY: # choice# 6 phase 2 ends
            histogram()


        display_menu()
        choice = int(input("Enter your option: "))
        if choice not in range(1,8):
            choice = int(input("Enter your option: ")) # while loop code fragment
            #after every excution of the body we check the condition
        
    if choice == EXITING:
        print("\nExiting the program!, see you later ... \n")

main()
