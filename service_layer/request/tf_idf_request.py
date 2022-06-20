#object
#check right -> param, wrong -> raise error
class TfIdfRequestHandler:
    def __init__(self, args):
        self.args = args
        try:
            if "field" not in self.args:
                raise KeyError("Lack of ""field"" key, can't retrieve tokens for textcloud")
        except:
            pass
            #call response object
        
