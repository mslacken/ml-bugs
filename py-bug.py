#!/usr/bin/python3
#
#  dir(bug)
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_bug_fields', '_update_dict', 'addcc', 'addcomment', 'assigned_to', 'autorefresh', 'blocks', 'bugzilla', 'cc', 'cf_biz_priority', 'cf_blocker', 'cf_foundby', 'cf_it_deployment', 'cf_marketing_qa_status', 'cf_nts_priority', 'classification', 'close', 'component', 'creation_time', 'creator', 'deletecc', 'depends_on', 'flags', 'get_attachment_ids', 'get_flag_status', 'get_flag_type', 'get_flags', 'get_history_raw', 'getcomments', 'groups', 'id', 'is_cc_accessible', 'is_confirmed', 'is_creator_accessible', 'is_open', 'keywords', 'last_change_time', 'op_sys', 'platform', 'priority', 'product', 'qa_contact', 'refresh', 'reload', 'resolution', 'see_also', 'setassignee', 'setstatus', 'severity', 'status', 'summary', 'target_milestone', 'updateflags', 'url', 'version', 'weburl', 'whiteboard']

import pprint
import bugzilla
import time
import datetime
import json

def getbug_fmt(bzapi,bug_id):
    data = {}
    data["id"] = bug_id
    try:
        bug = bzapi.getbug(bug_id)
    except: 
        data["is_allowed"] = False
    else:
        data["is_allowed"] = True
        data["Component"] = bug.component
        data["Status"] = bug.status
        data["Summary"] = bug.summary
        data["Priority"]  = bug.priority
        data["Severity"] = bug.severity
        ctime = datetime.datetime.strptime(str(bug.creation_time), '%Y%m%dT%H:%M:%S')
        data["ctime"] = time.mktime(ctime.timetuple())
        comments = bug.getcomments()
        etime = datetime.datetime.strptime(str(comments[-1]["creation_time"]), '%Y%m%dT%H:%M:%S')
        data["etime"] = time.mktime(etime.timetuple())
        #print("  Creation  = %s" % time.mktime(creation_time.timetuple()))
        #print("  End time  = %s" % time.mktime(end_time.timetuple()))
        data["Count"] = comments[-1]["count"]
        data["Text"] = comments[0]["text"]
#   print("\nLast comment data:\n%s" % pprint.pformat(comments[-1]))
    return data
    
# public test instance of bugzilla.redhat.com. It's okay to make changes
URL = "bugzilla.opensuse.org"

my_api = bugzilla.Bugzilla(URL)

not_allowed_f_name = 'not_allowed.lst'

bug_end = 1122748
nr_bugs = 10000

not_allowed_lst = []
bugs = {}

# read in list of not allowed bugs
try:
    not_allowed_f = open(not_allowed_f_name,'r')
except:
    print("Could not read %s" % not_allowed_f_name)
else:
    not_allowed_lst = not_allowed_f.read().splitlines()
    not_allowed_lst = list(filter(None,not_allowed_lst))
    for index, item in enumerate(not_allowed_lst):
        not_allowed_lst[index] = int(item)
    not_allowed_f.close()
    print("Read %i not allowed bugs" % len(not_allowed_lst))


for bug_nr in range(bug_end,bug_end - nr_bugs, -1):
    if bug_nr not in not_allowed_lst:
        ret_data = getbug_fmt(my_api,bug_nr)
        if ret_data["is_allowed"]:
            print("Read in bug %i" % bug_nr)
            bugs[bug_nr] = ret_data
        else:
            print("Could not access bug %i" % bug_nr)
            not_allowed_lst.append(bug_nr)

print("Allowed: %s Forbidden: %s" % (len(bugs),len(not_allowed_lst)))
# write out list
if len(not_allowed_lst) != 0:
    not_allowed_f = open(not_allowed_f_name,'w')
    not_allowed_lst = map(lambda x:str(x)+'\n',not_allowed_lst)
    not_allowed_f.writelines(not_allowed_lst)
    not_allowed_f.close()

# write out dict
if len(bugs) != 0:
    with open('bugs.txt','w') as ofile:
        ofile.write(json.dumps(bugs))

