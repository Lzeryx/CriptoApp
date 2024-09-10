from os import remove
import shutil
import cv2
from pyzbar import pyzbar
from tkinter import messagebox as MessageBox


def scan_barcode():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise ValueError

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            barcode_value = barcode.data.decode("utf-8")
            cv2.putText(frame, barcode_value, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.destroyAllWindows()
            return barcode_value

        cv2.imshow("Barcode Scanner", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def create_keys(password, bar_code, doc_name):
    # Count the number of characters that the document has. 
    with open(doc_name, "r", encoding="utf-8") as file:
        full_text = file.read()
        docum_characters = len(full_text)
        # For farther operetions we need the docum_characters' numbers of digits.
        len_docum_chararacters = len(str(docum_characters))
    
    # Set all barcodes with 13 digts.
    while len(str(bar_code)) < 13:
        bar_code *= 10
    while len(str(bar_code)) > 13:
        bar_code = round(bar_code/10)
    
    # Inicialites variables used to count or save the information
    # In password_number it is goint to be wroten each character converted in the equivalent number
    password_number = ""
    keys= []
    i = 0
    j = 0
    for char in password:
        # In password_number it is goint to be wroten each character converted in the equivalent number.
        char_numer = str(ord(char))
        password_number += char_numer
        # i measure the number of characters that are in password_number
        i += 1

        # When password number has 5 characters in it, he creates a key with them following the above formular.
        if i == 5:
            # j measure the number of keys and it used to mark in which position the key was created
            # because then we are going to sort the keys and we need something that mark in what position it was created to
            # avoid creating same keys if we changes the order of the characters in the password.
            j += 1
            keys.append(
                round((( int(password_number)+ (bar_code)/10) / (bar_code/1000) + (docum_characters/ pow(len_docum_chararacters, 7))) + j)
                )
            password_number = ""
            i = 0
    # If there is not more characters and password_number doesn't have 5 characters in it, we use this formular 
    # to create the last key.
    if i > 0:
        password_number = int(password_number)
        keys.append(round(password_number/ (bar_code/100000)+ (docum_characters/ pow(len_docum_chararacters, 7))))
    
    # Return the keys sorted.
    return sorted(keys, reverse=True)


def mode_encrypt(password, bar_code, document_file="document.txt", new_file="new.txt"):
    # Create the keys
    keys = create_keys(password, bar_code, document_file)
    # Copy the file in a temporary file.
    shutil.copy(document_file, "temp.txt")
    # This variable count the position of the key, which is being used, in keys (read explanation in ### comment).
    position_key = 2
    
    # This file will collect the exception cases.
    with open("problemas.txt", "w", encoding="utf-8") as case:
        # For each key it is going to re-encrypt the file.
        for key in keys:
            inicial_key = key
            # Open Files. Open the temp_file(that has the content of the document) and read lines.
            with open("temp.txt", "r", encoding="utf-8") as temp:
                with open(new_file, "w", encoding="utf-8") as new:
                        for line in temp:
                            # For each character in line is added 1 to key
                            for char in line:
                                key += 1
                                ### - Is the position of the key in keys is odd, the program add the value of key to the Unicode character,
                                # but if it is even, the program subtract the value of the key to the Unicode character.
                                while True:
                                    if position_key % 2 == 0:
                                    # Change original char to another using the key
                                        char_unicode = ord(char) + key
                                        try:
                                            new_char = chr(char_unicode)
                                        except ValueError: # If an error is detected, the key will reset to the initial one.
                                            key = inicial_key
                                            continue

                                    else:
                                        char_unicode = ord(char) - key
                                        new_char = chr(char_unicode)

                                    # Write in the new file the encrypted character
                                    try:
                                        new.write(f"{new_char}")
                                    except UnicodeEncodeError: # if it is detected a excemption case:
                                        char_unicode = char_unicode + 10000
                                        new_char = chr(char_unicode)
                                        new.write(f"{new_char}")

                                        # Write the exception in the problem file
                                        case.write(f"{key} {char_unicode}\n")
                                        break
                                    else:
                                        break
            # After each encryption, the information in the new file is copied in the temporary file to be re-encrypted
            shutil.copy(new_file, "temp.txt")

            position_key += 1 

    # Copy the problem.txt at the bottom of the encypted file.
    write_error_cases(new_file)

    # Remove the temporary file and the problem file.
    remove("temp.txt")
    remove("problemas.txt")




def mode_decrypt(password, bar_code, document_file="new.txt", new_file="nuevo.txt"):
    # Copy the file in a temporary file.
    shutil.copy(document_file, "temp.txt")


    # Identify error cases to then correct them when decrypting those characters.
    # That is, enter the error cases values in a dict to then search them and correct them.
    take_error_cases(document_file)
    with open("problemas.txt", "r", encoding="utf-8") as case:
        problem = {"key": [], "character": []}
        lines = case.readlines()
        for line in lines[::-1]:
            key, character = line.removesuffix("\n").split()
            problem["key"].append(key)
            problem["character"].append(character)

    # Create the keys
    keys = create_keys(password, bar_code, document_file)

    # Is need to invert the list becuase is need to start decrypting using the last key used to encrypt
    keys_decrypt = keys[::-1]

    # Set the postion of the key that was last used when the document was ecypted.
    if len(keys_decrypt) % 2 == 0:
        position_key = 1
    else:
        position_key = 2
    
    a = 0
    # For each key it is going to decrypt again the file
    for key in keys_decrypt:
            inicial_key = key
            # Open the file and read lines
            with open("temp.txt", "r", encoding="utf-8") as temp:
                with open(new_file, "w", encoding="utf-8") as new:
                    for line in temp:
                        # For each character in line is added 1 to key
                        for char in line:
                            key += 1

                            # Identify is the character is a error case and correct it.
                            discount = 0 # If the character is a error case, substract 10000, it not 0
                            if True:
                                
                                try:
                                    for i in range(len(problem["key"])):
                                        if int(problem["key"][i]) == key and int(problem["character"][i]) == ord(char):
                                            discount = 10000
                                except IndexError: # If there is not any error, it will raise IdexError
                                        continue
                                
            
                            
                            ### - Is the position of the key in keys is odd, the program subtract the value of key to the Unicode character,
                            # but if it is even, the program add the value of the key to the Unicode character.
                            if position_key % 2 == 0:
                            # Change original char to another using the key (decrypt)
                                char_unicode = ord(char) - key - discount
                            else:
                                char_unicode = ord(char) + key - discount
                            
                            try:
                                new_char = chr(char_unicode)
                            except ValueError: # If an error is detected, the key will reset to the initial one.
                                key = inicial_key
                                if position_key % 2 == 0:
                                    char_unicode = ord(char) - key - discount
                                else:
                                    char_unicode = ord(char) + key - discount
                                new_char = chr(char_unicode)
                            
                            # Write in the new file the dencrypted character
                            new.write(f"{new_char}")

            # After each dencryption, the information in the new file is copied in the temporary file to be decrypted again
            shutil.copy(new_file, "temp.txt")

            position_key += 1
            

    # Remove the temporary file and the problem file.
    remove("temp.txt")
    remove("problemas.txt")


# It takes the error cases and writes them in problem.txt
def take_error_cases(document_file="new.txt"):
    with open("problemas.txt", "w", encoding="utf-8") as problem:
        with open(document_file, "r", encoding="utf-8") as document:
            lines = document.readlines()
            lines = lines[::-1]

        if "@" in lines[0]: #@ is the symbol used to mark the start of error case information in the encrypted file.
            num_error_cases = int(lines[0].removeprefix("@"))
            for line in lines[1:num_error_cases+1]: 
                problem.write(line)


            # Write the encrypted document in temp.txt without the error cases information.
            with open("temp.txt", "w", encoding="utf-8") as temp:
                lines = lines[::-1]
                for i in range(len(lines)-(num_error_cases + 2)):
                    if i == len(lines)-(num_error_cases + 2) - 1:
                        temp.write(lines[i].removesuffix("\n"))
                    else:
                        temp.write(lines[i])



# Writes at the boton of the encrypted file problem.txt to safe the error case to then be able to decrytided them.
def write_error_cases(new_file="new.txt"):
    with open("problemas.txt", "r", encoding="utf-8") as problem:
        problem_lines = problem.readlines()
        num_cases = len(problem_lines)
        with open(new_file, "a", encoding="utf-8") as new:
            new.write("\n@\n") # @ is the symbol used to mark the start and end of problem.txt
            for line in problem_lines:
                new.write(line)
            new.write(f"@{num_cases}")


def main():
    password= input ("Password: ")
    barcode = int(input("Bardcode: "))
    print(create_keys(password, barcode))

if __name__ == "__main__":
    main()