import scapy.all as sc

def scaner(ip):
    # arping()
    # scapy.all.arping(ip)
    # arp_req = scapy.all.ARP(pdst=ip)
    # print(arp_req.summary())
    # scapy.all.ls(scapy.all.ARP())
    # broadcast = scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(broadcast.summary())
    arp_req_broad = sc.Ether(dst="ff:ff:ff:ff:ff:ff")/sc.ARP(pdst=ip)
    answer_yes = sc.srp(arp_req_broad, timeout=1, verbose=False)[0]
    print('IP-Adress\t\t\tMAC-Adress\n----------------------------------------------')
    for elem in answer_yes:
        print(elem[1].psrc + '\t\t\t' + elem[1].hwsrc)
    print(elem[1].pdst + '\t\t\t' + elem[1].hwdst)
scaner(['192.168.100.1','192.168.100.57', '192.168.100.2'])
