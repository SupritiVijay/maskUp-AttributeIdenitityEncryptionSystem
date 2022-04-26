import os
from src.platform import Platform
from src.user import User

class State:
	def __init__(self):
		self.platform = Platform()

	def menu(self):
		os.system("cls")
		#try:
		if True:
			option = int(input("----MENU----\n\t1. Login\n\t2. Register\n\t3. Browse\n\nEnter option:\t"))
			if option in [1, 2]:
				user_name = input("Enter user name:\t").strip()
				password = input("Enter password:\t").strip()
				if option==2:
					return self.platform.register_new_user(user_name, password)
				else:
					response = self.platform.login_user(user_name, password)
					if response:
						user = User(user_name)
						response = input("Do you wish to enter new data or view your own decrypted data? (Y/N)")
						if response.lower()=="y":
							user.instance()
						user.decrypt_user_data()
					else:
						print("Invalid Login Details...")
						return 0
		#except:
		if False:
			print("INVALID OPTION ERROR EXITING...")
			return 0

	def main(self):
		self.menu()
		
if __name__ == '__main__':
	state = State()
	state.main()