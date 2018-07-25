# simpledbms
a simple database management system with python

This project is the implementation of a simple database system design.
In order to use it most efficient way, user should put main.py file into an empty folder. After that; main.py file should be run with Python3; Python2 will throw error, this implementation is not compatible with Python2. main.py file should not be put on main directory. It has to have writing and reading consents.
After running, user should start with creating type. "create type" input will convey user to do that. After creating a type; user can use one of the following commands: "delete type", "list all types", "create record", "delete record", "search record" and "list all records".
Creating type needs a name of type, number of fields, sizes of fields, name of fields.
Deleting type needs a name of type.
Listing all types needs nothing.
Creating record needs name of type and fields.
Deleting record needs primary key and name of type. Primary key is first field of every record. It has to be unique.
Searching record needs primary key and name of type.
Listing all records needs name of type.
According to interpreter user use and default system language; encoding errors may occur. This rarely happens but can be solved by changing 'ascii' coding to 'latin-1' or 'utf-8' inside of main.py.
Code has many comments to be comprehensible.
None of the files including scat file and pages should be edited by hand. If there is a demand to do something, the system exists for satisfying that.
There is a folder named example. It has a few types and records. User can test it after extracting.
Hope you like it!
