from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen,ScreenManager
import connection
import ibm_db
import re
from mail_demo import send_registration_mail
from password_hashing import encrypt_pwd

class Registration(Screen):
    def insert_new_user(self, fname, lname, uname, pwd1, pwd2):
        fname = fname.text
        lname = lname.text
        email = uname.text
        pwd1 = pwd1.text
        pwd2 = pwd2.text
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        valid_str = ""
        if fname == "":
            valid_str = "First Name is blank"
        elif lname == "":
            valid_str = "Last Name is blank"
        elif email == "":
            valid_str = "Email is blank"
        elif pwd1 == "":
            valid_str = "Password is blank"
        elif pwd2 == "":
            valid_str = "Confirm Password is blank"
        elif pwd1 != pwd2:
            valid_str = "Passwords not matching"
        elif re.search(regex,email) is None:
            valid_str = "Email is not valid"
        
        if valid_str != "":
            ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
            self.dialog = MDDialog(title='Alert !', text=valid_str, size_hint=(0.7,1), 
                                buttons=[ok_button])
            self.dialog.open()
        else:
            encrypted_pwd = encrypt_pwd(pwd1)
            query = f'''INSERT INTO CONTACT(FIRST_NAME, LAST_NAME, EMAIL, PASSCODE) 
            VALUES (UPPER('{fname}'),UPPER('{lname}'),'{email}',{repr(encrypted_pwd)}) '''
            # run direct SQL
            stmt = ibm_db.exec_immediate(connection.conn, query)
            if ibm_db.num_rows(stmt) > 0 :
                send_registration_mail(email, fname, lname) #Call function to send mail
                self.ids['fname'].text = "" #Setting the values to NULL after sucessfull registration
                self.ids['lname'].text = ""
                self.ids['uname'].text = ""
                self.ids['pwd1'].text = ""
                self.ids['pwd2'].text = ""
                ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
                self.dialog = MDDialog(title='Successfully Registered', 
                                text="Please use login screen to login.", size_hint=(0.7,1), buttons=[ok_button])
                self.dialog.open()
                self.manager.transition.direction = 'right'
                self.manager.current = 'login_window'


    def dialog_close(self, obj):
            self.dialog.dismiss()
