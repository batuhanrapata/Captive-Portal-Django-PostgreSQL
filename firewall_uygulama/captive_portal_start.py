import http.server
import subprocess
from http.server import HTTPServer
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="firewall_uygulama/uygulama/.env")

PORT = os.environ.get("PORT")
IFACE = os.environ.get("IFACE")
IP_ADDRESS = os.environ.get("IP_ADDRESS")

subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", "53", "-j", "ACCEPT"])  # dns portu
subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-p", "tcp", "--dport", str(PORT), "-d", IP_ADDRESS, "-j","ACCEPT"])  # captive portal portu
subprocess.call(["iptables", "-A", "FORWARD", "-i", IFACE, "-j", "DROP"])  # diğer tüm paketler iptal edilir
httpd = HTTPServer(('', PORT), http.server.SimpleHTTPRequestHandler)  # captive portal başlatılır
subprocess.call(["iptables", "-t", "nat", "-A", "PREROUTING", "-i", IFACE, "-p", "tcp", "--dport", "80", "-j", "DNAT", "--to-destination", IP_ADDRESS + ":" + str(PORT)])  # iptables ayarları yapılır
try:  # captive portal başlatılır
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
