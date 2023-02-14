import subprocess

PORT = 9090  # the port in which the captive portal web server listens
IFACE = "wlan2"  # the interface that captive portal protects//??
IP_ADDRESS = "172.16.0.1"  # the ip address of the captive portal (it can be the IP of IFACE)//network ip ile eşleşmeli!

subprocess.call(
    ["iptables", "-t", "nat", "-D", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT",
     "--to-destination", IP_ADDRESS + ":" + str(PORT)])  # iptables ayarları iptal edilir
subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j", "ACCEPT"])
subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
subprocess.call(
    ["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT), "-d", IP_ADDRESS, "-j",
     "ACCEPT"])
subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-j", "DROP"])
