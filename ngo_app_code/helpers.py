username_helper = """
MDTextField:
    hint_text: "Enter Phone Number"
    pos_hint: {'center_x':0.5, 'center_y':0.6}
    size_hint_x: None
    width: 200
    max_text_length: 10
    required: True
    icon_right: "cellphone"
    icon_right_color: app.theme_cls.primary_color
"""
password_helper = """
MDTextField:
    password: True
    hint_text: "Enter Password"
    pos_hint: {'center_x':0.5, 'center_y':0.5}
    helper_text: "Click Forgot Password if you do not remember it"
    helper_text_mode: "on_focus"
    size_hint_x: None
    width: 200
    required: True
    icon_right: "cellphone-key"
    icon_right_color: app.theme_cls.primary_color
"""