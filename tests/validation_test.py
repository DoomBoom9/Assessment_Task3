import sys
sys.path.insert(0, '/Users/angusallen/Documents/GitHub/Assessment_Task3')

from validation import check_username, check_phone_num, check_default, check_file, sanitise, check_password

def test_check_username() -> None:
    assert check_username("test") == True 
    assert check_username("test123") == True
    assert check_username(1) == False # should be a string
    assert check_username([]) == False # should be a string
    assert check_username({}) == False # should be a string
    assert check_username(1.0) == False # should be a string
    assert check_username(True) == False # should be a string
    assert check_username("") == False # should be longer than 0 characters
    assert check_username("12345678901234567890123456") == False   # should be less than 26 characters
    assert check_username("1") == True # Edge case 1 character
    assert check_username("1234567890123456789012345") == True # Edge case 25 characters

def test_check_phone_num() -> None:
    assert check_phone_num("1234567890") == True
    assert check_phone_num(1) == False # should be a string
    assert check_phone_num([]) == False # should be a string
    assert check_phone_num({}) == False # should be a string
    assert check_phone_num(1.0) == False # should be a string
    assert check_phone_num(True) == False # should be a string
    assert check_phone_num("") == False # should be 10 characters
    assert check_phone_num("12345678901") == False  # should be 10 characters
    assert check_phone_num("123456789") == False # should be 10 characters
    assert check_phone_num("123456789a") == False  # should be numeric only
    assert check_phone_num("123456789!") == False  # should be numeric only

def test_check_default() -> None:
    assert check_default("test") == True
    assert check_default("test123") == True
    assert check_default(1) == False # should be a string
    assert check_default([]) == False # should be a string
    assert check_default({}) == False # should be a string
    assert check_default(1.0) == False # should be a string
    assert check_default(True) == False # should be a string
    assert check_default("") == False   # should be longer than 0 characters
    assert check_default("123456789012345678901234567890123456789012345678901") == False  # should be less than 51 characters
    assert check_default("1") == True # Edge case 1 character
    assert check_default("1234567890123456789012345") == True # Edge case 25 characters

def test_check_file() -> None:
    assert check_file("1.jpg") == True
    assert check_file("IMG_9036.heic") == False # should be a jpg, jpeg, or png
    assert check_file(1) == False # should be a string
    assert check_file([]) == False # should be a string
    assert check_file({}) == False # should be a string
    assert check_file(1.0) == False # should be a string
    assert check_file(True) == False # should be a string

def test_sanitise() -> None:
    assert sanitise("test") == "test"
    assert sanitise("test123") == "test123"
    assert sanitise(1) == False # should be a string
    assert sanitise([]) == False # should be a string
    assert sanitise({}) == False # should be a string
    assert sanitise(1.0) == False # should be a string
    assert sanitise(True) == False # should be a string
    assert sanitise("<script>alert('test')</script>") == "&lt;script&gt;alert(&#x27;test&#x27;)&lt;&#x2F;script&gt;"
    assert sanitise("'") == "&#x27;"
    assert sanitise('"') == "&quot;"
    assert sanitise("/") == "&#x2F;"
    assert sanitise("<") == "&lt;"
    assert sanitise(">") == "&gt;"

def test_check_password() -> None:
    assert check_password("BingoBongo!!!") == False # should have at least 1 number
    assert check_password("BingoBongo123") == False# should have at least 1 special character
    assert check_password("BingoBon!2") == False # should be longer than 11 characters
    assert check_password("BingoBongo12!!!BingoBongo!!!BingoBongo!!!") == False # should be less than 26 characters
    assert check_password("BingoBongo12!!!") == True
    assert check_password(1) == False # should be a string
    assert check_password([]) == False # should be a string
    assert check_password({}) == False # should be a string
    assert check_password(1.0) == False # should be a string
    assert check_password(True) == False # should be a string
    assert check_password(int) == False # should be a string