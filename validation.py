import re
import os

# import bcrypt


#checks if the password is valid
def check_password(password: str):
    try:
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if len(password) < 12:
            raise ValueError("Value must be more than 11 characters")
        if len(password) > 25:
            raise ValueError("Value must be less than 26 characters")
        if re.search(r"[ ]", password):
            raise ValueError("Value must have no whitespaces")
        if not re.search(r"[A-Z]", password):
            raise ValueError("Value must have at least 1 uppercase character")
        if not re.search(r"[a-z]", password):
            raise ValueError("Value must have at least 1 lowercase character")
        if not re.search(r"[0-9]", password):
            raise ValueError("Value must have at least 1 numeric character")
        if not re.search(r"[@$!%*?&]", password):
            raise ValueError("Value must have at least 1 special character")
    except ValueError:
        return False
    except TypeError:
        return False
    return True

#checks if username is valid
def check_username(username: str):
    try:
        if not issubclass(type(username), str):
            raise TypeError("Value must be type: string")
        if len(username) < 1:
            raise ValueError("Value must be longer than 0 characters")
        if len(username) > 25:
            raise ValueError("Value must be less than 25 characters") 
        else:
            return True
    except ValueError:
        return False
    except TypeError:
        return False

#checks if phone number is valid
def check_phone_num(phone_num: str):
    try:
        if not issubclass(type(phone_num), str):
            raise TypeError("Value must be type: string")
        if len(phone_num) != 10:
            raise ValueError("Value must be 10 characters")
        if not re.search(r"^[0-9]*$", phone_num):
            raise ValueError("Value must be numeric only")
        else:
            return True
    except ValueError:
        return False
    except TypeError:
        return False
    
#checks if default fields (longer answer fields) are valid (Address, security answers, etc.)
def check_default(input: str):
    try:
        if not issubclass(type(input), str):
            raise TypeError("Value must be type: string")   
        if len(input) > 50:
            raise ValueError("Value must no longer than 50 characters")
        if len(input) < 1:
            raise ValueError("Value must be longer than 0 characters") 
        else:
            return True
    except ValueError:
        return False
    except TypeError:
        return False
    
#checks if files are valid
def check_file(filepath: str):
    try:
        if not issubclass(type(filepath), str):
            raise TypeError("Value must be type: string") 
        file_ext = os.path.splitext(filepath)
        file_ext = file_ext[1]
        if file_ext not in ['.png','.jpeg','.jpg']:
            raise ValueError("Invalid filetype: must be .png, .jpeg, or .jpg")
        else:
            return True
    except ValueError:
        return False
    except TypeError:
        return False

# Function to sanitise text using a library
def sanitise(string: str) -> str:
    try:
        if not issubclass(type(string), str):
            raise TypeError("Value must be type: string")
        to_replace = ['<','>','"',"'","/"]
        replacements = ['&lt;', "&gt;", "&quot;", "&#x27;", '&#x2F;']
        char_list = list(string)
        for i in range(len(char_list)):
            if char_list[i] in to_replace:
                index = to_replace.index(char_list[i])
                char_list[i] = replacements[index]
        char_list = ''.join(char_list)
        return char_list
    except TypeError:
        return False


#checks validation for all
def check_all(username:str, password:str, securityA1:str, securityA2:str, securityA3:str, address:str, phone_num:str, filepath:str):
    error_log = []
    if check_username(username) != True:
        raise ValueError('Username validation failed!')
    if check_password(password) != True:
        raise ValueError('Password validation failed!')
    if check_default(securityA1) != True:
        raise ValueError('SecurityA1 validation failed!')
    if check_default(securityA2) != True:
        raise ValueError('SecurityA2 validation failed!')
    if check_default(securityA3) != True:
        raise ValueError('SecurityA3 validation failed!')
    if check_default(address) != True:
        raise ValueError('Address validation failed!')
    if check_phone_num(phone_num) != True:
        raise ValueError('Phone number validation failed!')
    if check_file(filepath) != True:
       raise ValueError('File extension validation failed!')
    else:
        return True
    



if __name__ == "__main__":
    # Add unit tests for validation functions here
    pass
