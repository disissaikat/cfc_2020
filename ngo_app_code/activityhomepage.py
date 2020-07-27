from kivy.uix.screenmanager import Screen,ScreenManager
from navdrawer import ContentNavigationDrawer
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.list import MDList, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.snackbar import Snackbar
import globalvariables
import connection
import ibm_db
from disasters import get_disasters

class ActivityWindow(Screen):
    def load_activity_page(self, orgname):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        self.ids['actscroll'].clear_widgets()
        self.ids['orgname'].title = orgname
        query = f'''SELECT ACTIVITY_ID, ORG_ID, NAME, LOCATION, DISASTER, TARGET_AMT FROM ACTIVITY WHERE 
        ORG_ID = {globalvariables.var_org_id} AND STATUS='Y' '''
        # run direct SQL
        print(globalvariables.var_org_id)
        stmt = ibm_db.exec_immediate(connection.conn, query)
        actlist = ibm_db.fetch_both(stmt)
        item = TwoLineIconListItem()
        while (actlist):
            icon = IconLeftWidget(icon="bank")         
            item = TwoLineIconListItem(text=str(actlist[2]), secondary_text=str(actlist[3])  )
            item.add_widget(icon)
            item.bind(on_release=self.row_press)
            self.ids['actscroll'].add_widget(item)
            actlist = ibm_db.fetch_both(stmt)   #for incrementing rows inside while loop
    
    def row_press(self, instance_row):
        globalvariables.var_act_name = instance_row.text
        self.manager.current = 'activity_detail_window'
        self.manager.get_screen('activity_detail_window').load_page()

class NewActivityWindow(Screen):
    def load_nav_drawer(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        #Load menu items
        disaster_list = get_disasters()
        self.menu = MDDropdownMenu(caller=self.ids['drop_item'],
        position="center",width_mult=5, callback=self.set_item)
        for i in disaster_list:
            self.menu.items.append({"text": str(i)})

    def cancel_act_creation(self):
        self.manager.current = 'activity_window'
        self.manager.transition.direction = 'right'

    def set_item(self, instance):
        self.ids['drop_item'].set_item(instance.text)
        self.menu.dismiss()
        self.get_total_amount_collected(instance.text)

    def get_total_amount_collected(self, disaster):
        query = f'''SELECT SUM(TARGET_AMT) FROM ACTIVITY 
        WHERE DISASTER='{disaster}'  '''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        userrow = ibm_db.fetch_tuple(stmt)
        if userrow != False :
            self.ids['planned_amount'].text = str(userrow[0])

    def create_activity(self, actname, loc, drop_item, target):
        actname = actname.text
        loc = loc.text
        disaster = drop_item.current_item
        target = target.text
        valid_str = ""
        if actname == "":
            valid_str = "Name is blank"
        elif loc == "":
            valid_str = "Location is blank"
        elif target == "":
            valid_str = "Target Amount is blank"  
        if valid_str != "":
            ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
            self.dialog = MDDialog(title='Alert !', text=valid_str, size_hint=(0.7,1), 
                                buttons=[ok_button])
            self.dialog.open()
        else:
            status = "Y"
            query1 = f'''INSERT INTO ACTIVITY(ORG_ID, NAME, LOCATION, DISASTER, TARGET_AMT, STATUS) 
            VALUES ({globalvariables.var_org_id},UPPER('{actname}'),'{loc}','{disaster}',{target}, '{status}')'''
            # run direct SQL
            stmt = ibm_db.exec_immediate(connection.conn, query1)
            if ibm_db.num_rows(stmt) > 0 :
                self.ids['actname'].text = "" #Setting the values to NULL after sucessfull registration
                self.ids['loc'].text = ""
                self.ids['drop_item'].text = ""
                self.ids['target'].text = ""
                self.ids['planned_amount'].text = ""
                ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
                self.dialog = MDDialog(title='Activity Created', 
                                text="Lets start helping!", size_hint=(0.7,1), buttons=[ok_button])
                self.dialog.open()
                self.manager.transition.direction = 'left'
                self.manager.current = 'activity_window'
                self.manager.get_screen('activity_window').load_activity_page(globalvariables.var_org_name)
                

    def dialog_close(self, obj):
            self.dialog.dismiss()


class ActivityDetailWindow(Screen):
    def load_page(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        actual_amount = 0
        spent_amount = 0
        print(type(actual_amount))
        print(globalvariables.var_org_id)
        print(globalvariables.var_act_name)
        query = f'''SELECT ACTIVITY_ID,NAME,LOCATION,DISASTER,TARGET_AMT FROM ACTIVITY 
        WHERE NAME='{globalvariables.var_act_name}' 
        AND ORG_ID = {globalvariables.var_org_id} AND STATUS='Y' '''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        userrow = ibm_db.fetch_tuple(stmt)
        act_id = ""
        act_name = ""
        act_loc = ""
        act_dis = ""
        act_target = ""
        if userrow != False :
            act_id = userrow[0]
            act_name = userrow[1]
            act_loc = userrow[2]
            act_dis = userrow[3]
            act_target = userrow[4]
        globalvariables.var_act_id = act_id
        globalvariables.var_act_name = act_name
        self.ids['actname'].text = act_name
        self.ids['location'].text = act_loc
        self.ids['actdis'].text = act_dis
        self.ids['acttarget'].text = str(act_target)
        query = f'''SELECT SUM(AMOUNT) FROM TRANSACTION WHERE ACTIVITY_ID= {globalvariables.var_act_id}'''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        userrow = ibm_db.fetch_tuple(stmt)
        if userrow != None :
            if userrow[0] != None :
                self.ids['actactual'].text = str(userrow[0])
                actual_amount = userrow[0]
            else :
                self.ids['actactual'].text = "0"
        query = f'''SELECT SUM(AMOUNT) FROM RESOURCES WHERE ACTIVITY_ID= {globalvariables.var_act_id}'''
        # run direct SQL
        stmt = ibm_db.exec_immediate(connection.conn, query)
        userrow = ibm_db.fetch_tuple(stmt)
        if userrow != None :
            if userrow[0] != None :
                self.ids['amountspent'].text = str(userrow[0])
                spent_amount = userrow[0]
            else :
                self.ids['amountspent'].text = "0"
        globalvariables.var_bal_amt = actual_amount - spent_amount
    
    def callback(self, instance):
        print(instance.icon)
        self.ids['actionbutton'].close_stack()
        if instance.icon == 'currency-inr':
            self.manager.transition.direction = 'left'
            self.manager.current = 'payment_window'
        else:
            self.manager.transition.direction = 'left'
            self.manager.current = 'new_resource_window'
            self.manager.get_screen('new_resource_window').load_page()



class AddResourcesWindow(Screen):
    def load_page(self):
        ContentNavigationDrawer.populateNavDrawerValues(self)
        self.rsrcmenu = MDDropdownMenu(caller=self.ids['name'], width_mult=5, 
        callback=self.set_item, position="center")
        items=["Medicine", "Biscuit", "Salt", "Tarpaulin", "Rice", "Daal", "Baby Food", "Sugar"]
        for i in items:
            self.rsrcmenu.items.append({"text": str(i)})

    def create_resource(self, name, desc, units, amount):
        rname = name.current_item
        rdesc = desc.text
        runits = units.text
        ramount = amount.text
        valid_str=""
        if rname == "":
            valid_str = "Select an Item"
        elif runits == "":
            valid_str = "Units is blank"
        elif ramount == "":
            valid_str = "Cost is blank"  
        elif int(ramount) > globalvariables.var_bal_amt :
            valid_str = "Insufficient funds"
        if valid_str != "":
            ok_button = MDFlatButton(text='OK', on_release=self.dialog_close)
            self.dialog = MDDialog(title='Alert !', text=valid_str, size_hint=(0.7,1), 
                                buttons=[ok_button])
            self.dialog.open()
        else:
            query1 = f'''INSERT INTO RESOURCES(CONTACT_ID, ACTIVITY_ID, NAME, DESC, UNITS, AMOUNT, DATE) 
            VALUES ({globalvariables.var_userid}, {globalvariables.var_act_id}, '{rname}', '{rdesc}', {runits},
            {ramount}, SYSDATE)'''
            # run direct SQL
            stmt = ibm_db.exec_immediate(connection.conn, query1)
            globalvariables.var_bal_amt = globalvariables.var_bal_amt - int(ramount)
            if ibm_db.num_rows(stmt) > 0 :
                #self.ids['name'].text=""
                self.ids['desc'].text=""
                self.ids['units'].text=""
                self.ids['amount'].text=""
                self.snackbar = Snackbar(text="Item Added!")
                self.snackbar.show()

    def dialog_close(self, obj):
            self.dialog.dismiss()

    def set_item(self, instance):
        self.ids['name'].set_item(instance.text)
        self.rsrcmenu.dismiss()

    def cancel_resource_creation(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'activity_detail_window'
        self.manager.get_screen('activity_detail_window').load_page()