
              print("3) UPDATE a CSV file")
              print("4) DELETE a CSV file")
              print("5) Exit the program\n")
             
              user_option = str(input("Please Select One Of The Numbers: "))

              if user_option == "1":
                    option1_value = option1.option1()
              elif user_option == "2":
                    print("CODE TO BE IMPLEMENTED")
              elif user_option == "3":
                    print("CODE TO BE IMPLEMENTED")
              elif user_option == "4":   
                    print("CODE TO BE IMPLEMENTED")
                    # We will determine the option2_value and what to do with it later on 
              elif user_option == "5":
                    print("Program Ended!")
                    break 
              else:
                    print("Invalid Option! Please select a valid option")
                

if __name__ == '__main__':
    main()