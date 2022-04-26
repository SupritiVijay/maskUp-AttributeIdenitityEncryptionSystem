import os

class State:
	def __init__(self, user_dir="./users/"):
		if not os.path.exists(user_dir):
			os.mkdir("users")
			user_df = pd.DataFrame({"user_id": [], "password": []})

	def menu(self):
		user_name = input("Enter login:\t").strip()
		password = input("Enter password:\t").strip()


if __name__ == '__main__':
	state = State()
	state.main()