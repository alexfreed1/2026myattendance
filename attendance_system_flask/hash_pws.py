import bcrypt

print("Hashed passwords for init_db.sql (copy the hashed values):")
print()

print("'admin' password (admin123):")
hashed_admin = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
print(f"  hashed = '{hashed_admin}'")
print()

print("'john' password (john123):")
hashed_john = bcrypt.hashpw(b"john123", bcrypt.gensalt()).decode()
print(f"  hashed = '{hashed_john}'")
print()

print("'mary' password (mary123):")
hashed_mary = bcrypt.hashpw(b"mary123", bcrypt.gensalt()).decode()
print(f"  hashed = '{hashed_mary}'")
print()
print("Replace plain passwords in init_db.sql INSERT statements, then run in Supabase SQL Editor.")
