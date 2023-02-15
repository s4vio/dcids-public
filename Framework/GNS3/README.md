## Network configuration
### Networks

- DMZ:           192.168.100.0/24
- Intranet:      192.168.200.0/21


#### DMZ

- #0 (DMZ 0)
```
#0 192.168.100.0/25       192.168.100.1   - 192.168.100.126    192.168.100.127
```

- #1 (DMZ 1)
```
192.168.100.128/25     192.168.100.129 - 192.168.100.254    192.168.100.255
```

#### Intranet

- #2 (Intranet)
```
192.168.200.0/24      192.168.200.1  - 192.168.200.254  192.168.200.255
```
- #3 (SOC)
```
192.168.201.0/24      192.168.201.1  - 192.168.201.254  192.168.201.255
```
- #4 (Datacenter)
```
192.168.202.0/24      192.168.202.1  - 192.168.202.254  192.168.202.255
```
- #5 (Enterprise 1)
```
192.168.203.0/24      192.168.203.1  - 192.168.203.254  192.168.203.255
```
- #6 (Enterprise 2)
```
192.168.204.0/24      192.168.204.1  - 192.168.204.254  192.168.204.255
```
- #7 (IT Department)
```
192.168.205.0/24      192.168.205.1  - 192.168.205.254  192.168.205.255
```

### VLANS

- Vlan 100 (Red): DMZ 1
- Vlan 201 (Gray): SOC
- Vlan 202 (Blue): Datacenter
- Vlan 203 (Orange): Enterprise 1
- Vlan 204 (Green): Enterprise 2
- Vlan 205 (Yellow): IT Department


### IP ADDRESS

```
Border-Router   eth0        192.168.122.206/24 (DHCP)
                eth1        192.168.100.1/25
```
```   
                e0          192.168.100.2/25 
Firewall        e1          192.168.100.129/25
                e2          192.168.200.1/24
```                
```
Router          eth0        192.168.200.2/24
                eth1.201    192.168.201.1/24 (Vlan SOC)
                eth2.202    192.168.202.1/24 (Vlan Datacenter)
                eth2.203    192.168.203.1/24 (Vlan Enterprise 1)
                eth2.204    192.168.204.1/24 (Vlan Enterprise 2)
                eth3        192.168.122.139  (DHCP/Host)
```
```
elasticsearch   eth0        192.168.201.2
```
```
kibana          eth0        192.168.201.3
```
```
redis           eth0        192.168.201.4
```
```
logstash        eth0        192.168.201.5    
```
```
master-0        ens4        192.168.202.2
```
```
worker-0        ens4        192.168.202.3
```
```
worker-1        ens4        192.168.202.4
```

## Vyos configuration


### Vyos Border-Router

```
vyos@Border-Router# set system host-name Border-Router
vyos@Border-Router# set system time-zone Brazil/East

vyos@Border-Router# set interfaces ethernet eth0 address dhcp
vyos@Border-Router# set interfaces ethernet eth1 address 192.168.100.1/25

vyos@Border-Router# set protocols static route 0.0.0.0/0 next-hop 192.168.122.1
vyos@Border-Router# set protocols static route 192.168.100.0/24 next-hop 192.168.100.2
vyos@Border-Router# set protocols static route 192.168.200.0/21 next-hop 192.168.100.2

vyos@Border-Router# set nat source rule 100 outbound-interface 'eth0'
vyos@Border-Router# set nat source rule 100 source address '192.168.0.0/16'
vyos@Border-Router# set nat source rule 100 translation address 'masquerade'
```

### Vyos Router

```
vyos@Router# set system host-name Router
vyos@Router# set system time-zone Brazil/East

vyos@Router# set interfaces ethernet eth0 address 192.168.200.2/24

vyos@Router# set protocols static route 0.0.0.0/0 next-hop 192.168.200.1
vyos@Router# set protocols static route 192.168.122.1/32 next-hop 192.168.200.2

vyos@Router# set interfaces ethernet eth1 vif 201 address '192.168.201.1/24'
vyos@Router# set interfaces ethernet eth1 vif 201 description 'VLAN 201 (SOC)'

vyos@Router# set interfaces ethernet eth2 vif 202 address '192.168.202.1/24'
vyos@Router# set interfaces ethernet eth2 vif 202 description 'VLAN 202 (Datacenter)'

vyos@Router# set interfaces ethernet eth2 vif 203 address '192.168.203.1/24'
vyos@Router# set interfaces ethernet eth2 vif 203 description 'VLAN 203 (Enterprise 1)'

vyos@Router# set interfaces ethernet eth2 vif 204 address '192.168.204.1/24'
vyos@Router# set interfaces ethernet eth2 vif 204 description 'VLAN 204 (Enterprise 2)'

vyos@Router# set interfaces ethernet eth3 address dhcp

vyos@Router# set nat source rule 100 outbound-interface 'eth0'
vyos@Router# set nat source rule 100 source address '192.168.122.1/32'
vyos@Router# set nat source rule 100 translation address 'masquerade'
```

## Pfsense

- Configure NAT for Internet (Outbound)
- Create gateway and static routes
- Configure DNS server
- Configure rules for each zones



### Clear snort rules

```
pfctl -t snort2c -T flush
pfctl -t snort2c -T delete 
```