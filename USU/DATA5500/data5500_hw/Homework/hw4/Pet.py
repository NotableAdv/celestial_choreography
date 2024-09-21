# Hard Question

# Create a class called Pet with attributes name, age, and species. 
class Pet():
    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    # Implement a method within the class to calculate the age of the pet in equivalent human years.
    def age_in_human_years(self):
        species_conversion = {
            "dog": 7,               # 1 dog year = 7 human years
            "cat": 4,               # 1 cat year = 4 human years (average)
            "bird": 7,              # 1 bird year = 7 human years (average)
            "bunny": 6,             # 1 bunny year = 6 human years
            "bearded dragon": 7     # 1 bearded dragon year = 7 human years (average)
        }

        if self.species in species_conversion:
            human_age = self.age * species_conversion[self.species]
            return self.name + " is " + str(human_age) + " in human years."
        else:
            return self.name + "'s age cannot be converted to human years"

    # Implement a method within the class that takes the species of the pet as input and returns the average lifespan for that species.
    def average_lifespan(self):
        lifespans = {
            "dog": 11,             # dogs live 11 years (average)
            "cat": 13,             # cats live 13 years (average)
            "bird": 4,             # birds live 4 years (average)
            "bunny": 5,            # bunnies live 5 years (average)
            "bearded dragon": 12   # bearded dragons live 12 years (average)
        }

        if self.species in lifespans:
            return self.name + "'s lifespan will be about " + str(lifespans[self.species]) + " years as a " + self.species + "."
        else:
            return self.name + "'s lifespan cannot be found as a " + self.species + "."

# Instantiate three objects of the Pet class with different names, ages, and species.

# my kitten
pet1 = Pet("Echo", 0.25, "cat")

# my sister's dog
pet2 = Pet("Tucker", 1, "dog")

# my boyfriend's lizard
pet3 = Pet("Icarus", 3, "bearded dragon")

# test
pet4 = Pet("Boo", 2, "ghost")

# Calculate and print the age of each pet in human years.
print(pet1.age_in_human_years())
print(pet2.age_in_human_years())
print(pet3.age_in_human_years())
print(pet4.age_in_human_years())

# Use the average lifespan function to retrieve and print the average lifespan for each pet's species.
print(pet1.average_lifespan())
print(pet2.average_lifespan())
print(pet3.average_lifespan())   
print(pet4.average_lifespan())


# ChatGPT prompt to help me with the formulas

# give me 3 ideas for how would I change the pass to give the age in human years for the species listed where species can have different conversion factors? 
#"class Pet():
#    def __init__(self, name, age, species):
#        self.name = name
#        self.age = age
#        self.species = species
#
#    # Implement a method within the class to calculate the age of the pet in equivalent human years.
#    def age_in_human_years(self):
#        pass"

# The ideas I got:

# 1) Dictonary of Conversion Factors --> the option I chose
# 2) Species-Specific Method (do an if/elif,else for the different species under the def)
# 3) Class Method with Subcalling (creating ex: a class Cat(Pet) parent and child relationship)
