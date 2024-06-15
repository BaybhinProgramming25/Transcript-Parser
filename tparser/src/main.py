""" 
Our entry point into the program. The main program is responsible
for initializing the state variables and creating threads that will
traverse through the transcript, parse the information, and store the
information within the state variables. 
After the threads have been reaped, the main program will then create the
tabular document as an XLSX file to be sent in the output folder
Note: This program is only meant for CSE or ISE students in the major
"""

from mongo.mongoclient import client 
from options import option1, option2, option3

def main():

        while True:
              
              # Display the 3 options
              print("\n1) POST a XLSX file")
              print("2) GET a XLSX File")
              print("3) DELETE a XLSX file")
              print("4) Exit the program\n")
             
              user_option = str(input("Please Select One Of The Numbers: "))

              if user_option == "1": # POST
                    option1.option1()
              elif user_option == "2": # GET
                    option2.option2()
              elif user_option == "3": # DELETE
                    option3.option3()
              elif user_option == "4": # Exit program   
                    print("Program Ended!")
                    client.close() # Close the client 
                    break 
              else:
                    print("Invalid Option! Please select a valid option")
                

if __name__ == '__main__':
    main()
