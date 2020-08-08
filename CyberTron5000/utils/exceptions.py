class EmbedError(Exception):
    def __init__(self):
        self.message = "Error! You passed incorrect embed arguments!"
    
    def __str__(self):
        return self.message


class UserError(Exception):
    def __init__(self, message="This parameter must be a valid user id!"):
        self.message = message
    
    def __str__(self):
        return self.message
