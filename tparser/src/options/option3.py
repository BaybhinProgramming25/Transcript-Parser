# DELETE a specific xlsx file from the backend 

from mongo.mongoclient import collection_name

import requests, os 

def option3():

    # list all the documents that are possible for deletion
    database_documents = collection_name.find()

    if not database_documents:

        print("There are no documents in the database. Please select option 2 to create a transcript\n")
        return
    else:

        list_of_document_names = []
        for index, document in enumerate(database_documents):
            print(f'Document #{index+1}: {document.get("xlsx_name")}\n')
            list_of_document_names.append(document.get('xlsx_name'))
        
        transcript_option = str(input("Please select which of the following transcripts to DELETE. MAKE SURE ALL XLSX FILES ARE CLOSED\n"))

        option_found = False 
        for name in list_of_document_names:
            if transcript_option == name:
                option_found = True 
                break 

        if option_found:

            # Find the file with the specific name
            file_to_retrieve = {'file_name': transcript_option}
            delete_response = requests.delete("http://127.0.0.1:8000", json=file_to_retrieve)

            delete_response_json = delete_response.json()

            if delete_response.status_code == 404:
                print(f'HTTP Status Code {delete_response.status_code}: {delete_response_json.get("message")}', end="\n\n")
                return 
            else:
                
                # Delete the document if it exists 
                document_directory = f'{os.getcwd()}\\TParser\\output_xlsx\\{transcript_option}.xlsx'

                if os.path.exists(document_directory):
                    os.remove(document_directory)
                
                print(f'HTTP Status Code {delete_response.status_code}: {delete_response_json.get("message")}', end="\n\n")
                return 
        else:
            print("Could not find the requested document. Returning back to the options menu\n")
            return 
