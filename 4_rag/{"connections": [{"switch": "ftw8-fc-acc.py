{"connections": [{"switch": "ftw8-fc-acc-sw-11-1.amazon.com", "interface_ip": "10.19.64.96", "interface_port": "TenGigabitEthernet1/0/1","outgoing_interface_ip":"10.19.64.95", "outgoing_interface_port": "TenGigabitEthernet1/1/1", "vlan": "1", "vlan_type": "native", "version": "16.9.3", "color": "lightblue", "switchport_type": "L2", "ospf_features": "", "bfd_interval": ""}, {"switch": "ftw8-fc-acc-sw-11-1.amazon.com", "interface_ip": "10.19.64.96", "interface_port": "TenGigabitEthernet2/0/1","outgoing_interface_ip":"10.19.64.95", "outgoing_interface_port": "TenGigabitEthernet1/1/2", "vlan": "1", "vlan_type": "native", "version": "16.9.3", "color": "lightblue", "switchport_type": "L2", "ospf_features": "", "bfd_interval": ""}, {"switch": "ftw8-fc-acc-sw-11-9.amazon.com", "interface_ip": "10.19.64.97", "interface_port": "TenGigabitEthernet1/0/9","outgoing_interface_ip":"10.19.64.98", "outgoing_interface_port": "TenGigabitEthernet1/1/1", "vlan": "1", "vlan_type": "native", "version": "16.9.3", "color": "lightblue", "switchport_type": "L2", "ospf_features": "", "bfd_interval": ""}, {"switch": "ftw8-fc-acc-sw-11-9.amazon.com", "interface_ip": "10.19.64.97", "interface_port": "TenGigabitEthernet2/0/9","outgoing_interface_ip":"10.19.64.98", "outgoing_interface_port": "TenGigabitEthernet1/1/2", "vlan": "1", "vlan_type": "native", "version": "16.9.3", "color": "lightblue", "switchport_type": "L2", "ospf_features": "", "bfd_interval": ""}, {"switch": "ftw8-fc-agg-t1-a-4.amazon.com", "interface_ip": "100.101.1.4", "interface_port": "TenGigabitEthernet2/0/34","outgoing_interface_ip":"100.101.1.5", "outgoing_interface_port": "TenGigabitEthernet1/0/11", "vlan": "", "vlan_type": "", "version": "17.3.3", "color": "lightblue", "switchport_type": "L3", "ospf_features": "", "bfd_interval": ""}, {"switch": "ftw8-fc-agg-t1-a-3.amazon.com", "interface_ip": "100.101.0.180", "interface_port": "TenGigabitEthernet2/0/33","outgoing_interface_ip":"100.101.0.181", "outgoing_interface_port": "TenGigabitEthernet1/0/11", "vlan": "", "vlan_type": "", "version": "17.3.3", "color": "lightblue", "switchport_type": "L3", "ospf_features": "ipv6 ospf 100 area 0 ipv6 ospf network point-to-point", "bfd_interval": "750 min_rx 750 multiplier 3"}, {"switch": "ftw8-fc-agg-t1-a-2.amazon.com", "interface_ip": "100.101.0.100", "interface_port": "TenGigabitEthernet1/0/34","outgoing_interface_ip":"100.101.0.101", "outgoing_interface_port": "TenGigabitEthernet1/0/11", "vlan": "", "vlan_type": "", "version": "17.3.3", "color": "lightblue", "switchport_type": "L3", "ospf_features": "", "bfd_interval": ""}, {"switch": "ftw8-fc-agg-t1-a-1.amazon.com", "interface_ip": "100.101.0.20", "interface_port": "TenGigabitEthernet1/0/33","outgoing_interface_ip":"100.101.0.21", "outgoing_interface_port": "TenGigabitEthernet1/0/11", "vlan": "", "vlan_type": "", "version": "17.3.3", "color": "lightblue", "switchport_type": "L3", "ospf_features": "", "bfd_interval": ""}], "switch_name": "ftw8-fc-dis-r-11-1", "switchport_enabled_ports": ["Po1", "TenGigabitEthernet1/0/1", "TenGigabitEthernet1/0/9"], "switchport_access_ports": ["TenGigabitEthernet1/0/1", "TenGigabitEthernet1/0/9"], "trunk_enabled_ports": ["Po1", "TenGigabitEthernet1/0/1", "TenGigabitEthernet1/0/9"], "vlan_enabled_ports": ["TenGigabitEthernet1/0/1", "TenGigabitEthernet1/0/9"], "Po1": ["TenGigabitEthernet1/0/1", "TenGigabitEthernet2/0/1"], "Po9": ["TenGigabitEthernet1/0/9", "TenGigabitEthernet2/0/9"], "All Port Channels": ["Po1", "Po9", "Po101", "Po102", "Po103", "Po104"], "macsec_interfaces": ["TenGigabitEthernet1/0/33", "TenGigabitEthernet1/0/34"], "ospf_interfaces": ["TenGigabitEthernet2/0/33"], "multicast_interfaces": ["TenGigabitEthernet2/0/33", "TenGigabitEthernet2/0/34"]}