import MySQLdb
import logging
from shelf import populate

logging.basicConfig(filename='lib.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
conn = MySQLdb.connect(host='localhost', database='library', user='root', password='krish@12345')
cursor = conn.cursor()

master = ['librarian07', 'lib@12345']


class User():

    def __init__(self, uname, upwd):
        self.username = uname
        self.password = upwd

    def show_catalog(self):
        print("\t\t\t\t\t******LIBRARY CATALOG*****")
        cursor.execute("select distinct genre from book ")
        all_genre = cursor.fetchall()

        i = 1
        for ind_genre in all_genre:
            print("{}. {}:-".format(i, ind_genre[0]))
            total = cursor.execute("select name from book where genre='%s'" % ind_genre[0])
            genre_books = cursor.fetchall()
            z = 1
            for ind_book in genre_books:
                print("\t\t\t{}. {}".format(z, ind_book[0]))
                z += 1
            print("\t\t---> Total Books:- {}".format(total))
            i += 1

    def borrow_book(self):
        cursor.execute("select name from book where status='AV'")
        book_list = cursor.fetchall()
        print('The following books are available in library:-\n')
        i = 1
        for bk in book_list:
            print('{}. {}'.format(i, bk[0]))
            i += 1
        inp = int(input("Chose the book you wish to borrow: "))
        try:
            str = "update credentials set book_borrowed='%s' where username='%s'"
            cursor.execute(str % (book_list[inp - 1][0], self.username))
            cursor.execute("update book set status='BU' where name='%s'" % book_list[inp - 1])
            conn.commit()
            logging.info("{} issued from library".format((book_list[inp - 1][0])))
            print('Book issued successfully!!')
            print('Database Updated!')

        except:
            conn.rollback()
            print('Error')

    def return_book(self):
        command = "select book_borrowed from credentials where username ='%s'"
        cursor.execute(command % self.username)
        val = cursor.fetchone()
        if val[0] == None or val[0] == 'None':
            print('Sorry..You have no book to return')
        else:
            print('Are you sure you want to return the following book(y\\n)\n--->{}'.format(val[0]))
            ans = input("--->")
            if ans == 'y':
                try:
                    str = "update credentials set book_borrowed='%s' where username='%s'"
                    cursor.execute(str % (None, self.username))
                    cursor.execute("update book set status='AV' where name='%s'" % val[0])
                    conn.commit()
                    logging.info("{} returned to the library".format(val[0]))
                    print('Book Returned!!!')
                    print('Database Successfully Updated!!!')
                except:
                    conn.rollback()
                    print('ERROR!!')

    def reserve_book(self):
        cursor.execute("select name from book where status='BU'")
        book_rows = cursor.fetchall()
        print('The following borrowed books can be reserved:-\n--->')
        i = 1

        for x in book_rows:
            print("{}. {}".format(i, x[0]))
            i += 1
        inp = int(input('Enter the serial number of book to reserve: '))
        res_book = book_rows[inp - 1]
        try:
            cursor.execute(
                "update book set status='BR', reserved_by= '%s' where name='%s'" % (self.username, res_book[0]))
            str1 = "update credentials set book_reserved='%s' where username='%s'"
            tpl = (res_book[0], self.username)
            cursor.execute(str1 % tpl)
            conn.commit()
            print('The chosen book has been reserved....')
            print('Database Updated!!!')
        except:
            conn.rollback()
            print('ERROR!!')


class Librarian():

    def add_book(self, name, author, isbn, genre):
        try:
            str = "insert into book(NAME, AUTHOR, ISBN, genre, status) values('%s','%s', '%s', '%s', 'AV')"
            cursor.execute(str % (name, author, isbn, genre))
            conn.commit()
            print('Book added to the database!!!')
        except:
            conn.rollback()
            print('ERROR!!!')

    def remove_book(self, name):
        cursor.execute('select name from book')
        all_books = cursor.fetchall()
        book_flag = False
        for book in all_books:
            if name == book[0]:
                book_flag = True

        if book_flag:
            try:
                cursor.execute("delete from book where name='%s'" % name)
                cursor.execute("update credentials set book_borrowed='None' where book_borrowed='%s'" % name)
                cursor.execute("update credentials set book_reserved='None' where book_reserved='%s'" % name)
                conn.commit()
                print('Book deleted from database')
            except:
                conn.rollback()
                print('ERROR!!!')
        else:
            print('The entered book dose not exist in the database....')

    def get_books_count(self):
        tot = cursor.execute("select * from book")
        ava = cursor.execute("select * from book where status='AV'")
        print("Total books in library: {}\nBooks Available to borrow: {}\nBooks Borrowed: {} ".format(tot, ava,
                                                                                                      tot - ava))

    def popuate_book(self):
        file = input('Paste the path of excel workbook you want to populate database with:-\n--->')
        sheet = input('Enter sheet number:- ')
        populate(file, sheet)

    def reg_users(self):
        cursor.execute("select username, book_borrowed, book_reserved from credentials")
        data_rows = cursor.fetchall()
        print("\t\tNAME\t\t\t\tBOOK BORROWED\t\t\t\tBOOK RESERVED\n")
        for row in data_rows:
            print("\t\t{}\t\t\t\t{}\t\t\t\t\t\t{}".format(row[0], row[1], row[2]))

def login(name, password):
    if name == master[0]:
        if password == master[1]:
            return 'LIBRARIAN'

    else:
        cursor.execute('select * from credentials')
        cred_rows = cursor.fetchall()
        login_flag = False
        for cred in cred_rows:
            if name == cred[0]:
                if password == cred[1]:
                    login_flag = True

        return login_flag


def end():
    cursor.close()
    conn.close()
    exit()


print("\t\t\t\t\t******WELCOME TO THE LIBRARY PORTAL******")
print("1. SIGN IN\n2. SIGN UP")
inp = input("---> ")

if inp == '1':

    user_name = input('Username: ')
    user_pwd = input('Password: ')

    check = login(user_name, user_pwd)

    if check == 'LIBRARIAN':
        librarian = Librarian()
        print("\t\t\t\t\t\n*****CHOSE ONE OF THE FOLLOWING*****")
        print("1. ADD A BOOK")
        print("2. REMOVE A BOOK")
        print("3. GET BOOKS COUNT")
        print("4. POPULATE LIBRARY DATABASE")
        print("5. VIEW REGISTERED USERS")
        print("6. LOG OUT")

        while True:
            command = input('\nEnter your choice:- ')
            if command == '1':
                bk_name = input('NAME: ')
                bk_author = input('AUTHOR: ')
                bk_isbn = input('ISBN: ')
                bk_genre = input('GENRE: ')
                librarian.add_book(bk_name, bk_author, bk_isbn, bk_genre)
            elif command == '2':
                name_book = input('Enter name of the book: ')
                librarian.remove_book(name_book)
            elif command == '3':
                librarian.get_books_count()
            elif command == '4':
                librarian.popuate_book()
            elif command == '5':
                print("\t\t\t\t\tREGISTERED USERS\n")
                librarian.reg_users()
            elif command == '6':
                print("LOGGING OUT!!!")
                end()
            else:
                print('Invalid input try again....')


    elif check:
        user = User(user_name, user_pwd)

        print("\n*****CHOSE ONE OF THE FOLLOWING*****")
        print("1. ISSUE BOOK")
        print("2. RETURN BOOK")
        print("3. RESERVE BOOK")
        print("4. SHOW CATALOG")
        print("5. LOG OUT")

        while True:
            com = input('\nEnter your choice: ')

            if com == '1':
                cursor.execute("select book_borrowed from credentials where username='%s'" % user_name)
                val = cursor.fetchone()
                print(val[0], type(val[0]))
                if val[0] == 'None':
                    user.borrow_book()
                else:
                    print('Sorry you have already borrowed a book....')

            elif com == '2':
                user.return_book()

            elif com == '3':
                user.reserve_book()

            elif com == '4':
                user.show_catalog()

            elif com == '5':
                print('*******Thank You******')
                end()
            else:
                print('Invalid input try again....')

    else:
        print('INVALID USER')
        end()

elif inp == '2':
    u_name = input("Enter Username: ")
    u_pass = input("Enter Password: ")
    cursor.execute("select username from credentials")
    all_users = cursor.fetchall()
    user_flag = True
    for user in all_users:
        if u_name == user[0]:
            user_flag = False
    if user_flag:
        try:
            cursor.execute("insert into credentials values('%s', '%s', 'NULL', 'NULL')" % (u_name, u_pass))
            conn.commit()
            print("NEW USER REGISTERED...")
            print("USER DATABASE SUCCESSFULLY UPDATED...")
            print("PLEASE VISIT AGAIN...")
            end()

        except:
            conn.rollback()
            print("ERROR!!!")
            end()
    else:
        print("Username already exists...")
else:
    print("INVALID INPUT!!!")
    print("TERMINATING...")
    end()
