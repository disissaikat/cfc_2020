from kivy.uix.screenmanager import Screen,ScreenManager
from navdrawer import ContentNavigationDrawer
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
import globalvariables
import connection
import ibm_db
from mail_demo import payment_mail

class PaymentWindow(Screen):
    def load_payment_page(self):
        self.ids['actname'].text = "Donate to "+ globalvariables.var_act_name

    def make_payment(self,payamount):
        amount = payamount.text
        valid_str=""
        if amount == "":
            valid_str = "Amount is blank"
        elif int(amount) < 10:
            valid_str = "Minimum Amount to donate is 10"
        if valid_str != "":
            ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
            self.dialog = MDDialog(title='Alert !', text=valid_str, size_hint=(0.7,1), 
                                buttons=[ok_button])
            self.dialog.open()
        else:
            query = f'''INSERT INTO TRANSACTION(ACTIVITY_ID, CONTACT_ID, TXN_DATE, AMOUNT) 
            VALUES ({globalvariables.var_act_id}, {globalvariables.var_userid}, SYSDATE, {amount})'''
            # run direct SQL
            stmt = ibm_db.exec_immediate(connection.conn, query)
            if ibm_db.num_rows(stmt) > 0 :
                payment_mail(globalvariables.var_email, globalvariables.var_fname, amount, globalvariables.var_org_name, globalvariables.var_act_name)
                self.ids['payamount'].text = "" #Setting the values to NULL after sucessfull registration
                ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
                self.dialog = MDDialog(title='Payment Successfull!', 
                                text="Thank you for your donation!", size_hint=(0.7,1), buttons=[ok_button])
                self.dialog.open()
                self.manager.transition.direction = 'right'
                self.manager.current = 'my_transaction_window'
                self.manager.get_screen('my_transaction_window').load_txn_page()
                
    def dialog_close(self, obj):
            self.dialog.dismiss()

    def cancel_payment(self):
        self.ids['payamount'].text = ""
        self.manager.current = 'home_window'
        self.manager.transition.direction = 'right'
        self.manager.get_screen('home_window').load_home_page()

class MyTransactionWindow(Screen):
    def load_txn_page(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        query = f'''SELECT TXN_DATE, ORG.NAME as ORG_NAME, ACT.NAME as ACT_NAME, TXN.AMOUNT
        FROM TRANSACTION TXN, ACTIVITY ACT, ORG ORG
        WHERE TXN.CONTACT_ID={globalvariables.var_userid}
        AND TXN.ACTIVITY_ID = ACT.ACTIVITY_ID
        AND ACT.ORG_ID=ORG.ORG_ID ORDER BY TXN_DATE DESC'''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        txnlist = ibm_db.fetch_both(stmt)
        if txnlist is False :
            warn_label = MDLabel(pos_hint = {'center_x':0.5, 'center_y':0.5},font_size = '10sp',
            text = "You have not made any donations yet")
            self.ids['float_lay'].add_widget(warn_label)
        else:
            print(txnlist)
            tlist=[]
            while(txnlist):
                tlist.append([str(txnlist[0]),txnlist[1],txnlist[2],str(txnlist[3])])
                txnlist = ibm_db.fetch_both(stmt)
            data_tables = MDDataTable(
                size_hint=(0.8, 0.8),
                rows_num=100,
                background_color=[1,0,0,1],
                pos_hint = {'center_x':0.5, 'center_y':0.5},
                column_data=[
                    ("Date", dp(50)),
                    ("Group", dp(50)),
                    ("Activity", dp(50)),
                    ("Amount", dp(30)),
                ],
                row_data=[(f"{i[0]}",f"{i[1]}",f"{i[2]}",f"{i[3]}") for i in tlist]
                )
            self.ids['float_lay'].add_widget(data_tables)
            self.ids['float_lay'].add_widget(MDFillRoundFlatIconButton(text="BACK",
            pos_hint={'center_x':0.5, 'center_y':0.1}, icon="arrow-left-bold-circle",theme_text_color="Custom", 
            text_color= (0, 0, 1, 1), on_release=lambda x: self.to_home_page() ))

    def to_home_page(self):
        self.manager.current = 'home_window'
        self.manager.transition.direction = 'right'

class ResourcesWindow(Screen):
    def load_resources_page(self):
        self.ids['float_lay'].clear_widgets()
        ContentNavigationDrawer.populateNavDrawerValues(self)
        query = f'''SELECT NAME,SUM(UNITS) AS UNITS, SUM(AMOUNT) AS AMOUNT
        FROM RESOURCES WHERE ACTIVITY_ID = {globalvariables.var_act_id}
        GROUP BY NAME ORDER BY NAME   '''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        txnlist = ibm_db.fetch_both(stmt)
        if txnlist is False :
            warn_label = MDLabel(pos_hint = {'center_x':0.5, 'center_y':0.5},font_size = '10sp',
            text = "No Resources yet")
            self.ids['float_lay'].add_widget(warn_label)
        else:
            print(txnlist)
            tlist=[]
            while(txnlist):
                tlist.append([txnlist[0],str(txnlist[1]),str(txnlist[2])])
                txnlist = ibm_db.fetch_both(stmt)
            data_tables = MDDataTable(
                size_hint=(0.8, 0.8),
                rows_num=100,
                background_color=[1,0,0,1],
                pos_hint = {'center_x':0.5, 'center_y':0.5},
                column_data=[
                    ("Resource", dp(50)),
                    ("Units", dp(50)),
                    ("Amount", dp(50)),
                ],
                row_data=[(f"{i[0]}",f"{i[1]}",f"{i[2]}") for i in tlist]
                )
            self.ids['float_lay'].add_widget(data_tables)
            self.ids['float_lay'].add_widget(MDFillRoundFlatButton(text="BACK",
            pos_hint={'center_x':0.3, 'center_y':0.1}, theme_text_color="Custom", 
            text_color= (0, 0, 1, 1), on_release=lambda x: self.to_previous_page() ))
            self.ids['float_lay'].add_widget(MDFillRoundFlatButton(text="DETAILS",
            pos_hint={'center_x':0.7, 'center_y':0.1}, theme_text_color="Custom", 
            text_color= (0, 0, 1, 1), on_release=lambda x: self.to_details_page() ))

    def to_previous_page(self):
        self.manager.current = 'activity_detail_window'
        self.manager.transition.direction = 'right'

    def to_details_page(self):
        self.manager.current = 'resources_history_window'
        self.manager.transition.direction = 'left'
        self.manager.get_screen('resources_history_window').load_hist_page()

class ResourcesHistoryWindow(Screen):
    def load_hist_page(self):
        self.ids['float_lay'].clear_widgets()
        ContentNavigationDrawer.populateNavDrawerValues(self)
        query = f'''SELECT RES.DATE, CON.FIRST_NAME||' '||CON.LAST_NAME AS NAME, 
        RES.NAME AS ITEM, RES.DESC AS DESC, RES.UNITS, RES.AMOUNT
        FROM RESOURCES RES, CONTACT CON 
        WHERE RES.ACTIVITY_ID = {globalvariables.var_act_id}
        AND CON.CONTACT_ID = RES.CONTACT_ID  ORDER BY RES.DATE DESC '''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        txnlist = ibm_db.fetch_both(stmt)
        if txnlist is False :
            warn_label = MDLabel(pos_hint = {'center_x':0.5, 'center_y':0.5},font_size = '10sp',
            text = "No Resources yet")
            self.ids['float_lay'].add_widget(warn_label)
        else:
            print(txnlist)
            tlist=[]
            while(txnlist):
                tlist.append([txnlist[0],txnlist[1],txnlist[2], str(txnlist[3]), str(txnlist[4]), str(txnlist[5]) ])
                txnlist = ibm_db.fetch_both(stmt)
            data_tables = MDDataTable(
                size_hint=(0.8, 0.8),
                rows_num=100,
                background_color=[1,0,0,1],
                pos_hint = {'center_x':0.5, 'center_y':0.5},
                column_data=[
                    ("Date", dp(30)),
                    ("Name", dp(30)),
                    ("Item", dp(30)),
                    ("Description", dp(30)),
                    ("Units", dp(30)),
                    ("Amount", dp(30)),
                ],
                row_data=[(f"{i[0]}",f"{i[1]}",f"{i[2]}",f"{i[3]}",f"{i[4]}",f"{i[5]}") for i in tlist]
                )
            self.ids['float_lay'].add_widget(data_tables)
            self.ids['float_lay'].add_widget(MDFillRoundFlatButton(text="BACK",
            pos_hint={'center_x':0.5, 'center_y':0.1}, theme_text_color="Custom", 
            text_color= (0, 0, 1, 1), on_release=lambda x: self.to_previous_page() ))

    def to_previous_page(self):
        self.manager.current = 'resources_window'
        self.manager.transition.direction = 'right'


class DonationsHistoryWindow(Screen):
    def load_hist_page(self):
        self.ids['float_lay'].clear_widgets()
        ContentNavigationDrawer.populateNavDrawerValues(self)
        query = f'''SELECT TXN.TXN_DATE, CON.FIRST_NAME||' '||CON.LAST_NAME AS NAME, 
        CON.EMAIL, TXN.AMOUNT
        FROM TRANSACTION TXN, CONTACT CON 
        WHERE TXN.ACTIVITY_ID = {globalvariables.var_act_id}
        AND CON.CONTACT_ID = TXN.CONTACT_ID  ORDER BY TXN.TXN_DATE DESC '''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        txnlist = ibm_db.fetch_both(stmt)
        if txnlist is False :
            warn_label = MDLabel(pos_hint = {'center_x':0.5, 'center_y':0.5},font_size = '10sp',
            text = "No Donations yet")
            self.ids['float_lay'].add_widget(warn_label)
        else:
            tlist=[]
            while(txnlist):
                tlist.append([txnlist[0],txnlist[1],txnlist[2], str(txnlist[3]) ])
                txnlist = ibm_db.fetch_both(stmt)
            data_tables = MDDataTable(
                size_hint=(0.8, 0.8),
                rows_num=100,
                background_color=[1,0,0,1],
                pos_hint = {'center_x':0.5, 'center_y':0.5},
                column_data=[
                    ("Date", dp(30)),
                    ("Name", dp(30)),
                    ("Email", dp(30)),
                    ("Amount", dp(30)),
                ],
                row_data=[(f"{i[0]}",f"{i[1]}",f"{i[2]}",f"{i[3]}") for i in tlist]
                )
            self.ids['float_lay'].add_widget(data_tables)
            self.ids['float_lay'].add_widget(MDFillRoundFlatButton(text="BACK",
            pos_hint={'center_x':0.5, 'center_y':0.1}, theme_text_color="Custom", 
            text_color= (0, 0, 1, 1), on_release=lambda x: self.to_previous_page() ))

    def to_previous_page(self):
        self.manager.current = 'activity_detail_window'
        self.manager.transition.direction = 'right'
