from telegram import InlineKeyboardButton, InlineKeyboardMarkup





def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

class Utils:
    @staticmethod
    def create_inlinekeyboard(buttons, cols, header=None, footer=None):
        button_list = []
        for button in buttons:
            ikb = InlineKeyboardButton(button.get('text'), callback_data=button.get('callback_data'))
            button_list.append(ikb)

        reply_markup = InlineKeyboardMarkup(
            build_menu(button_list, n_cols=cols, header_buttons=header, footer_buttons=footer))

        return reply_markup      


