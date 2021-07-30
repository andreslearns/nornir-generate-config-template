from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_config, netmiko_send_command
from nornir.plugins.functions.text import print_title, print_result
from nornir.plugins.tasks import networking, text
from nornir.core.exceptions import NornirExecutionError
from colorama import Fore
from nornir.core.filter import F

red = Fore.RED
green = Fore.GREEN
reset = Fore.RESET

def send_config(task):
    """ a function for running something"""

    r = task.run(task=text.template_file,
                     name="AAA Tacacs Base configuration",
                     template="base.j2",
                     tacacs_server = task.host.data['tacacs_server'],
                     tacacs_key = task.host.data['tacacs_key'],
                     radius_server = task.host.data['radius_key'],
                     radius_key = task.host.data['radius_key'],
                     mgmt_vlan = task.host.data['mgmt_vlan'],
                     source_int = task.host.data['source_int'],
                     path=f"templates/{task.host.data['hardware_type']}",)

    task.host["rendered_config"] = r.result


    cmd = task.run(netmiko_send_config,
                name="Deploying config in the host",
                config_commands=task.host["rendered_config"])
    # task.host["show"] = cmd.result
    # shw_cmd = task.host["show"]
    print_result(cmd)

def main():
    nr = InitNornir(config_file="config.yml")

    # result = nr.run(task=send_config)

    try:
        prompt = input("select a group of device: ")

        if prompt == "all":
            result = nr.run(task=send_config)
            prompt_all = result.failed_hosts.keys()  
            hosts = nr.inventory.hosts
            print('x' * 80)
            print("\t\t\t\tTASK SUMMARY")
            print('x' * 80)
            for x in hosts:
                if x in prompt_all:
                    print(red + (f"\t\t\tError\t\t-->\t{x}"))
                else:
                    print(green + (f"\t\t\tSuccess\t\t-->\t{x}") + reset)

        elif prompt == prompt:
            groups = nr.filter(F(groups__contains=prompt,))
            groups_result = groups.run(task=send_config)
            failed_group = groups_result.failed_hosts.keys()
            hosts = groups.inventory.hosts.keys()
            print_result(groups)

            print('x' * 80)
            print("\t\t\t\tTASK SUMMARY")
            print('x' * 80)
            for x in hosts:
                if x in failed_group:
                    print(red + (f"\t\t\tError\t\t-->\t{x}"))
                else:
                    print(green + (f"\t\t\tSuccess\t\t-->\t{x}") + reset)

    except IndexError:
        print("not allowed")

if __name__ == "__main__":
    main()