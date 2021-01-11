#! /usr/bin/python3

from plumbum import local
import json
import pprint as pp
import sys
import time
import os


def is_ip_dev_exists():
    ip = local["ip"]

    ip_link_str = ip("-j", "link")
    ip_link = json.loads(ip_link_str)
    devs = [d["ifname"] for d in ip_link]

    for dev in devs:
        if dev.startswith("wl"):
            print("pass")
            return True

    print("fail")
    return False


def test_count(ret, to_reboot=-1):
    recfile = "/home/u/testcount.json"
    if os.path.exists(recfile):
        with open("/home/u/testcount.json") as f:
            test_count = json.loads(f.read())
    else:
        test_count = 0
    if test_count > 100:
        print("test pass for 100 times")
        return

    print("Test count previously is", test_count)

    if ret:
        test_count += 1
        with open("/home/u/testcount.json", "w+") as f:
            f.write(json.dumps(test_count))
        if to_reboot >= 0:
            print("I am going to reboot in", to_reboot, "seconds")
            if to_reboot > 0:
                time.sleep(to_reboot)
            local["reboot"]()
    return

ret = is_ip_dev_exists()
test_count(ret, 5)

sys.exit(ret)

