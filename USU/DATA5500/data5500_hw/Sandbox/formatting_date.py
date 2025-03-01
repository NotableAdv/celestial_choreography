from datetime import datetime
date_string = "20240925"
date_object = datetime.strptime(date_string, "%Y%m%d")
formatted_date = date_object.strftime("%m/%d/%Y")
print(date_string)
print(formatted_date) 