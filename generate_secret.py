from cryptography.fernet import Fernet
key = Fernet.generate_key() #generates a secret key that can be exported to the environment as a var
print(key.decode())