from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen,ScreenManager
from homepage import HomeWindow
import connection
import ibm_db, random, string
import globalvariables
from password_hashing import decrypt_pwd, encrypt_pwd
from mail_demo import forgot_password_mail

class Login(Screen):
    def check_login(self, username, pwd):
        email = username.text
        passcode = pwd.text
        check_str = ""
        if email is "":
            check_str = "Please enter an Email"
        elif passcode is "":
            check_str = "Please enter password"
        if check_str != "":
            ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
            self.dialog = MDDialog(title='Alert', text=check_str, size_hint=(0.7,1), 
                                buttons=[ok_button])
            self.dialog.open()
        else:
            # passcode = bytes(passcode, 'utf-8')
            query = f"""SELECT CONTACT_ID,FIRST_NAME,LAST_NAME,EMAIL,PASSCODE FROM CONTACT 
            WHERE EMAIL='{email}' """
            # run direct SQL
            stmt = ibm_db.exec_immediate(connection.conn, query)
            userrow = ibm_db.fetch_tuple(stmt)
            if userrow != False :
                stored_pwd = userrow[4]
                stored_pwd = decrypt_pwd(stored_pwd)
                if passcode == stored_pwd:
                    globalvariables.var_userid = userrow[0]
                    globalvariables.var_fname = userrow[1]
                    globalvariables.var_lname = userrow[2]
                    globalvariables.var_email = userrow[3]
                    self.manager.current = 'home_window'
                    self.manager.transition.direction = 'left'
                    self.manager.get_screen('home_window').load_home_page()
                else:
                    ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
                    self.dialog = MDDialog(title='Login Unsucessfull!', 
                                text="Incorrect Password", size_hint=(0.7,1), buttons=[ok_button])
                    self.dialog.open()
            else:
                ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
                self.dialog = MDDialog(title='Login Unsucessfull!', 
                                text="Email not registered", size_hint=(0.7,1), buttons=[ok_button])
                self.dialog.open()


    def dialog_close(self, obj):
        self.dialog.dismiss()

    def forgot_password(self, username):
        email = username.text
        check_str = ""
        if email is "":
            check_str = "Please enter an Email"
        if check_str != "":
            ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
            self.dialog = MDDialog(title='Alert', text=check_str, size_hint=(0.7,1), 
                                buttons=[ok_button])
            self.dialog.open()
        else:
            query = f"""SELECT CONTACT_ID,FIRST_NAME,LAST_NAME FROM CONTACT 
            WHERE EMAIL='{email}' """
            # run direct SQL
            stmt = ibm_db.exec_immediate(connection.conn, query)
            userrow = ibm_db.fetch_tuple(stmt)
            if userrow != False :
                new_pwd = self.get_random_string()
                print(new_pwd)
                encrypted_pwd = encrypt_pwd(new_pwd)
                query = f'''UPDATE CONTACT SET PASSCODE={repr(encrypted_pwd)}
                WHERE EMAIL='{email}' '''
                # run direct SQL
                stmt = ibm_db.exec_immediate(connection.conn, query)
                if ibm_db.num_rows(stmt) > 0 :
                    print("Password changed")
                    forgot_password_mail(email, userrow[1], userrow[2], new_pwd) #Call function to send mail
                    self.ids['username'].text = "" #Setting the values to NULL after sucessfull registration
                    self.ids['pwd'].text = ""
                    ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
                    self.dialog = MDDialog(title='Password Changed', 
                                    text="Mail sent with new password. Please change you password after login", size_hint=(0.7,1), buttons=[ok_button])
                    self.dialog.open()
            else:
                ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
                self.dialog = MDDialog(title='Alert', text="Email is not registered", size_hint=(0.7,1), 
                                buttons=[ok_button])
                self.dialog.open()

    def get_random_string(self):
        # Random string with the combination of lower and upper case
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(8))
        return result_str


    def sign_out(self):
        self.ids['username'].text= ""
        self.ids['pwd'].text= ""
        globalvariables.var_userid= ""
        globalvariables.var_fname= ""
        globalvariables.var_lname= ""
        globalvariables.var_email= ""
        globalvariables.var_org_id= ""
        globalvariables.var_act_name= ""
        globalvariables.var_act_id= ""
        self.manager.get_screen('home_window').ids['nogroupwarning'].text = ""