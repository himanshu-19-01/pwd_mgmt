import random
import string

def random_pass():
        # List of alphabets
        alphabets = list(string.ascii_letters)

        # List of numbers
        numbers = list(string.digits)

        # List of special characters
        special_chars = list(string.punctuation)

   
        selected_special_char = random.sample(special_chars, 1)

        selected_numbers = random.sample(numbers, 3)
 
        selected_alphabets = random.sample(alphabets, 4)
 
        password = selected_special_char + selected_numbers + selected_alphabets

        
        random.shuffle(password)
 
        password = ''.join(password)

       
        return password
