from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from kivymd.theming import ThemableBehavior
from kivy.core.window import Window
from registration import Registration
from login import Login
from homepage import HomeWindow
from settings import SettingsWindow, ApprovalsWindow
from grouppage import GroupWindow, NewGroupWindow, JoinGroupWindow
from activityhomepage import ActivityWindow,NewActivityWindow,ActivityDetailWindow,AddResourcesWindow
from payment import PaymentWindow, MyTransactionWindow, ResourcesWindow, ResourcesHistoryWindow, DonationsHistoryWindow
import globalvariables
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.picker import MDThemePicker

# Window.size = (300,500)

class MainApp(MDApp):
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Login(name='login_window'))
        manager.add_widget(Registration(name='register_window'))
        manager.add_widget(HomeWindow(name='home_window'))
        manager.add_widget(SettingsWindow(name='settings'))
        manager.add_widget(GroupWindow(name='group_window'))
        manager.add_widget(NewGroupWindow(name='new_group_window'))
        manager.add_widget(ActivityWindow(name='activity_window'))
        manager.add_widget(NewActivityWindow(name='new_activity_window'))
        manager.add_widget(JoinGroupWindow(name='join_group_window'))
        manager.add_widget(ActivityDetailWindow(name='activity_detail_window'))
        manager.add_widget(PaymentWindow(name='payment_window'))
        manager.add_widget(MyTransactionWindow(name='my_transaction_window'))
        manager.add_widget(ApprovalsWindow(name='approvals_window'))
        manager.add_widget(AddResourcesWindow(name='new_resource_window'))
        manager.add_widget(ResourcesWindow(name='resources_window'))
        manager.add_widget(ResourcesHistoryWindow(name='resources_history_window'))
        manager.add_widget(DonationsHistoryWindow(name='donations_history_window'))
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = "Light"
        self.title="Aaksathe"
        return manager

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()
        print(self.theme_cls.primary_palette)
        print(self.theme_cls.theme_style)

# Below all functions are used to handle file manager
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            #preview=True,
        )
    def file_manager_open(self):
        self.file_manager.show('/')  # output manager to the screen
        self.manager_open = True
    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.
        :type path: str;
        :param path: path to the selected directory or file;
        '''
        globalvariables.var_img_path = path
        self.exit_manager()

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.manager_open = False
        self.file_manager.close()
    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

MainApp().run()