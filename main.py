# imports
import os
import shutil

# useful shortcuts
scat = 'scat'
original_dir = os.getcwd()
encoding = 'ascii'

# creating folder function
def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def create_type(name_of_type, num_of_fields, field_sizes, field_names):
    os.chdir(original_dir)
    # creating scat file if not exists, if exists reading it
    try:
        scat_file = open(scat, 'x', encoding=encoding)
    except:
        scat_file = open(scat, 'a', encoding=encoding)

    # counting existing type number using another function

    types_data = str(list_all_types())

    type_counter=0
    for string in types_data:
        if string == '\n':
            type_counter = type_counter + 1

    if type_counter > 9:
        print("database is full of types!")
        return 0

    if types_data.find(name_of_type) != -1:
        print("there is already a type named", name_of_type)
        return 0

    # writing scat data

    file_to_work = str(name_of_type) + ' ' + str(num_of_fields) + ' ' + str(field_sizes) + str(field_names) + '\n'

    scat_file.write(file_to_work)

    scat_file.close()

    # creating folder

    create_folder(name_of_type)
    os.chdir(original_dir)

    print("type is successfully created.")


def delete_type(name_of_type):
    os.chdir(original_dir)
    # opening scat file
    try:
        scat_file = open(scat, encoding=encoding)
        file_to_work = scat_file.read()
        scat_file.close()
    except:
        print("there is not any type at the momennt. you have to create a type first!")
        return 0

    if file_to_work.find(name_of_type) != -1:
        # if that type exists

        position = file_to_work.find(name_of_type)
        position_of_newline = file_to_work.find('\n', position)

        # after finding necessary positions deletes type info
        file_to_work = file_to_work[:position] + file_to_work[(position_of_newline + 1):]

        # writes new version of scat file
        scat_file_edited = open(scat, 'w', encoding=encoding)
        scat_file_edited.write(file_to_work)
        scat_file_edited.close()

        # deletes that type's data
        shutil.rmtree(name_of_type, ignore_errors=True)
        print("type and all related data are successfully deleted.")
    else:
        # if there is no such a type
        print("no such type exists.")



def list_all_types():
    os.chdir(original_dir)
    # reads from scat file
    try:
        scat_file = open(scat, encoding=encoding)
        file_to_work = scat_file.read()
        scat_file.close()
    except:
        return 0

    # counts number of existing types

    line_counter = open(scat, encoding=encoding)
    count = 0
    for line in line_counter:
        count = count + 1
    line_counter.close()

    # finding part
    type_holder = ""
    position_of_newline = 0
    for i in range(0, count):
        position = file_to_work.find(" ", position_of_newline)

        if position_of_newline == 0:
            type = file_to_work[position_of_newline:position]
        else:
            type = file_to_work[position_of_newline + 1:position]

        position_of_newline = file_to_work.find('\n', position)

        # holds all found types at one string

        type_holder = type_holder + type + '\n'

    os.chdir(original_dir)
    return type_holder


def create_record(type_of_record, fields):
    # reads data from scat file
    try:
        scat_file = open(scat, encoding=encoding)
        scat_data = scat_file.read()
        scat_file.close()
    except:
        print("you have to create a type first!")
        os.chdir(original_dir)
        return 0

    try:
        os.chdir(type_of_record) # goes to related directory
    except:
        print("no such type exists.")
        os.chdir(original_dir)
        return 0

    pages = sorted(os.listdir()) # pages' names are collected
    try:
        if (pages[0].startswith('.')): # unnecessary files of macOS
            pages.pop(0)
    except:
        pages = pages

    desired_page = "" # the page all the data will be written into

    # creates first page with id: 001 and isFull: 0
    if '001' not in pages:
        page_file = open('001', 'x', encoding=encoding)
        page_file.write('001 ')
        page_file.write('0\n')
        desired_page = "001"
        page_file.close()

    # if there is 900 pages of a type, it throws an database full error
    if '900' in pages:
        print("database is full of that type's records!")
        os.chdir(original_dir)
        return 0

    #if 001 exists, does usual behaviour
    else:
        for page_id in pages:
            page_file = open(page_id, encoding=encoding)
            file_to_work = page_file.read()
            page_file.close()

            # if isFull equals to 0, then found!
            if file_to_work[4] != '1':
                desired_page = page_id
                break

        # if all existing pages' header says that they are full, creates new page
        if desired_page == "":
            # page name settings
            if len(pages) < 9:
                desired_page = '00' + str(int(pages[-1]) + 1)
            if len(pages) < 99 and len(pages) >= 9:
                desired_page = '0' + str(int(pages[-1]) + 1)
            if len(pages) >= 99:
                desired_page = str(int(pages[-1]) + 1)

            # after creating page, writes header
            page_file = open(desired_page, 'x', encoding=encoding)
            page_file.write(desired_page + ' ')
            page_file.write('0\n')
            page_file.close()

    # writes info of record into page
    page_file = open(desired_page, 'a', encoding=encoding)
    page_file.write('0 ' + fields + '\n') # 0 for is_deleted
    page_file.close()

    print("record is successfully created.")

    position=0
    position_of_new_line=0

    # finally it checks for if the page is full now?
    for i in range(0,len(scat_data)):
        position = scat_data.find(type_of_record)
        position_of_new_line = scat_data.find('\n', position)

    scat_data = scat_data[position:position_of_new_line]

    # lets calculate maximum page size
    calc = scat_data.split() # scat_data has become a list named calc
    num_of_fields = int(calc[1]) # second element of calc is num of fields
    header_size = 5 # it is 5 and fixed for every page

    # finding total field sizes
    field_sizes = 0
    for i in range(0, num_of_fields):
        field_sizes = field_sizes + int(calc[i+2])
    maximum_records = (1000-header_size)/(field_sizes+num_of_fields)
    maximum_records = int(maximum_records)-1 # making it an integer and being sure of not exceeding 1KB

    # lets see is page full
    page_file = open(desired_page, encoding=encoding)
    line_count = -1 # starts from -1 not to include header
    for line in page_file:
        line_count = line_count + 1
    page_file.close()

    # updates it if is full
    if line_count == maximum_records:
        page_file = open(desired_page, encoding=encoding)
        file_to_work = page_file.read()
        file_to_work = file_to_work[:4]+'1'+file_to_work[5:] # changing part
        page_file_edited = open(desired_page, 'w', encoding=encoding)
        page_file_edited.write(file_to_work)
        page_file.close()

    # going back to original directory for further operations
    os.chdir(original_dir)


def delete_record(type_of_record, primary_key):
    try:
        os.chdir(type_of_record) # goes to related directory
    except:
        print("no such type exists.")
        os.chdir(original_dir)
        return 0
    pages = sorted(os.listdir()) # pages' names are collected
    try:
        if (pages[0].startswith('.')): # unnecessary files of macOS
            pages.pop(0)
    except:
        pages = pages

    if len(pages) == 0:  # if there is no page, then stop
        print("there is no record.")
        os.chdir(original_dir)
        return 0

    found = False

    for page_id in pages:
        page_file = open(page_id, encoding=encoding)
        page_data = page_file.read()
        page_file.close()

        # after reading data, looks for primary key
        position = page_data.find(primary_key, 4)
        print(page_data[position-3])
        while(page_data[position-3]!='\n'):
            oldpos = position
            position = page_data.find(primary_key, oldpos+1)
        print("çıktım")
        position_of_deleted = position - 2 # 2 spaces before primary key is isDeleted info

        if position != -1:
            found = True

        page_data_edited = page_data[:position_of_deleted]+'1'+page_data[position_of_deleted+1:] # changing 0 to 1 for is_deleted

        # writing changed version
        page_file = open(page_id, 'w', encoding=encoding)
        page_file.write(page_data_edited)
        page_file.close()

    if found:
        print("record is successfully deleted.")
    else:
        print("cannot find record.")
    # going back to original directory for further operations
    os.chdir(original_dir)


def search_record(type_of_record, primary_key):
    os.chdir(original_dir)
    # reads data from scat file
    try:
        scat_file = open(scat, encoding=encoding)
        scat_data = scat_file.read()
        scat_file.close()
    except:
        print("you have to create a type first!")
        os.chdir(original_dir)
        return 0

    try:
        # finds field names in scat file
        field_position1 = scat_data.find(type_of_record)
        field_position2 = scat_data.find("\n", field_position1)
        type_details = scat_data[field_position1:field_position2]
        type_details = type_details.split()
        field_num = type_details[1]
        field_names = list()
        for i in range(0, int(field_num)):
            field_names.append(type_details[i+2+int(field_num)])

        os.chdir(type_of_record) # goes to related directorys
        pages = sorted(os.listdir()) # pages' names are collected
        try:
            if (pages[0].startswith('.')):  # unnecessary files of macOS
                pages.pop(0)
        except:
            pages = pages

        if len(pages) == 0: # if there is no page, then stop
            print("there is no record.")
            os.chdir(original_dir)
            return 0

        found = False

        for page_id in pages:
            page_file = open(page_id, encoding=encoding)
            page_data = page_file.read()
            page_file.close()

            # after reading data, begins searching starting from where the header ends
            page_data_list = page_data.split()
            search_result = list()
            for i in range(3, len(page_data_list), int(field_num)+1):
                if page_data_list[i]==primary_key:
                    found = True
                    for j in range(i-1, int(field_num)+i):
                        search_result.append(page_data_list[j])
                    break
            search_result_without_isdeleted = search_result[1:]
            search_result_final = "" # trying to add field name before fields
            for i in range(0, int(field_num)):
                search_result_final = search_result_final + str(field_names[i]) + ': ' + str(search_result_without_isdeleted[i]) + ' '
            if found:
                if search_result[0]=='1':
                    # if record is deleted
                    listening = input("this record has been deleted. if you still want to see it, type y\n")
                    if listening == "y":
                        print(search_result_final)
                        found = False
                else:
                    print(search_result_final)
                    found = False
    except:
        # going back to original directory for further operations
        os.chdir(original_dir)
        print("no such type exists")


def list_all_records(type_of_record):
    try:
        # reads scat file to know how many fields it has and how big these fiels are
        scat_file = open(scat, encoding=encoding)
        scat_data = scat_file.read()
        scat_file.close()
        scat_type_position = scat_data.find(type_of_record)
        scat_type_position = scat_data.find(' ', scat_type_position)
        os.chdir(type_of_record) # goes to related directory
        pages = sorted(os.listdir()) # pages' names are collected
        try:
            if (pages[0].startswith('.')):  # unnecessary files of macOS
                pages.pop(0)
        except:
            pages = pages

        # finds field names in scat file
        field_position1 = scat_data.find(type_of_record)
        field_position2 = scat_data.find("\n", field_position1)
        type_details = scat_data[field_position1:field_position2]
        type_details = type_details.split()
        field_num = type_details[1]
        field_names = list()
        for i in range(0, int(field_num)):
            field_names.append(type_details[i+2+int(field_num)])

        if len(pages) == 0: # if there is no page, then stop
            print("there is no record.")
            os.chdir(original_dir)
            return 0

        for page_id in pages:
            page_file = open(page_id, encoding=encoding)
            page_data = page_file.read()
            page_file.close()

            # lists records by using new lines
            second_new_line=0
            while second_new_line!=-1:

                first_new_line = page_data.find('\n', second_new_line)
                second_new_line = page_data.find('\n', first_new_line + 1)
                fields_info = (page_data[first_new_line + 3:second_new_line]).split()
                final_print = ""
                for i in range(0, len(fields_info)):
                    final_print = final_print + field_names[i]+': '+fields_info[i] + ' '
                try:
                    if page_data[first_new_line+1]!='1':
                        print(final_print)
                    else:
                        print(final_print + "(deleted)")
                except:
                    continue

        # going back to original directory for further operations
        os.chdir(original_dir)
    except:
        print("no such type exists.")


# end user

welcome = input("welcome, please type what you want to do. you can use create type, delete type, list all types, create record, delete record, search record or list all records!\n")

while welcome != "quit":

    if welcome == "create type":

        # max length of name is 10
        name_of_type = ""
        while len(name_of_type) > 10 or len(name_of_type) == 0:
            name_of_type = input("name of type to be created?\n")

        # max num of fields is 5
        num_of_fields = 6
        while int(num_of_fields) > 5:
            num_of_fields = input("number of field(s) of that type?\n")
            if num_of_fields == '':
                num_of_fields = 6

        # max length of field sizes are 10
        field_sizes = ""
        for i in range(1, int(num_of_fields)+1):
            field_size = 11
            while int(field_size) > 10:
                print('size of field {} of that type?'.format(i))
                field_size = input()
            field_sizes = field_sizes + str(field_size) + ' '

        # max length of field names are totally 10*num of fields
        field_names = ""
        space_counter = int(num_of_fields)-1
        while len(field_names) > (int(num_of_fields)*10+space_counter) or len(field_names) == 0:
            field_names = input("names of field(s) of that type?\n")

        # finally sends to function
        create_type(name_of_type, num_of_fields, field_sizes, field_names)

    if welcome == "delete type":
        name_of_type = input("name of type to be deleted?\n")
        delete_type(name_of_type)

    if welcome == "list all types":
        if list_all_types()!=0:
            print("here are the existing types:")
            print(list_all_types()[:-1]) # not to include latest new line
        else:
            print("you have to create a type first!")

    if welcome == "create record":
        type_of_record = input("type of record to be created?\n")
        fields = input("field(s)?\n")
        create_record(type_of_record, fields)

    if welcome == "delete record":
        type_of_record = input("type of record to be deleted?\n")
        primary_key = input("primary key of it?\n")
        delete_record(type_of_record, primary_key)

    if welcome == "search record":
        type_of_record = input("type of record to be searched?\n")
        primary_key = input("primary key of it?\n")
        search_record(type_of_record, primary_key)

    if welcome == "list all records":
        type_of_record = input("name of type to be listed with all of its records?\n")
        list_all_records(type_of_record)

    welcome = input("your next command?\n")

os.chdir(original_dir)
