from Crypto.Cipher import AES
import pickle
import random
import os
from src.authorities import Authorities
from src.platform import Platform

class User:
	def __init__(self, username, password, logging_in=True, user_dir="./data/users/", seed=0):
		self.seed = seed
		self.username = username
		self.password = password
		self.user_dir = user_dir
		self.logging_in = logging_in
		self.replacements = {"names": ["Jake", "Josh"], "locations": ["London", "Paris", "CityHall"], "organizations": ["Google"]}
		if logging_in:
			self.authorities = Authorities(username, password)
			self.platform = Platform()
			session_key = self.get_session_key()
			self.aes = AES.new(session_key, AES.MODE_ECB)

	def get_session_key(self, new=True):
		password = ''.join([self.password for _ in range(16//len(self.password) + 1)])[:16]
		password = list(password)
		random.seed(self.seed)
		random.shuffle(password)
		password = ''.join(password)
		tmp_aes = AES.new(password.encode(), AES.MODE_ECB)
		session_key = tmp_aes.encrypt(password.encode())
		if new:
			print("User-Personal Key", session_key)
		self.platform.send_session_key(self.username, session_key)
		return session_key


	def instance(self):
		data = input("Enter tweet:\t").encode().split()
		word_array = input("Enter words:\t").encode().split()
		path = self.user_dir+self.username+".dat"
		new_data = []
		encrypted_words = []
		for idx, word in enumerate(data):
			if word in word_array:
				word = word+b' '*(16-(len(word)%16))
				word = self.aes.encrypt(word)
				encrypted_words.append(word)
			new_data.append(word)
		new_data = b' '.join(new_data)
		if not os.path.exists(path):
			dat_savable = [{"data":new_data, "encrypted_words": encrypted_words}]
			with open(path, "wb") as f:
				pickle.dump(dat_savable, f)
		else:
			with open(path, "rb") as f:
				dat_savable = pickle.load(f)
			dat_savable.append({"data":new_data, "encrypted_words": encrypted_words})
			with open(path, "wb") as f:
				pickle.dump(dat_savable, f)

	def decrypt_user_data(self, session_key=None):
		path = self.user_dir+self.username+".dat"
		if self.logging_in:
			if session_key is None:
				session_key = self.get_session_key(new=False)
			aes = AES.new(session_key, AES.MODE_ECB)
			if not os.path.exists(path):
				print("No data stored...")
			else:
				data_arr = []
				with open(path, "rb") as f:
					dat_savable = pickle.load(f)
					for query in dat_savable:
						data = query["data"]
						encrypted_words = query["encrypted_words"]
						for encrypted_word in encrypted_words:
							decrypted_word = aes.decrypt(encrypted_word)
							data = data.replace(encrypted_word, decrypted_word.strip())
						data_arr.append(data)
				return data_arr
		else:
			data_arr = []
			with open(path, "rb") as f:
				dat_savable = pickle.load(f)
				random.seed(sum([ord(i) for i in self.username]))
				for query in dat_savable:
					data = query["data"]
					encrypted_words = query["encrypted_words"]
					for encrypted_word in encrypted_words:
						replacement = random.choice(self.replacements["names"])
						data = data.replace(encrypted_word, replacement.encode())
					data_arr.append(data)
			return data_arr


	def browse(self):
		if not self.authorities.logged_in:
			usernames = [i[:-4] for i in os.listdir(self.user_dir)]
			print("\n\n")
			_ = [print(str(i+1)+".\t"+username) for i,username in enumerate(usernames)]
			response = input("\n\nDo you have someone's session key? (Y/N)")
			if response.lower()=='y':
				session_username = input("Enter username:\t").strip()
				session_key_path = input("Enter session key path:\t").strip().encode()
				with open(session_key_path, "rb") as f:
					session_key = f.read()
				print(session_key)
			else:
				session_username=""
			for username in usernames:
				if username!=self.username and username!=session_username:
					tmp_usr = User(username, "", False)
					_ = [print({username: i}) for i in tmp_usr.decrypt_user_data()]
				elif username==session_username:
					tmp_usr = User(username, "", False)
					tmp_usr.logging_in = True
					_ = [print({username: i}) for i in tmp_usr.decrypt_user_data(session_key)]
				else:
					_ = [print({username: i}) for i in self.decrypt_user_data()]
		else:
			session_keys = self.authorities.get_all_session_keys()
			for username in os.listdir(self.user_dir):
				username = username[:-4]
				tmp_usr = User(username, "", False)
				tmp_usr.logging_in = True
				_ = [print({username: i}) for i in tmp_usr.decrypt_user_data(session_keys[username])]
