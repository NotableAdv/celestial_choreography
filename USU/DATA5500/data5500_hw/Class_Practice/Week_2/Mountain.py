class Mountain:
    def __init__(self, name, ht, miles, elevation):
        self.name = name
        self.ht = ht 
        self.miles = miles
        self.elevation = elevation
    
    def __str__(self):
        return "Mount " + self.name + ", elevation: " + str(self.elevation) + " ft."
    
    def get_name(self):
        return self.name
    
    def get_ht(self):
        return self.ht
    
    def get_miles(self):
        return self.miles
    
    def get_elevation(self):
        return self.elevation
    
    def set_name(self):
        return self.name
    
    def set_ht(self):
        return self.ht
    
    def set_miles(self):
        return self.miles
    
    def set_elevation(self):
        return self.elevation
  
mt_rainier = Mountain("Rainer", 5000, 4, 14000)
    
print(mt_rainier)

half_dome = Mountain("Half Dome", 10000, 9, 13000)

print(half_dome)