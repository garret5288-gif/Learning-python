# ceasar cypher
# encrypts and decrypts messages by shifting letters by a key value
letters = "abcdefghijklmnopqrstuvwxyz" #26 letters in the alphabet
num_of_letters = len(letters) #26

def main(): #main function to run the program
    print("*************")
    print("Caesar Cypher")
    print("*************")
    action = input("Do you want to encrypt or decrypt a message? (Press E or D): ")
    print()
    
    if action.lower() == "e": # encrypt
        text = input("Enter your message to encrypt: ")
        key = int(input("Enter the key (number of positions to shift): "))
        encrypted_text = encrypt_decrypt(text, "e", key)
        print(f"Encrypted message: {encrypted_text}")
    elif action.lower() == "d": # decrypt
        text = input("Enter your message to decrypt: ")
        key = int(input("Enter the key (number of positions to shift): "))
        plain_text = encrypt_decrypt(text, "d", key)
        print(f"Decrypted message: {plain_text}")
    else:
        print("Invalid action. Please choose either 'E' for encrypt or 'D' for decrypt.")

def encrypt_decrypt(text, mode, key)->str | int: # function to encrypt or decrypt the message
    """
    Encrypts or decrypts a message using the Caesar cipher.

    Args:
        text (str): The input text to encrypt or decrypt.
        mode (str): "e" for encryption, "d" for decryption.
        key (int): The number of positions to shift the letters.

    Returns:
        str: The encrypted or decrypted message.
    


    Returns:_type_: _description_
    """
    result = "" # initialize result string
    if  mode == "d": 
        key = -key # reverse the key for decryption

    for letter in text:
        letter = letter.lower()
        if not letter == " ": # ignore spaces
            index = letters.find(letter)
            if index == -1: # if character is not in alphabet, keep it unchanged
                result += letter # add unchanged character to result
            else:
                new_index = index + key # calculate new index
                if new_index >= num_of_letters:
                    new_index -= num_of_letters
                elif new_index < 0: # wrap around for negative index
                    new_index += num_of_letters
                result += letters[new_index]
    return result

main()