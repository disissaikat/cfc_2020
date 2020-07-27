from kivy.uix.screenmanager import Screen,ScreenManager
from navdrawer import ContentNavigationDrawer
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
import globalvariables
import connection
import ibm_db,os
from kivymd.uix.list import MDList, TwoLineAvatarListItem, ImageLeftWidget
from image_upload import upload_org_logo, download_org_image

class GroupWindow(Screen):
    def load_group_page(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        self.ids['allorgscroll'].clear_widgets()      #To clear list of orgs
        query = f'''SELECT ORG_ID,NAME,REGISTRATION FROM ORG WHERE 
        ORG_ID IN (
        SELECT ORG_ID FROM ORG
        MINUS 
        SELECT ORG_ID FROM CONTACT_ORG WHERE CONTACT_ID = {globalvariables.var_userid}
        AND STATUS='Y')'''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        orglist = ibm_db.fetch_both(stmt)
        item = TwoLineAvatarListItem()
        while (orglist):
            file_found = download_org_image(str(orglist[0]))
            if file_found == True :
                image = ImageLeftWidget(source="resources/org/"+str(orglist[0])+".png")
            else:
                image = ImageLeftWidget(source="resources/org/default.jpg")               
            item = TwoLineAvatarListItem(text=str(orglist[1]), secondary_text=str(orglist[2])  )
            item.add_widget(image)
            item.bind(on_release=self.row_press)
            self.ids['allorgscroll'].add_widget(item)
            orglist = ibm_db.fetch_both(stmt)   #for incrementing rows inside while loop
    
    def row_press(self, instance_row):
        self.manager.current = 'join_group_window'
        self.manager.get_screen('join_group_window').load_page(instance_row.secondary_text)

    
class NewGroupWindow(Screen):
    def cancel_org_creation(self):
        self.ids['groupname'].text = "" #Setting the values to NULL after cancel registration
        self.ids['regnum'].text = ""
        self.ids['desc'].text = ""
        self.manager.transition.direction = 'right'
        self.manager.current = 'group_window'
        
    def load_nav_drawer(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)

    def create_org(self, groupname, regnum, desc):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        groupname = groupname.text
        regnum = regnum.text
        desc = desc.text
        valid_str = ""
        if groupname == "":
            valid_str = "Name is blank"
        elif regnum == "":
            valid_str = "Registration is blank"
        elif desc == "":
            valid_str = "Description is blank"    
        if valid_str != "":
            ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
            self.dialog = MDDialog(title='Alert !', text=valid_str, size_hint=(0.7,1), 
                                buttons=[ok_button])
            self.dialog.open()
        else:
            status = "Y"
            query1 = f'''INSERT INTO ORG(NAME, REGISTRATION, DESC, OWNER_ID, STATUS) 
            VALUES (UPPER('{groupname}'),UPPER('{regnum}'),'{desc}',{globalvariables.var_userid}, '{status}')'''
            # run direct SQL
            stmt = ibm_db.exec_immediate(connection.conn, query1)
            if ibm_db.num_rows(stmt) > 0 :
                query2 = f'''SELECT ORG_ID FROM ORG WHERE REGISTRATION=UPPER('{regnum}') '''
                stmt = ibm_db.exec_immediate(connection.conn, query2)
                orglist = ibm_db.fetch_both(stmt)
                orgid=""
                while (orglist):
                    orgid = orglist[0]
                    query3 = f'''INSERT INTO CONTACT_ORG(ORG_ID, CONTACT_ID, MEMBER_FLAG, STATUS) 
                    VALUES ({orgid},{globalvariables.var_userid},'Y', '{status}')'''
                    stmt1 = ibm_db.exec_immediate(connection.conn, query3)
                    orglist = ibm_db.fetch_both(stmt)
                self.ids['groupname'].text = "" #Setting the values to NULL after sucessfull registration
                self.ids['regnum'].text = ""
                self.ids['desc'].text = ""
                #To upload Org Logo
                if globalvariables.var_img_path != "":
                    logo_path = globalvariables.var_img_path
                    tgt_logo_path = "org_"+str(orgid)+".png"
                    upload_org_logo(logo_path, tgt_logo_path)
                    globalvariables.var_img_path = ""
                ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
                self.dialog = MDDialog(title='Successfully Registered', 
                                text="Lets start helping!", size_hint=(0.7,1), buttons=[ok_button])
                self.dialog.open()
                self.manager.transition.direction = 'left'
                self.manager.current = 'home_window'
                self.manager.get_screen('home_window').load_home_page()
                
    def dialog_close(self, obj):
            self.dialog.dismiss()

class JoinGroupWindow(Screen):
    def load_page(self, greg):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        query = "SELECT ORG_ID,NAME,REGISTRATION,DESC FROM ORG WHERE REGISTRATION='"+greg+"'"
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        userrow = ibm_db.fetch_tuple(stmt)
        org_id = ""
        org_name = ""
        org_reg = ""
        org_desc = ""
        if userrow != False :
            org_id = userrow[0]
            org_name = userrow[1]
            org_reg = userrow[2]
            org_desc = userrow[3]
            file_found = download_org_image(str(userrow[0]))
            if file_found == True :
                self.ids['grouplogo'].source="resources/org/"+str(userrow[0])+".png"
            else:
                self.ids['grouplogo'].source="resources/org/default.jpg"
        globalvariables.var_org_id = org_id
        globalvariables.var_org_name = org_name
        self.ids['gname'].text = org_name
        self.ids['greg'].text = org_reg
        self.ids['gdesc'].text = org_desc
        #USED TO POPULATE DROP DOWN OF ACTIVITY FOR PAYMENTS FOR NON JOINERS
        query = "SELECT ACTIVITY_ID,NAME FROM ACTIVITY WHERE ORG_ID="+str(globalvariables.var_org_id)
        stmt = ibm_db.exec_immediate(connection.conn, query)
        act = ibm_db.fetch_both(stmt)
        actlist=[]
        while (act):
            actlist.append(str(act[1]))
            act = ibm_db.fetch_both(stmt)
        self.menu = MDDropdownMenu(caller=self.ids['activity_item'],
        position="center",width_mult=5, callback=self.set_item)
        for i in actlist:
            self.menu.items.append({"text": str(i)})

    def set_item(self, instance):
        self.ids['activity_item'].set_item(instance.text)
        self.menu.dismiss()
        self.get_total_amount_collected(instance.text)

    def get_total_amount_collected(self, disaster):
        query = f'''SELECT TARGET_AMT FROM ACTIVITY 
        WHERE NAME='{disaster}' AND ORG_ID={globalvariables.var_org_id} '''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        userrow = ibm_db.fetch_tuple(stmt)
        if userrow != False :
            self.ids['planned_amount'].text = str(userrow[0])
        query = f'''SELECT SUM(TXN.AMOUNT) AS AMOUNT
        FROM TRANSACTION TXN, ACTIVITY ACT
        WHERE TXN.ACTIVITY_ID = ACT.ACTIVITY_ID
        AND ACT.NAME = '{disaster}'
        AND ACT.ORG_ID = {globalvariables.var_org_id}  '''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        userrow = ibm_db.fetch_tuple(stmt)
        if userrow != False :
            self.ids['reached_amount'].text = str(userrow[0])

    def donate_to_activity(self):
        query = f'''SELECT ACTIVITY_ID,NAME FROM ACTIVITY 
        WHERE NAME='{self.ids['activity_item'].current_item}' AND ORG_ID={globalvariables.var_org_id}'''
        stmt = ibm_db.exec_immediate(connection.conn, query)
        print(query)
        act = ibm_db.fetch_tuple(stmt)
        if act != False :
            globalvariables.var_act_id = act[0]
            globalvariables.var_act_name = act[1]
        self.manager.current = 'payment_window'

    def join_group(self):
        query = f'''INSERT INTO CONTACT_ORG(ORG_ID, CONTACT_ID, STATUS, MEMBER_FLAG) 
        VALUES ({globalvariables.var_org_id},{globalvariables.var_userid}, 'N', 'P')'''
        stmt = ibm_db.exec_immediate(connection.conn, query)
        if ibm_db.num_rows(stmt) > 0 :
            ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
            self.dialog = MDDialog(title='Group Request Submitted', 
                            text="Your group would be available in My Groups when a moderator approves", size_hint=(0.7,1), buttons=[ok_button])
            self.dialog.open()
            self.manager.transition.direction = 'left'
            self.manager.current = 'home_window'
            self.manager.get_screen('home_window').load_home_page()

    def cancel_join_group(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'group_window'

    def dialog_close(self, obj):
        self.dialog.dismiss()