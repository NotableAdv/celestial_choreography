#defining a class of my Lego Collection for class practice 9/11

class Legos:
    def __init__(self, name, theme, size, location, price):
        self.name = name
        self.theme = theme
        self.size = size
        self.location = location
        self.__price = price
    
    def __str__(self, ):
        return "The Lego set " + self.name + " is a " + self.theme + " set. It is a " + self.size + " size set located on my " + self.location + "."
    
    def get_name(self):
        return self.name
    
    def get_theme(self):
        return self.theme
    
    def get_size(self):
        return self.size
    
    def get_location(self):
        return self.location
    
    def get_price(self):
        return self.__price
    
    def set_name(self):
        return self.name
    
    def set_theme(self):
        return self.theme
    
    def set_size(self):
        return self.size
    
    def set_location(self):
        return self.location
    
    def set_price(self):
        return self.__price

orchid = Legos("Orchid", "Botanical", "Medium", "TV stand", 50)

print(orchid)

