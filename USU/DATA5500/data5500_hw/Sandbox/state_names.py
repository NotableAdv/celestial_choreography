# Dictionary mapping state abbreviations to full state names

fil_path = r"C:\Users\arika\USU\DATA5500\data5500_hw\Homework\hw5\states_territories.txt"

states = [line.strip() for line in open(fil_path).readlines()]


state_names = {
    'al': 'Alabama', 'ak': 'Alaska', 'as': 'American Samoa', 'az': 'Arizona', 'ar': 'Arkansas', 
    'ca': 'California', 'co': 'Colorado', 'ct': 'Connecticut', 'dc': 'Washington DC', 'de': 'Delaware', 
    'fl': 'Florida', 'ga': 'Georgia', 'gu': 'Guam', 'hi': 'Hawaii', 'id': 'Idaho', 
    'il': 'Illinois', 'in': 'Indiana', 'ia': 'Iowa', 'ks': 'Kansas', 
    'ky': 'Kentucky', 'la': 'Louisiana', 'me': 'Maine', 'md': 'Maryland', 
    'ma': 'Massachusetts', 'mi': 'Michigan', 'mn': 'Minnesota', 'ms': 'Mississippi', 
    'mo': 'Missouri', 'mp': 'Northern Mariana Islands', 'mt': 'Montana', 'ne': 'Nebraska', 'nv': 'Nevada', 
    'nh': 'New Hampshire', 'nj': 'New Jersey', 'nm': 'New Mexico', 'ny': 'New York', 
    'nc': 'North Carolina', 'nd': 'North Dakota', 'oh': 'Ohio', 'ok': 'Oklahoma', 
    'or': 'Oregon', 'pa': 'Pennsylvania', 'pr': 'Puerto Rico', 'ri': 'Rhode Island', 'sc': 'South Carolina', 
    'sd': 'South Dakota', 'tn': 'Tennessee', 'tx': 'Texas', 'ut': 'Utah', 
    'vt': 'Vermont', 'va': 'Virginia', 'vi': 'Virgin Islands', 'wa': 'Washington', 'wv': 'West Virginia', 
    'wi': 'Wisconsin', 'wy': 'Wyoming'
}

def print_state_name(state):
    full_name = state_names.get(state, 'Unknown abbreviation')
    print(state, full_name)

for state in states:
    print_state_name(state)