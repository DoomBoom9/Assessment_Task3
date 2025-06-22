import sys
sys.path.insert(0, '/Users/angusallen/Documents/GitHub/Assessment_Task3')

from main import encrypt_input, decrypt_input, group_order_history
from main import cipher
from ORM.ORM_operations import get_product_by_id
encrypted_input = encrypt_input('test', cipher)

class TestOrder():
    def __init__(self, order_id, product_id):
        self.order_id = order_id
        self.product_id = product_id

def item_object_quantity_dict(test_data:dict) -> dict: #this is a clone used to test
    #using the one in main would require me to pass in test data
    #but not passing in anything would also make it angry
    #so to save the headache I've cloned it without session['cart']
    object_quantity_dict = {}
    cart = test_data

    for i in cart.keys():
        object_quantity_dict[get_product_by_id(i)] = cart[i] #creates a dictionary of the products in the cart
    return object_quantity_dict
    



def test_encrypt_input():
    assert encrypt_input('test', cipher) != 'test' #Tests valid data
    try: 
        encrypt_input(1, cipher) #should throw an error since int is an invalid type
        assert False #asserts false if the test fails
    except AttributeError:
        assert True #asserts true if the test passes
    try:
        encrypt_input(b'test', cipher) #should throw an error, bytes are an invalid type
        assert False
    except AttributeError:
        assert True
    try:
        encrypt_input('test', 1)  #should throw an error int is an invalid type
        assert False
    except AttributeError:
        assert True


def test_decrypt_input():
    assert decrypt_input(encrypted_input, cipher) == 'test' # sees if it decrypts correctly
    try:
        decrypt_input(1, cipher) # tests invalid type int
        assert False
    except TypeError:
        assert True
    try:
        decrypt_input(encrypted_input, 1) #tests invalid type int in the other argument
        assert False
    except AttributeError:
        assert True
    
def test_item_object_quantity_dict():
    product_object = get_product_by_id(1)
    assert item_object_quantity_dict({1:4}) == {product_object:4} #tests valid data

    try:
        item_object_quantity_dict({'test':4}) #should throw an error since get_product_by_id expects type int
        assert False   
    except TypeError: #If an invalid type is passed in but for some reason i entered the id 'test' into the db
        assert True   
    except Exception: #if invalid product id is passed in, It should return none and throw an error
        assert True

def test_group_order_history():
    expected_value = [[TestOrder(1,1), TestOrder(1,3)], [TestOrder(2, 4)], [TestOrder(5, 3), TestOrder(5,2)]]
    test_list = group_order_history([TestOrder(1,1), TestOrder(1,3), TestOrder(2, 4), TestOrder(5, 3), TestOrder(5,2)])
    for i in range(len(test_list)): #Tests valid data
        for j in range(len(test_list[i])):
            assert test_list[i][j].order_id == expected_value[i][j].order_id
            assert test_list[i][j].product_id == expected_value[i][j].product_id

    test_list = group_order_history([TestOrder(-1,1), TestOrder(1,3), TestOrder(2, 4), TestOrder(5, 3), TestOrder(5,2)])
    expected_value = [[TestOrder(-1,1)], [TestOrder(1,3)], [TestOrder(2, 4)], [TestOrder(5, 3), TestOrder(5,2)]]
    for i in range(len(test_list)): #Tests valid but technically impossible data (this should still pass)
        for j in range(len(test_list[i])):
            assert test_list[i][j].order_id == expected_value[i][j].order_id
            assert test_list[i][j].product_id == expected_value[i][j].product_id

    try:
        x= group_order_history(3) #should throw error since the function expects an array
        print(x)
        assert False
    except:
        assert True
    try:
        x= group_order_history([1,2,3,4,5,6]) #should throw an error since array elements are not objects
        print(x)
        assert False
    except:
        assert True


