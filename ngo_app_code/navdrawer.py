from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
import globalvariables, os
from image_upload import download_contact_image

class ContentNavigationDrawer(MDBoxLayout):
    nav_drawer = ObjectProperty()
    nav_bar_name = ObjectProperty()
    nav_bar_email = ObjectProperty()
    def populateNavDrawerValues(self):
        file_found = download_contact_image(str(globalvariables.var_userid)+'.png')
        if file_found == True:
            self.ids['nav_lay'].ids['avatar'].source = "resources/contact/"+str(globalvariables.var_userid)+".png"
        else:
            self.ids['nav_lay'].ids['avatar'].source = "resources/contact/dummy-profile-pic.png"
        self.ids['nav_lay'].ids['drawer_name'].text = globalvariables.var_fname+" "+globalvariables.var_lname
        self.ids['nav_lay'].ids['drawer_email'].text = globalvariables.var_email
