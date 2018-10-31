def menu_select(top_value):
    while True:
        range_value= int(top_value)
        try:
            choice = int(input(f"Please enter your choice (1 - {top_value})"))
            if choice not in range(1,top_value) or type(choice) is not int:
                print(f"Please enter a value from 1 - {top_value}")
            if choice in range(1,top_value):
                return(choice)
                break
        except:
            print("Please enter a numerical value")

menu_select(5)
