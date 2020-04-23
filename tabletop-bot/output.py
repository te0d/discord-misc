# Lazy logger like thing for defining how the bot should handle responses
class Output:
    def __init__(self, private, message):
        self.private = private
        self.message = message
