import customtkinter as ctk
import pathlib as ph
import random as rn
import pypdf as pdf
import threading as th
import concurrent.futures as ct
import pymupdf as pdfm
import Main, keyring, io
import json, socket, os, string, uuid, ipaddress
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet as Frt
from CTkMessagebox import CTkMessagebox
from CTkMessagebox.ctkmessagebox import CTkMessagebox as MB
from PIL import Image



class Log:

    def __init__(self):

        ctk.FontManager.load_font('Operation Napalm.ttf')
        

        self.Win = ctk.CTk()
        self.Win._set_appearance_mode('dark')

        self.Font = ctk.CTkFont(family = 'Operation Napalm', size = 17, weight = 'normal')
        self.Tfont = ('Courier New', 17)

        self.Win.title('DATLink :  Login')
        self.Win.geometry('300x270')
        self.Win.resizable(False, False)

        self.Lb1 = ctk.CTkLabel(self.Win, text = 'Welcome!', font = self.Font, text_color= '#029CFF')
        self.Lb1.pack(padx = (10, 10), pady = (7, 7))

        self.Frm1 = ctk.CTkFrame(self.Win, corner_radius = 5)
        self.Frm1.pack(padx = (5, 5),  pady = (0, 7))

        self.Lb2 = ctk.CTkLabel(self.Frm1, text = 'User :', font = self.Font)
        self.Lb2.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.Uname = ctk.CTkEntry(self.Frm1, font = self.Tfont, corner_radius = 5)
        self.Uname.grid(row = 0, column = 1, padx = 5, pady = (5, 5))
        
        self.Lb3 = ctk.CTkLabel(self.Frm1, text = 'Passkey :', font = self.Font)
        self.Lb3.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.Pass = ctk.CTkEntry(self.Frm1, font = self.Tfont, show = '*', corner_radius = 5)
        self.Pass.grid(row = 1, column = 1, padx = (5, 5), pady = (5, 5))

        self.Bt1 = ctk.CTkButton(self.Win, text = 'Login', font = self.Font, corner_radius = 5, command = self.Login)
        self.Bt1.pack(pady = (0, 7))

        self.Val1 = ctk.IntVar(self.Win, value = 0)

        self.Ct1 = ctk.CTkCheckBox(self.Win, text = 'Admin' ,font = self.Font, variable = self.Val1, offvalue = 0, onvalue = 1)
        self.Ct1.pack(padx = 20, side = 'left')

        self.Ct1.configure(state = 'disabled')

        self.Val2 = ctk.IntVar(self.Win, value = 0)

        self.Sth1 = ctk.CTkSwitch(self.Win, text = 'Domain', font = self.Font, variable = self.Val2, offvalue = 0, onvalue = 1, command = self.Act_Dmn)
        self.Sth1.pack(padx = (5, 5), pady = 5)

        self.Bt2 = ctk.CTkButton(self.Win, text = 'Create User' ,font = self.Font, command = self.Create_Us, corner_radius = 5)
        self.Bt2.pack(pady = (0, 10), padx = (0, 15), side = 'bottom')


        self.Win.bind('<Alt-c>', lambda e: self.Win.destroy())
        self.Win.bind('<Return>', lambda e : self.Login())
        

        self.Win.mainloop()
       

    def Gen_Key(self, Key):

        Gen = hashes.Hash(hashes.SHA224())
        Gen.update(str(Key).encode())
        Lc =  Gen.finalize()

        return Lc.hex()


    def Login(self):

        os.chmod(ph.Path('User.json'), mode = 222)

        Data = json.load(open(ph.Path('User.json')))
        if self.Gen_Key(self.Uname.get()) in tuple(dict(Data).keys()):
            if self.Gen_Key(self.Pass.get()) == Data[self.Gen_Key(self.Uname.get())][0]:
                self.Win.bind('<Return>', lambda : None)
                self.Win.after(300, self.GUI)
        
        
            else:
                self.Pass.delete(0,ctk.END)
                Error(self.Win, 'PassKey').EntryError('Red')

        else:
            self.Pass.delete(0, ctk.END)
            self.Uname.delete(0, ctk.END)
            Error(self.Win, 'User').EntryError('Orange')

        open(ph.Path('User.json')).close()
        os.chmod(ph.Path('User.json'), mode = 200)


    def GUI(self):

        self.Win.withdraw()
        self.Pass.delete(0, ctk.END)
        self.Uname.delete(0, ctk.END)
        self.Bt1.configure(state = 'disabled')

        self.Tp3 = ctk.CTkToplevel(self.Win)
        self.Tp3.focus_set()
        self.Tp3.geometry('915x535')
        self.Tp3.resizable(False, False)
        self.Tp3.title('DATAlink : Creditals')
        self.Tp3.protocol('WM_DELETE_WINDOW', self.Close)

        self.Lb10 = None

        self.Lb11 = ctk.CTkLabel(self.Tp3, text = 'Welcome User', font = self.Font)
        self.Lb11.pack(padx = (5, 5), pady = (5, 5))

        self.Frm3 = ctk.CTkFrame(self.Tp3, corner_radius = 5)
        self.Frm3.pack(anchor = 'nw', pady = (0, 5), padx = (10, 5))

        self.Bt4 = ctk.CTkButton(self.Frm3, text = 'Add Dir', font = self.Font, corner_radius = 5, command = lambda : UserI(self.Tp3, self.Gen_Key(self.Uname.get())).set_root())
        self.Bt4.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.Sth2 = ctk.CTkSwitch(self.Frm3, text = 'Show Private', font = self.Font)
        self.Sth2.grid(row = 1, column = 0, padx = (5, 5), pady = (2, 5))

        self.Frm4 = ctk.CTkFrame(self.Tp3, corner_radius = 5)
        self.Frm4.pack(padx = 5, pady = 5, expand = True, fill = 'both')

        self.Frm5 = ctk.CTkFrame(self.Frm4, corner_radius = 5)
        self.Frm5.pack(padx = 5, pady = 5)

        self.File = ctk.CTkEntry(self.Frm5, font = self.Tfont, corner_radius = 5)
        self.File.grid(row =0, column = 0, padx = 2, pady = 2)

        self.Bt5 = ctk.CTkButton(self.Frm5, text = 'Search File', font = self.Font, corner_radius = 5)
        self.Bt5.grid(row = 0, column = 1, padx = (0, 2), pady = (0, 2))

        self.Frm6 = ctk.CTkFrame(self.Frm4, corner_radius = 5)
        self.Frm6.pack(expand = True, fill = 'both', padx = (5, 5), pady = (5, 5))

        self.Frm7 = ctk.CTkScrollableFrame(self.Frm6, corner_radius = 5)
        self.Frm7.grid(row = 0, column = 0, padx = (5, 5), pady = (5, 5))

        self.Tp3.protocol('VM_DELETE_WINDOW', self.Close)

        
        def Dir_lst():

            for l in Main.Mod(self.Gen_Key(self.Uname.get()), self.Gen_Key(self.Pass.get()), None).load_dir():

                self.Btn = ctk.CTkButton(self.Frm7, text = bytes.fromhex(l[0]).decode(), font = self.Font, fg_color = 'transparent', hover_color=("gray85", "gray25"), command = lambda dir = l[0] : File_lst((dir)))
                self.Btn.pack(padx = (5, 5), pady = (5, 0))


        self.Frm8 = ctk.CTkScrollableFrame(self.Frm6, corner_radius = 5)
        self.Frm8.grid(row = 0, column = 1, padx = (0, 5), pady = (5, 5))

        def File_lst(dir):
            Val = Main.Mod(self.Gen_Key(self.Uname.get()), None, None).show_files(dir)
            for l in Val:
                self.Btn11 = ctk.CTkButton(self.Frm8, corner_radius = 5, font = self.Font, text = bytes.fromhex(l).decode(),  fg_color = 'transparent', hover_color=("gray85", "gray25"), command = lambda file = l, dir = dir : reader(file = file, dir = dir))
                self.Btn11.pack(padx = (5, 5), pady = (5, 0))
                self.Btn.configure('disabled')


        def reader(file, dir):
            PDFReader(user = self.Gen_Key(self.Uname.get()), file = file, Tp = self.Tp3, dir = dir)

        self.Bt9 = ctk.CTkButton(self.Frm3, text = 'Add Files', font = self.Font, corner_radius = 5)
        self.Bt9.grid(row = 0, column = 1, padx = (0, 5), pady = (5, 5))


        def reload_lst():
                self.Bt10.configure(state = 'disabled')

                if self.Frm7.winfo_children() is not None:

                    for l in self.Frm7.winfo_children():
                        l.destroy()

                    if self.Frm8.winfo_children() is not None:
                        for l in self.Frm8.winfo_children():
                            l.destroy()

                    else:
                        pass

                else:
                    pass
                
                self.Tp3.after(2000, lambda : Dir_lst())

                self.Tp3.after(15000, lambda : self.Bt10.configure(state = 'normal'))
                

                
        self.Bt10 = ctk.CTkButton(self.Frm3, text = 'Refresh', font = self.Font, corner_radius = 5, command = reload_lst)
        self.Bt10.grid(row = 0, column = 2, padx = (0, 5), pady =(5, 5))
        #Text = ctk.CTkLabel(self.Frm6, text = )

        #self.Bt4 = ctk.CTkButton(self.Tp3, fg_color = '#242424', border_color =  '#144870', border_width = 2, hover_color = '#7F8C8D').pack()


    def Act_Dmn(self):
       if  self.Val2.get() == 1:
           self.Ct1.configure(state = 'normal')
           self.Req1 = ctk.CTkInputDialog(font = self.Font, text = 'Enter Domain Name', title = 'Domain Acess')

           if self.Req1.get_input() is not None:
                Val = Main.Mod(self.Gen_Key(self.Uname.get()), self.Gen_Key(self.Pass.get()), None).search('Domain')
                print(Val)
                if Val is None:
                    self.Sth1.deselect()
                    Error(self.Win, None).DomainError()

           else:
               self.Ct1.configure(state = 'disabled')
               self.Sth1.deselect()
        

    def Create_Us(self):

        self.Win.withdraw()

        self.Tp2 = ctk.CTkToplevel(self.Win)
        self.Tp2.title('User Setup')
        self.Tp2.geometry('425x325')
        self.Tp2.resizable(False, False)

        def Close():
            self.Tp2.after(1000, self.Win.deiconify())

            self.Tp2.destroy()

        
        self.Tp2.protocol('WM_DELETE_WINDOW', Close)
        

        self.Lb4 = ctk.CTkLabel(self.Tp2, text = 'Set A User', font = self.Font)
        self.Lb4.pack(padx = 5, pady = 5)

        self.Frm2 = ctk.CTkFrame(self.Tp2, corner_radius = 5)
        self.Frm2.pack(padx = (0, 5), pady = 5)

        self.Lb5 = ctk.CTkLabel(self.Frm2, text = 'Name :', font = self.Font)
        self.Lb5.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.Name = ctk.CTkEntry(self.Frm2, font = self.Tfont, corner_radius = 5)
        self.Name.grid(row = 0, column = 1, padx = (5, 5), pady = (5, 5))

        self.Lb6 = ctk.CTkLabel(self.Frm2, text = '(Full Name)', font = self.Font)
        self.Lb6.grid(row = 0, column = 2, padx = 5, pady = 5)

        self.Lb7 = ctk.CTkLabel(self.Frm2, text = 'User :', font = self.Font)
        self.Lb7.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.Unme = ctk.CTkEntry(self.Frm2, font = self.Tfont, corner_radius = 5)
        self.Unme.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.Lb8 = ctk.CTkLabel(self.Frm2, text = "Set Pass :", font = self.Font)
        self.Lb8.grid(row = 2, column = 0, padx = 5, pady = 5)

        self.S_Pass = ctk.CTkEntry(self.Frm2, font = self.Tfont, show = '*', corner_radius = 5)
        self.S_Pass.grid(row = 2, column = 1, padx = 5, pady = 5)

        self.Lb9 = ctk.CTkLabel(self.Frm2, text = 'Renter Same Pass : ', font = self.Font)
        self.Lb9.grid(row = 4, column = 0, padx = 5, pady = 5)

        self.R_Pass = ctk.CTkEntry(self.Frm2, font = self.Tfont, show = '*', corner_radius = 5)
        self.R_Pass.grid(row = 4, column = 1, padx = 5, pady = 5)

        self.Bt3 = ctk.CTkButton(self.Tp2, text = 'Confirm', font = self.Font, command = self.Set_User)
        self.Bt3.pack(padx = 5)


    def Set_User(self):

        def Chk_Pass():
            if self.S_Pass.get() == self.R_Pass.get():
                if 8 < len(self.S_Pass.get()) < 26:
                    if self.Unme.get() != self.Name.get() and self.Name.get().isalpha():
                        return True

                    else:
                        Error(self.Tp2, ': Enter Differnet Uname (Not Name itself)').EntryError('Orange')
                        return False

                else:
                    Error(self.Tp2, 'Creditals').EntryError('Orange')

            else:
                self.S_Pass.delete(0, ctk.END)
                self.R_Pass.delete(0, ctk.END)
                Error(self.Tp2, 'Pass').EntryError('Red')
                return False

        if Chk_Pass():
            Mod = Main.Mod(User = self.Gen_Key(self.Uname.get()), Passkey = self.Gen_Key(self.S_Pass.get()), Name = self.Name.get())

            Data = dict(json.load(ph.Path('User.json').open('r')))
            Data.setdefault(self.Gen_Key(self.Unme.get()), (self.Gen_Key(self.S_Pass.get()), socket.gethostbyname(socket.gethostname())))

            if self.Gen_Key(self.Unme) not in tuple(Data.keys()):
                json.dump(Data, ph.Path('User.json').open('w'))

                CTkMessagebox(self.Tp2, title = 'User Settings', message = 'User has Been Created', font = self.Font, corner_radius = 5, fade_in_duration = 3, icon = 'check')

                Cde = str(self.Name.get()[0]).upper() + str(self.Name.get()[-1]).upper() + (''.join(rn.sample(string.digits, k = 4)))

                Mod.Cret_User(socket.gethostbyname(socket.gethostname()), Cde)

                

                self.Win.after(5000, self.Tp2.destroy())
                self.Win.deiconify()

        else:
            Error(self.Tp2, ': User Exists', ).EntryError('Orange')

            self.Win.after(3000, self.Tp2.destroy())
            self.Win.deiconify()

    
    def Close(self):

        Main.Mod(None, None, None).close()
        self.Win.deiconify()
        self.Tp3.destroy()
        


class Error:
    def __init__(self, root, text):
        self.Font = ctk.CTkFont(family = 'Operation Napalm', size = 17, weight = 'normal')
        self.Root = root
        self.Text = text

    def MessageBox(self, title, mes, color, icon):
        CTkMessagebox(self.Root, message = mes, title = title, text_color = color, font = ('Operation Napalm', 17, 'normal'), corner_radius = 5, fade_in_duration = 3, icon = icon, sound = True)

    def EntryError(self, color):
        Colour = {'Red' : ('#C02226', 'cancel'), 'Orange' : ('#F0792E', 'warning'), 'Green' :( '#009967', 'check'), 'Blue' : ('#144870', 'info'), 'None' : ('#cccccc', 'question')}
        if color in (Colour.keys()):
            self.MessageBox('Entry Error', f'InVALID {self.Text}',Colour[color][0], Colour[color][1])

        else:
            raise ValueError('Incorrect Color')

    def ExistsError(self):
        self.MessageBox('Exits Error', f'{self.Text} Exists', '#F0792E', 'warning')

    def FIleError(self):
        self.MessageBox('File Error', 'No File', '#C02226', 'cancel')

    def DomainError(self):
        self.MessageBox('Domain Error', 'No Domain Exists', '#F0792E', 'warning')

#Incomplete
class UserI:

    def __init__(self, win, user):

        self.Win = win
        self.User = user
        self.Font = ctk.CTkFont(family = 'Operation Napalm', size = 17)
        ctk.ThemeManager.theme['CTkFont'] = {'family' : 'Operation Napalm', 'size' : 17, 'weight' : 'normal'}


    def set_root(self):
        self.Req2 = ctk.CTkInputDialog(text = 'Add Dir ', font = self.Font, title = 'New Dir')
        self.Req_txt = self.Req2.get_input()

        if self.Req_txt is not None:

            self.Tp4 = ctk.CTkToplevel(self.Win)
            self.Tp4.title('Add File')
            self.Tp4.geometry('525x200')
            self.Tp4.resizable(False, False)
            self.Tp4.attributes('-topmost', True)
            self.Tp4.focus_set()

            self.Lb14 = ctk.CTkLabel(self.Tp4, text = f'Add file : {self.Req_txt}', font = self.Font)
            self.Lb14.pack(padx = (5, 5), pady = (5, 5))

            self.Frm6 = ctk.CTkFrame(self.Tp4)
            self.Frm6.pack(padx = (0, 5), pady = (5, 5))

            self.Lb13 = ctk.CTkLabel(self.Frm6, text = 'Name', font = self.Font)
            self.Lb13.grid(row = 0, column = 0, padx = (5, 5), pady = (5, 5))

            self.File = ctk.CTkEntry(self.Frm6, font = self.Font, corner_radius = 5)
            self.File.grid(row = 0, column = 1, padx = (5, 5), pady = (0, 5))

            self.Bt7 = ctk.CTkButton(self.Frm6, font = self.Font, text = 'Choose File', command = self.add_file)
            self.Bt7.grid(row =1, column = 0, padx = (5, 5), pady = (0, 5))

            self.Lb15 = ctk.CTkLabel(self.Frm6, text = 'File :', font = self.Font)
            self.Lb15.grid(row = 2, column = 0, padx = (2, 2), pady = (0, 5))

            self.Val3 = ctk.IntVar(self.Tp4, value = 0)
            self.Ctk2 = ctk.CTkCheckBox(self.Frm6, text = 'Private', font = self.Font, textvariable = self.Val3, offvalue = 0, onvalue = 1)
            self.Ctk2.grid(row = 1, column = 1, padx = (0, 2), pady = (0, 5))

            self.Val4 = ctk.IntVar(self.Tp4, value = 0)

            self.Bt8 = ctk.CTkButton(self.Tp4, text = 'Confirm', font = self.Font, corner_radius = 5, command = lambda : self.St.start(), state = 'disabled')
            self.Bt8.pack(padx = (5,5), pady = (0, 5))

        else:
            pass


    def add_file(self):

        self.Bt8.configure(state = 'normal')

        self.Tp4.bind('<Return>', lambda e = None : self.add_file())

        Dir = self.Req_txt.encode().hex()

        self.Tp4.attributes('-topmost', False)

        if self.File.get() != '':

            File = ctk.filedialog

            R_txt = File.askopenfilename(title = 'Select File', filetypes = [("PDF files", "*.pdf"),("Word documents", "*.doc *.docx"),("Image files", "*.jpg *.jpeg *.png *.png *.webp"), ("All Supported Files", "*.pdf *.doc *.docx *.jpg *.jpeg *.png *.webp")])

            if R_txt is None:
                Error(self.Tp4, None).FIleError()

            else:

                self.Lb15.configure(text = f'File :{ph.Path(R_txt).name}')
                #self.Bt8.configure(state = 'disabled')

                Key = Frt.generate_key()
                
                if self.Val3.get() == 1:
                    Dir = './' + Dir

                else:
                    pass

            def Reader():


                with (ph.Path(R_txt).open('rb')) as Rn:
                    text = Rn.read()

                self.Tp4.attributes('-topmost', True)

                L_txt = Frt(Key).encrypt(text)

                return L_txt


            def Add():
                 
                with ct.ThreadPoolExecutor(max_workers = 1) as thr:
                    Data_R = thr.submit(Reader)
                    Data = Data_R.result()

                self.Bt8.configure(state = 'normal')
                
                self.F_Name = hashes.Hash(hashes.BLAKE2b(64))
                self.F_Name.update(self.File.get().encode())
                
                with open(ph.Path('File.json')) as Fn:
                    Dats = json.load(Fn)
                    if self.User not in Dats.keys():
                        Dats.setdefault(self.User, {self.F_Name.finalize().hex() : Key.hex()})#[self.User, self.F_Name.finalize().hex(), Key.hex()])

                    else:
                        Dats[self.User].setdefault(self.F_Name.finalize().hex(), Key.hex())

                with open(ph.Path('File.json'), 'w') as Frn:
                    json.dump(Dats, Frn)
                

                Main.Mod(self.User, None, None).add_file(Dir ,Data ,self.File.get().encode().hex())
                
                Msg = MB(self.Tp4, title = 'Dir Set', message = f'Dir {Dir} has scuessfully created', font = self.Font, corner_radius = 3, fade_in_duration = 3, icon = 'check', option_1 = 'Done')

                if Msg.get() is not None:
                    self.Tp4.destroy()
                    

            self.St = th.Thread(target = Add, daemon = True)
            #self.Tp4.bind('',func = lambda e : St.start())

        else:
            Error(self.Tp4, 'Name').EntryError('Orange')


    def set_file(self, name, file):
        pass


class PDFReader:
    def __init__(self, user,  file, Tp, dir):

        self.File = file

        self.Tfont = ctk.CTkFont(family = 'Operation Napalm', size = 17)

        self.Tp5 = ctk.CTkToplevel(Tp)
        self.Tp5.title('FileVeiwer.xcr')
        self.Tp5.geometry('700x500')
        self.Tp5.attributes('-topmost', True)
        self.Tp5.grab_set()

        self.C_Page = 0

        self.Frm9 = ctk.CTkFrame(self.Tp5, corner_radius = 5, height = 120)
        self.Frm9.pack(padx = (5, 5), pady = (2, 5), expand = True, fill = 'x')

        self.Frm13 = ctk.CTkScrollableFrame(self.Tp5, corner_radius = 5, )
        self.Frm13.pack(padx = (5, 5), pady = (0, 5), expand = True, fill = 'both')

        Val = Main.Mod(user, None, None).acess_files(file, dir)

        f = hashes.Hash(hashes.BLAKE2b(64))
        f.update(bytes.fromhex(self.File))
        fle = f.finalize().hex()


        with open(ph.Path('File.json')) as Fn:

            Jats = json.load(Fn)
            Key = Jats.get(user).get(fle)

        try:
           Dat =  Frt(bytes.fromhex(Key)).decrypt(Val.decode()[2 : -1])

        except:
            return 

        self.Dat = pdfm.open(stream = Dat, filetype= 'pdf').
        print(self.Dat)

        self.Tp5.after(500, lambda : self.File_Acess)

    def File_Acess(self):

        for l in range(len(self.Dat)):
            Page = self.Dat.load_page(l)

            matx = pdfm.Matrix(1.2, 1.4)

            Pix = Page.get_pixmap(matrix = matx)

            Img = Image.open(io.BytesIO(Pix.tobytes()))

            C_Img = ctk.CTkImage(Img, Img, size = (Img.width, Img.height))

            Lbl14 = ctk.CTkLabel(self.Tp5, text = '', image = C_Img)
            Lbl14.pack(padx = (3, 3), pady = (2, 2), side = 'top')
            Lbl14.image = C_Img
            #Under Development
#Log()




