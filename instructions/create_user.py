print()
print("Create user that will be executing app functions in database with following command:")
print("CREATE USER library_user WITH PASSWORD '123';")
print()
print("In next step give this user premmision to connect to database:")
print("GRANT CONNECT ON DATABASE library TO library_user;")
print()
print("Then give him premmision to manage table data database:")
print("GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE book TO library_user;")
print()
