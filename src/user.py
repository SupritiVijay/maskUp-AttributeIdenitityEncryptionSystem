from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import pickle
import os

class User:
	def __init__(self, username, user_session_key_path="./data/user_sess.dat", user_dir="./data/users/"):
		self.user_session_key_path = user_session_key_path
		self.username = username
		session_key = self.get_session_key()
		self.aes = AES.new(session_key, AES.MODE_ECB)
		self.user_dir = user_dir

	def get_session_key(self):
		if not os.path.exists(self.user_session_key_path):
			with open(self.user_session_key_path, "wb") as f:
				session_key = get_random_bytes(16)
				pickle.dump({self.username: session_key}, f)
				return session_key
		else:
			with open(self.user_session_key_path, "rb") as f:
				dat = pickle.load(f)
			if self.username not in dat.keys():
				session_key = get_random_bytes(16)
				dat.update({self.username: session_key})
				with open(self.user_session_key_path, "wb") as f:
					pickle.dump(dat, f)
			return dat[self.username]

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
		if session_key is None:
			session_key = self.get_session_key()
		aes = AES.new(session_key, AES.MODE_ECB)
		path = self.user_dir+self.username+".dat"
		if not os.path.exists(path):
			print("No data stored...")
		else:
			with open(path, "rb") as f:
				dat_savable = pickle.load(f)
				for query in dat_savable:
					data = query["data"]
					encrypted_words = query["encrypted_words"]
					for encrypted_word in encrypted_words:
						decrypted_word = aes.decrypt(encrypted_word)
						data = data.replace(encrypted_word, decrypted_word.strip())
					print(data)

