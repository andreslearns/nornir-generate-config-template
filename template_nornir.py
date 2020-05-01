import csv
from jinja2 import Template
import os

try:
    path = "inventory/"
    os.makedirs(path)
except FileExistsError:
    pass

#store the source csv in variable
source_file_hosts = "template_source.csv"    
# store the jinja2 file in a variable
template_file_hosts = "nornir_hosts.j2" 

#create an empty string for the ouput container
host_configs =""   

#open the template_file and assign to variable f
with open (template_file_hosts) as f: 
    #reading jinja2 environment and assigning to var interface template
    interface_template = Template(f.read(), keep_trailing_newline=True) 
    
# opening the csv file and assigning to var f
with open(source_file_hosts) as f:
    reader = csv.DictReader(f) #reading the csv file
    for row in reader:  #loop in all rows of csv file and assigning to row variable
        host_data = interface_template.render(   #assigned all the rendered file into variables
            # assigning all the row values into variables                                       
            hostname = row['hostname'],
            ipaddress = row['ipaddress'],
            platform = row['platform'],
            groups = row['groups'],)
        host_configs += host_data #appending all the values from hosts_data to output_configs

with open(path + "hosts.yml", 'w') as f:
    f.write(host_configs)


    

