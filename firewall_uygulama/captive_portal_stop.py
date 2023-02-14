import subprocess
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/firewall_uygulama/uygulama/.env")
PORT = os.environ.get("PORT")
IFACE = os.environ.get("IFACE")
IP_ADDRESS = os.environ.get("IP_ADDRESS")

subprocess.call(["iptables", "-t", "nat", "-D", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT","--to-destination", IP_ADDRESS + ":" + str(PORT)])  # iptables ayarları iptal edilir
subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j", "ACCEPT"])
subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT), "-d", IP_ADDRESS, "-j","ACCEPT"])
subprocess.call(["iptables", "-D", "FORWARD", "-i", IFACE, "-j", "DROP"])
