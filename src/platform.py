from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import random
import pickle
import os


class Platform:
	def __init__(self, platform_storage="./.platform/", public_storage="./data/", sess_id="./data/sess.dat", user_pass_file="./data/user_pass.dat"):
		self.sess_id = sess_id
		self.user_pass_file = user_pass_file
		self.platform_storage = platform_storage
		self.public_storage = public_storage
		self.authorities_public_key = None
		self.platform_platform_key = None
		self.init_platform_keys()
		self.aes = AES.new(self.platform_platform_key, AES.MODE_ECB)
		self.user_pass = self.read_user_pass()

	def send_session_key(self, username, session_key):
		with open("./.platform/authority_public.key", "rb") as f:
			public_key = RSA.import_key(f.read())
		cipher_rsa = PKCS1_OAEP.new(public_key)
		enc_session_key = cipher_rsa.encrypt(session_key)
		if not os.path.exists(self.sess_id):
			data = {username: enc_session_key}
			with open(self.sess_id, "wb") as f:
				pickle.dump(data, f)
		with open(self.sess_id, "rb") as f:
			data = pickle.load(f)
		if username not in data.keys():
			data.update({username: enc_session_key})
			with open(self.sess_id, "wb") as f:
				pickle.dump(data, f)

	def init_platform_keys(self):
		if not os.path.exists(self.platform_storage+"platform.key"):
			with open(self.platform_storage+"platform.key", "wb") as f:
				platform_platform_key = get_random_bytes(16)
				f.write(platform_platform_key)
		with open(self.platform_storage+"platform.key", "rb") as f:
			self.platform_platform_key = f.read()

	def read_user_pass(self):
		if not os.path.exists(self.user_pass_file):
			return {}
		else:
			with open(self.user_pass_file, "rb") as f:
				return pickle.load(f)

	def register_new_user(self, user_name, password):
		if user_name in self.user_pass.keys():
			print("Username already registered!")
			return 0
		else:
			print("Registering new user... Please login again!")
			password = password+' '*(16-(len(password)%16))
			password = password.encode()
			self.user_pass.update({user_name: self.aes.encrypt(password)})
			with open(self.user_pass_file, "wb") as f:
				pickle.dump(self.user_pass, f)
			return 0

	def login_user(self, user_name, password):
		if user_name not in self.user_pass.keys():
			print("Not registered!")
			return False
		else:
			password_enc = self.user_pass[user_name]
			password_orig = self.aes.decrypt(password_enc)
			password_orig = password_orig.decode()
			password_orig = password_orig.strip()
			return password==password_orig