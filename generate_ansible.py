import os
import yaml
from helpers.nso import NSO


def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')


yaml.add_representer(type(None), represent_none)


def main():
    # pull NSO config from Ansible vars
    with open('group_vars/all.yaml', 'r') as fh:
        config = yaml.safe_load(fh)

    if not os.path.exists('host_vars'):
        os.makedirs('host_vars')

    ip = config['nso']['ip']
    username = config['nso']['username']
    password = config['nso']['password']
    nso = NSO(ip, username, password)
    #
    print("Syncing Configuration from Devices")
    nso.sync_from()

    devices = nso.get_device_list()

    # create inventory yaml
    inv_dict = {"all": {"hosts": {}}}
    inv_dict["all"]["hosts"] = {k: None for k in devices}

    with open('inventory.yaml', 'w') as inv:
        yaml.safe_dump(inv_dict, inv, default_flow_style=False,
                       explicit_start=False,
                       encoding='utf-8')

    print(devices)
    for d in devices:
        config = dict()
        config['config'] = nso.get_device_config(d)['tailf-ncs:config']
        with open('host_vars/{}.yaml'.format(d), 'w') as fh:
            print("Generating host_vars for {}".format(d))
            yaml.dump(config, fh, default_flow_style=False,
                      explicit_start=False)


if __name__ == "__main__":
    main()
