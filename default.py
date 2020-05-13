from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command

table = []
def function_name(task):
    """ a function for running something"""
    cmd = task.run(netmiko_send_command, command_string="show ip int br", use_textfsm=True)
    task.host["show"] = cmd.result
    shw_cmd = task.host["show"]
    
    print(shw_cmd)

def main():
    nr = InitNornir(config_file="config.yml")
    #will save the script result to var "cmd_result"
    cmd_result = nr.run(task=function_name)
    

if __name__ == "__main__":
    main()