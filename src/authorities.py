from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import pickle

class Authorities:
	def __init__(self, username, password, sess_id="./data/sess.dat"):
		self.sess_id = sess_id
		self.username = username
		self.password = password
		if self.username == 'admin' and self.password == 'admin':
			self.logged_in = True
		else:
			self.logged_in = False
		if not os.path.exists("./.platform/authority_public.key"):
			key = RSA.generate(2048)
			private_key = key.export_key()
			with open("./.authorities/authority_private.key", "wb") as f:
				f.write(private_key)
			public_key = key.publickey().export_key()
			with open("./.platform/authority_public.key", "wb") as f:
				f.write(public_key)

	def get_all_session_keys(self):
		if self.logged_in:
			with open(self.sess_id, "rb") as f:
				data = pickle.load(f)
			session_keys = {}
			with open("./.authorities/authority_private.key", "rb") as f:
				private_key = RSA.import_key(f.read())
			cipher_rsa = PKCS1_OAEP.new(private_key)
			for key, item in data.items():
				session_key = cipher_rsa.decrypt(item)
				session_keys.update({key: session_key})
			return session_keys
		else:
			return 0