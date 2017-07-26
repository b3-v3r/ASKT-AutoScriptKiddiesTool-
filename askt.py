import socket
import os
import sys
import requests
import time
import random
import argparse
import nmap
import re
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan
U  = '\033[4m'
M = '\033[1;35;32m' # magenta


work_dir = []
open_port = []
crawl_url = ''
sql_bool   = False
xxs_bool   = False
robot_bool = False
def clean():
    os.system('clear')
def print_line():
    print(C+'='*40+W)
def checkroot():
    if not os.geteuid() == 0:
        print(R+'#'*27)
        print(R+'#'+G+'Run this program in root!'+R+'#')
        print(R+'#'*27)
        exit()

def desc():
    print(T+'''
    This program was created for review and not for causing harm.
    Usage of hunner for attacking targets without prior mutual consent is illegal.
    Developers assume no liability and are not responsible for any misuse or damage caused by this program.
    '''+W)
    des = input('Yes/no:')
    if des.lower() == 'yes':
        pass
    else:
        exit()
def banner():
    banner1 = B+"""
 _______  _______  ___   _  _______
|   _   ||       ||   | | ||       |
|  |_|  ||  _____||   |_| ||_     _|
|       || |_____ |      _|  |   |
|       ||_____  ||     |_   |   |
|   _   | _____| ||    _  |  |   |
|__| |__||_______||___| |_|  |___|
    """+R+'Author: B3@v3r'+W
    banner2 = G+"""
             """+R+'Coder: B3@v3r'+G+"""
   _____    _____________  __.___________
  /  _  \  /   _____/    |/ _|\__    ___/
 /  /_\  \ \_____  \|      <    |    |
/    |    \/        \    |  \   |    |
\____|__  /_______  /____|__ \  |____|
        \/        \/        \/
              """+B+'Version: 1.0'+"\n"
    banner3 = M+"""
 _______  _______  _       _________
(  ___  )(  ____ \| \    /\\__   __/
| (   ) || (    \/|  \  / /   ) (
| (___) || (_____ |  (_/ /    | |
|  ___  |(_____  )|   _ (     | |
| (   ) |      ) ||  ( \ \    | |
| )   ( |/\____) ||  /  \ \   | |
|/     \|\_______)|_/    \/   )_(

        """+B+'Version: 1.0'+"""
        """+"Coder: B3@v3r"+W
    m = random.randint(0, 2)
    if m == 0:
        print(banner1+"\n")
    elif m == 1:
        print(banner2+"\n")
    elif m == 2:
        print(banner3+"\n")

def pars_args_check():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Target host')
    args = parser.parse_args()
    if args.host:
        global host
        host = args.host
    else:
        sys.exit('Error! Usage: python3 askt.py --host <host>/<host:port>')

def sql():
    global sql_bool
    print(O+'Start scan SQL vuln'+W)
    sql_payload = [
    "'",
    'or 1=/=1',
    'and or 1==2',
    'select or select'
    'and select *',
    '=-12',
    "union and or -12' "
    ]
    sql_error = ['Query failed',
    'SQL syntax error',
    'Query failed',
    'Unknown error',
    'MySQL fetch',
    'Syntax error'
    ]
    num_pay = 0
    error = False
    for payload in sql_payload:
        if sql_bool or error:
            break
        num_pay +=1
        try:
            packet = host+' '+payload
            html = requests.get(packet).text
            t = 0
            for check_sql in sql_error:
                if check_sql in html:
                    print(R+'['+time.strftime("%H:%M:%S")+']'+M+'[SQL]Payload: '+packet+' work')
                    print(M+'[++] Site have sql vuln'+W)
                    sql_bool = True
                    break
                elif check_sql not in html and t == 5:
                    print(M+'['+time.strftime("%H:%M:%S")+']'+R+'[SQL]Payload: '+packet+' not work'+W)
                else:
                    t += 1
        except:
            print(R+'This site not have Sql vuln'+W)
            error = True
            break
    if not sql_bool:
        print(R+'[-] This site not have Sql vuln'+W)

def xxs():
    global xxs_bool
    print(O+'Start scan XXS vuln'+W)
    xxs_payload = [
    ";<script>alert('xxs');</script>",
    ';<script>alert("xxs");</script>',
    '\><script>alert("xxs")</script>',
    '<sCriPt>alert("xxs");</sCriPt>',
    '</title><body onload=alert("XSS")>',
    "></title></style></scrIpt><scRipt>alert('XXS')</scrIpt>"
    ]
    for xxs_text in xxs_payload:
        if xxs_bool:
            break
        pack = host+xxs_text
        try:
            text = requests.get(pack).text
        except:
            print(G+'Site not have XXS vuln'+W)
        if xxs_text in text:
            print(R+'['+time.strftime("%H:%M:%S")+']'+M+'[XXS]Payload: '+pack+' work'+W)
            print(M+'[++] This site have XXS vuln'+W)
            xxs_bool = True
        else:
            print(M+'['+time.strftime("%H:%M:%S")+']'+R+'[XXS]Payload: '+pack+' not work'+W)
    if not xxs_bool:
        print(R+'Site not have XXS vuln')
def url_short():
    if "http://" in host:
        if 'www.' in host:
            host_short = host.split('http://')[1]
            host_short = host.split('www.')[1]
        else:
            host_short = host.split('http://')[1]
    elif 'https://' in host:
        if 'www' in host:
            host_short = host.split('https://')[1]
            host_short = host.split('www.')[1]
        else:
            host_short = host.split('https://')[1]
    return host_short
def ip_site():
    host_short = url_short()
    ind_short_url =  host_short.index('/')
    host_short    =  host_short[:ind_short_url]
    global crawl_url
    crawl_url = host_short
    ip = socket.gethostbyname(host_short)
    return ip

def info_site():
    print(O+'Info site:'+W)
    print(M+'Url -=>'+host+W)
    ip = ip_site()
    print(M+'IP host -=> '+ip+W)

def dir_site_search():
    top_dir = [
    '/admin/',
    '/admin.php',
    '/login/'
    '/login.php',
    '/wp-login/'
    '/wp-login.php',
    '/robots.txt',
    '/phpmyadmin.php',
    '/phpinfo.php',
    '/admin/admin.php',
    '/admin/login.js',
    '/adm.php',
    '/moderator/',
    '/moderator/admin.php',
    '/moderator.php',
    '/moderator.js',
    '/panel-administracion/admin.php',
    '/panel-administracion/admin.js',
    '/webadmin.php',
    '/webadmin/admin.js',
    '/webadmin/admin.php',
    '/memberadmin/',
    '/memberadmin.js',
    '/memberadmin.php'
    ]
    print(O+'Dir and basic admin finger'+W)
    host_ = url_short()
    ind_short_url =  host_.index('/')
    host_short    =  host_[:ind_short_url]
    for dirs in top_dir:
        res = requests.get('http://'+host_short+dirs)
        if res.status_code == 200:
            print(M+'Dir: '+host_short+dirs+' code: '+str(res.status_code)+W)
            work_dir.append(dirs)
        elif res.status_code == 300:
            print(G+'Dir: '+host_short+dirs+' code: '+str(res.status_code)+W)
        else:
            print(R+'Dir: '+host_short+dirs+' code: '+str(res.status_code)+W)

def port_scan():
    print(O+'Start scan port'+W)
    nm = nmap.PortScanner()
    ip = ip_site()
    nm.scan(ip, '1-999')
    ports_tcp = nm[ip].all_tcp()
    ports_udp = nm[ip].all_udp()
    print(M+'Open ports:'+W)
    if len(ports_tcp) > 0:
        for port_tcp in ports_tcp:
            print(M+'| '+str(port_tcp)+' |'+' tcp | open |'+W)
    if len(ports_udp) > 0:
        for port_udp in ports_udp:
            print(M+'| '+str(ports_udp)+' |'+' udp | open |'+W)

def cloudflare_detect():
    print(O+'Start detect cloudflare'+W)
    res = requests.get(host)
    headers = res.headers
    server = headers.get('Server')
    print(M+'Response: '+server+W)
    if 'cloudflare' in server:
        print(R+'Detect cloudflare'+W)
    else:
        print(G+'Cloudflare not detect'+W)

def crawl():
    print(M+'Search start...'+W)
    try:
        main_res = requests.get('http://'+crawl_url).text
    except:
        print(R+'Error open site'+W)
    for url_site in re.findall('<a href="(.*?)"', main_res):
        if '.php' or '.html' in url_site:
            print(M+'Found: '+'http://'+crawl_url+'/'+url_site+W)

def recon():
    print(O+'Start recon'+W)
    crawl()
def scan_main():
    print(O+'[+] Start scan host -=>'+M+host+W)
    print_line()
    info_site()
    print_line()
    cloudflare_detect()
    print_line()
    sql()
    print_line()
    xxs()
    print_line()
    port_scan()
    print_line()
    dir_site_search()
    print_line()
    recon()
    print(P+'End scan'+W)
def main():
    clean()
    desc()
    clean()
    banner()
    checkroot()
    pars_args_check()
    scan_main()
main()
