import mysql.connector as Dm
import dotenv as de
import random as rn
import pickle as Pl
import pathlib as ph
import socket as sc
import os, string
import keyring

class Mod:
    def __init__(self, User, Passkey, Name):

        self.User = User
        self.Pass = Passkey
        self.Name = Name

        os.chmod(ph.Path('Root.env'), mode = 440)

        de.load_dotenv('Root.env')

        if keyring.get_password(sc.gethostbyname(sc.gethostname()), os.getenv('User')) is not None and os.path.exists('Pass.bin'):

            self.Con = Dm.connect(host = sc.gethostbyname(sc.gethostbyname(sc.gethostname())), user = os.getenv('User'), password = keyring.get_password(sc.gethostbyname(sc.gethostname()), os.getenv('User')))

            os.chmod(ph.Path('Root.env'), mode = 000)
            os.chmod(ph.Path('Pass.bin'), mode = 440)

            open('Pass.bin', 'wb').write((''.join('\x00' for l in range(os.path.getsize('Pass.bin')))).encode())

            os.remove('Pass.bin')

        elif not(os.path.exists('Pass.bin')):

            self.Con = Dm.connect(host = sc.gethostbyname(sc.gethostname()), user = os.getenv('User'), password = keyring.get_password(os.getenv('Id'), os.getenv('User')),)

        else:

            keyring.set_password(sc.gethostbyname(sc.gethostname()), os.getenv('User'), bytes.fromhex(Pl.load(open('Pass.bin', 'rb'))[0]).decode())

            open('Pass.bin', 'wb').write((''.join('\x00' for l in range(os.path.getsize('Pass.bin')))).encode())
            open('Pass.bin', 'wb').close()

            os.remove('Pass.bin')


    def Cret_User(self, Host, Cde, Domain = 'null'):

        if self.Con.is_connected():
            Cur = self.Con.cursor()
            self.elemets = ()
            Cur.execute(f'create table PUB.{self.User} (No int primary key, DIR varchar(100) not null, FILE longblob not null, NAME varchar(100) not null);')
            Cur.execute(f'insert into DAT.USER_51611 values (\'{Cde}\', \"{self.User}\", \"{self.Pass}\", \"{Host}\",\"{self.Name}\", \'{Domain}\');')
            self.Con.commit()
            Cur.close()


    def show_files(self, dir):

        if self.Con.is_connected():
            Cur = self.Con.cursor()
            Cur.execute(f'select NAME from PUB.{self.User} where DIR = \"{dir}\";')
            Val = Cur.fetchall()
            Cur.close()

            Var = list()
            
            for l in Val:
                Var.append(l[0])

            return Var
            

    def load_dir(self):

        if self.Con.is_connected():
            Cur = self.Con.cursor()
            Cur.execute(f'select distinct(DIR) from PUB.{self.User};')
            Val = Cur.fetchall()
            Cur.close()
            return Val


    def add_domain(self, Host):
        if self.Con.is_connected():
            Cur = self.Con.cursor()
            self.Domain = ''
            self.Res = False
            Cur.execute(f'create database {self.Domain};')
            Cur.execute(f'update DAT.USER_51611 set Domain =\'{Host}\' where = User = {self.User};')
            Cde = str(self.Domain)[0] + str(self.Domain)[-1] + (''.join(rn.sample(string.digits, k = 5)))
            Cur.execute(f'insert into DAT.DOMAIN_78371 values (\'{Cde}\', \"{self.Domain}\", \'{Host}\')')
            self.Con.commit()
            Cur.close()

            self.Cde = ''.join(rn.sample([l for l in self.User.decode()], k = 5)) + ''.join(rn.sample(string.digits(), k = 5))


            def Wizard():

                Cur = self.Con.cursor()
                Cur.execute(f'create table {self.Domain}.hierarchy_chart (ROLE varchar(20) not null, SUDO char(5) not null, CDE int not null unique);')
                Cur.execute(f'create table {self.Domain}.member_list (MEID char(10 primary key), NAME varchar(50) not null), UID char(8), UNAME varchar(224) not null, ROLE int not null);')
                Cur.execute(f'create table {self.Domain}.FILE_LOG (FID int primary key, MEID not null);')
                Cur.execute(f'insert into {self.Domain}hierarchy_chart values(\'ROOT\', \'TRUE\', {int(''.join(str(ord(l)) for l in 'ROOT'))}')

                self.Con.commit()
                Cur.close()


                
            if self.Res:
                pass


    def add_file(self, dir, file, name):

        Cur = self.Con.cursor()
        Cur.execute(f'insert into PUB.{self.User} (DIR, FILE, NAME) values (\"{dir}\", \"{file}\", \"{name}\")')
        self.Con.commit()
        Cur.close()


    def acess_files(self, file, dir):
        Cur = self.Con.cursor()
        Cur.execute(f'select FILE from PUB.{self.User} where DIR = \"{dir}\" and NAME = \"{file}\";')
        Val = Cur.fetchone()[0]
        Cur.close()
        return Val


    def search(self, e):
        Cur = self.Con.cursor()
        Cur.execute(f'select {e} from DAT.USER_51611 where user = \"{self.User}\";')
        Val = Cur.fetchone()
        Cur.close()

        if Val is not None:
            return Val[0]

        else:
            return None


    def delete(self, dir, file):

        if self.Con.is_connected():
            Cur = self.Con.cursor()
            if file is None:
                Cur.execute(f'delete from PUB.{self.User} where DIR = \"{dir}\"')

            else:
                Cur.execute(f'delete from pub.{self.User} where DIR = \"{dir}\" and \"{file}\"')

            self.Con.commit()
            Cur.close()


    def domain_lst(self, user):

        Val = []

        if self.Con.is_connected():
            if user is None:
                Cur = self.Con.cursor()
                Cur.execute('select Domain, Host, Acess_Word from dat.domain_78371')
                for l in Cur.fetchall():
                    Val.append(l)

                return Val

            else:
                pass


    def close(self):

        self.Con.commit()
        self.Con.close()

