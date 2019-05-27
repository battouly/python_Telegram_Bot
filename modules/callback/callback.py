from modules.Consts.main import Const

class CallBack:
    def __init__():
        pass
    
    def look_up_method(self, command):
        return getattr(self, 'callback_' + command, self.state_default)

    def state_pr_template(self, **kwargs):