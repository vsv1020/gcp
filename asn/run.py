import requests,json,os
def curl_ip(ip,ip_f):
    url = "https://ipinfo.io/"+ip
    ip_result = requests.get(url).json()
    ip_f.write(ip_result["ip"])
    ip_f.write(",")
    ip_f.write(ip_result["city"])
    ip_f.write(",")
    ip_f.write(ip_result["country"])
    ip_f.write(",")
    ip_f.write(ip_result["org"])
    ip_f.write("\n")
def asn():
    """
    调用命令 curl -s https://ipinfo.io/IP 
    """
    asn_f = open("ip.txt","r")
    ip_f = open("result.txt","w")
    ip_f.write("ip,city,country,org")
    ip_f.write("\n")
    for asn_ip in asn_f:
        if "/" in asn_ip.strip():
            ip = asn_ip.split("/")[0]
            curl_ip(ip,ip_f)
        else:
            ip = asn_ip.strip()
            curl_ip(ip,ip_f)
    asn_f.close()
    ip_f.close()
  

if __name__ == '__main__':
    asn = asn()
    #print(os.system('cat result.txt'))
    print(os.popen('cat result.txt').read())
