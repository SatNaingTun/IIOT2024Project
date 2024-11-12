# import bcrypt

# def hash_password(password):
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed

# def check_password(hashed, user_password):
#     return bcrypt.checkpw(user_password.encode('utf-8'), hashed)

# if __name__ == "__main__":
#     password = getpass.getpass("Enter your password: ")
#     hashed_password = hash_password(password)
#     print(f"Hashed password: {hashed_password}")

#     # To verify the password later
#     user_password = getpass.getpass("Re-enter your password: ")
#     if check_password(hashed_password, user_password):
#         print("Password match!")
#     else:
#         print("Password does not match.")