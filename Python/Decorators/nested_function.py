def is_called(): 
    def is_returned():
         print("returned")
    return is_returned

new = is_called()
new()
