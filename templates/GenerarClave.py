import bcrypt

password = "PasswordTemporal123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(hashed.decode())

