import socket
import json
import urllib2
import sys
# {[src_ip: ip, dest_ip: ip, port : port, proto : proto, status: status],[]}


def test_connectivity(dest_ip, port, proto):
    if(proto == "tcp"):
        proto_type = socket.SOCK_STREAM
    elif(proto == "udp"):
        proto_type = socket.SOCK_DGRAM

    sock = socket.socket(socket.AF_INET, proto_type)
    status = sock.connect_ex((dest_ip, port))
    return status


def get_rule_list():
    try:
        data = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
    with open('rules.list') as f:
        json.dumps(data, f)
    return "rules.list"


def print_to_file(dest_ip, port, proto, status):
    src_ip = socket.getfqdn()
    with open("status.csv", "w") as f:
        f.writeline(src_ip+","+dest_ip+","+port+","+proto+","+status+"\n")


def send_status(sendfile, src_ip):
    with open(sendfile) as f:
        data = json.load(f)
    url = 'http://search.yahooapis.com/ContentAnalysisService/V1/'

    params = urllib2.urlencode({
                                'src_ip': src_ip,
                                'data': data})
    result = urllib2.urlopen(url, params).read()
    print result
# make connection to server and then send the file


def main(argv=None):
    inputfile = get_rule_list()
    out_file = "tmp_status.json"
    with open(out_file) as outf:
        src_ip = socket.getfqdn()
        json.dumps('{', outf)
        with open(inputfile) as f:
            for line in f:
                print line
                dest_ip, port, proto = line.split(',')
                status = test_connectivity(dest_ip, port, proto)
                if(status == 0):
                    print "Success"
                    status_str = "SUCCESS"
                else:
                    print "Failure"
                    status_str = "FAILED"
                json.dumps('[src_ip:' + src_ip +
                           ',dest_ip:'+dest_ip +
                           ',port:' + port +
                           ',protocol:'+proto +
                           ',status:' + status_str +
                           '],', outf)

        json.dumps('}', outf)
    send_status(out_file)
    return 0

if __name__ == "__main__":
    sys.exit(main())

# import json
# import urllib2
# json.load(urllib2.urlopen("url"))
# http://www.pythonlearn.com/html-008/cfbook014.html
# https://developer.yahoo.com/python/python-rest.html
