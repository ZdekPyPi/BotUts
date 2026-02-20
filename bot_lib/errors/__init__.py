class BusinessException(Exception):
    def __init__(self,msg):
        self.msg = msg

class EventException(Exception):
    def __init__(self,msg):
        self.msg = msg