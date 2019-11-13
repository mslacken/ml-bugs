#!/usr/bin/python3
#
#  dir(bug)
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_bug_fields', '_update_dict', 'addcc', 'addcomment', 'assigned_to', 'autorefresh', 'blocks', 'bugzilla', 'cc', 'cf_biz_priority', 'cf_blocker', 'cf_foundby', 'cf_it_deployment', 'cf_marketing_qa_status', 'cf_nts_priority', 'classification', 'close', 'component', 'creation_time', 'creator', 'deletecc', 'depends_on', 'flags', 'get_attachment_ids', 'get_flag_status', 'get_flag_type', 'get_flags', 'get_history_raw', 'getcomments', 'groups', 'id', 'is_cc_accessible', 'is_confirmed', 'is_creator_accessible', 'is_open', 'keywords', 'last_change_time', 'op_sys', 'platform', 'priority', 'product', 'qa_contact', 'refresh', 'reload', 'resolution', 'see_also', 'setassignee', 'setstatus', 'severity', 'status', 'summary', 'target_milestone', 'updateflags', 'url', 'version', 'weburl', 'whiteboard']

import pprint
import bugzilla
import time
import datetime
import json
import argparse
import inspect
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read in bugzilla.')
    parser.add_argument('-u','--url',dest='url',default='https://bugzilla.opensuse.org',help='url of bugzilla sever')
    parser.add_argument('-o','--output',dest='output',default='bugs.txt',help='name of the output file')
    parser.add_argument('-c','--component',dest='component',default="Development",help='name of the component to query')
    
    args = parser.parse_args()
    # public test instance of bugzilla.redhat.com. It's okay to make changes
    ofile = open(args.output,'w')

    my_api = bugzilla.Bugzilla(args.url)

    bugs_rec = []

    bz_query = my_api.build_query(
            component = args.component,
            status = "RESOLVED",
            product = "openSUSE Distribution")
    try:
        bugs_rec = my_api.query(bz_query)
    except Exception as excep_se: 
        #data["is_allowed"] = False
        print("Got exception")
        print(excep_se)
        sys.exit(1)
    print("got %i bugs" % len(bugs_rec))
    for bug in bugs_rec:
        bug_dict = {}
        bug_dict["id"] = bug.id
        #bug_dict["blocks"] = bug.blocks
        ctime = datetime.datetime.strptime(str(bug.creation_time), '%Y%m%dT%H:%M:%S')
        bug_dict["ctime"] = time.mktime(ctime.timetuple())
        comments = bug.getcomments()
        comment_lst = []
        for my_comment in comments:
            comment_lst.append(my_comment["text"])
        bug_dict["comments"] = comment_lst
        etime = datetime.datetime.strptime(str(comments[-1]["creation_time"]), '%Y%m%dT%H:%M:%S')
        bug_dict["etime"] = time.mktime(etime.timetuple())
        bug_dict["count"] = comments[-1]["count"]
        bug_dict["text"] = comments[0]["text"]
        bug_dict["summary"] = bug.summary 
        bug_dict["component"] = bug.component
        bug_dict["product"] = bug.product
        ofile.write(json.dumps(bug_dict))
        ofile.write("\n")
        ofile.flush()
        print("wrote #%i" % bug.id)
# call with
# for comp in Apache AppArmor AutoYast Basesystem Bootloader Cloud:Images Cloud:Tools Commercial Containers Development Documentation Evolution Firefox GNOME 'High Availability' Installation 'KDE Applications' 'KDE Workspace(Plasma)' KDE3 Kernel KVM LibreOffice libzypp 'Live Medium' LXDE LXQT Maintenance Network OpenStack Other Patterns Printing 'Release Notes' Ruby Salt Samba Security Sound Translations 'Upgrade Problems' Virtualization:Other Virtualization:Tolls Virtualization:VMDP WSL X.org 'X11 3rd Party Driver' 'X11 Applications' Xen Xfce YaST2; do echo "$comp"; done
