FROM Python
WORKDIR ./firewall_uygulama
COPY . /firewall_uygulama
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt
CMD ["python", "captive_portal_start.py"]
CMD ["python", "manage.py", "runserver"]
EXPOSE 9090 9090
