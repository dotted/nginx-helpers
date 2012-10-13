"""
Copyright (c) 2012, Bo Fjord Jensen <bo@bxd.dk>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import argparse
python3 = False
try:
    import urllib2
except ImportError:
    python3 = True
    import urllib.request as urllib2

parser = argparse.ArgumentParser()
parser.add_argument("output_file", help="Path to the file you wish to write")
args = parser.parse_args()

try:
    with open(args.output_file, "w") as f:
        f.write("# Cloudflare\n")
        f.write("# IPv4\n")

        ipv4_repsonse = urllib2.urlopen('https://www.cloudflare.com/ips-v4')
        if python3: ipv4_html = str(ipv4_repsonse.read(), encoding = "utf8")
        else: ipv4_html = ipv4_repsonse.read()
        ipv4_list = ipv4_html.split("\n")

        ipv6_repsonse = urllib2.urlopen('https://www.cloudflare.com/ips-v6')
        if python3: ipv6_html = str(ipv6_repsonse.read(), encoding = "utf8")
        else: ipv6_html = ipv6_repsonse.read()
        ipv6_list = ipv6_html.split("\n")

        for ip in ipv4_list:
            f.write("set_real_ip_from\t" + ip + ";\n")

        f.write("# IPv6\n")

        for ip in ipv6_list:
            f.write("set_real_ip_from\t" + ip + ";\n")

        f.write("real_ip_header\t\tCF-Connecting-IP;\n")
except IOError:
    print("Could not write to file, perhaps you need to sudo?")
