import pandas as pd
import MySQLdb
conn = MySQLdb.connect(host='localhost', database = 'library', user='root', password='krish@12345')
cursor = conn.cursor()


def populate(file, sheet):
        df = pd.read_excel(file,sheet)
        df.set_index('Sr.' ,inplace=True)
        for name, author, isbn, genre in zip(df.NAME, df.AUTHOR, df.ISBN, df.GENRE):
                try:
                        str1= "insert into book(NAME, AUTHOR, ISBN, genre, status) values('%s','%s', '%s', '%s', '%s')"
                        tpl = (name, author, str(isbn), genre, 'AV')
                        cursor.execute(str1 % tpl )
                        conn.commit()

                except:
                        conn.rollback()
                        print('ERROR!!!')
                        break
        else:
                print('Database successfully populated!!!')
