from Crypto.Cipher import AES

password = b'1234567812345678' #The secret key, b, is expressed as bytes
text = b'abcdefghijklmnhi' #Content to be encrypted, bytes type
aes = AES.new(password,AES.MODE_ECB) #Create an aes object
# AES.MODE_ECB indicates that the mode is ECB mode
en_text = aes.encrypt(text) #Encrypted plaintext
print("Ciphertext:",en_text) #Encrypted plaintext, bytes type
den_text = aes.decrypt(en_text) # Decrypt ciphertext
print("Plaintext:",den_text)