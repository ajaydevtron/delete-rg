from datetime import date
import subprocess as sp
from datetime import *
import datetime
import os ,sys
username=sys.argv[1]
password=sys.argv[2]
tenantid=sys.argv[3]

def delete():
    date=datetime.datetime.today().strftime('%Y-%m-%d')
    output = sp.getoutput(f'az group list --tag schedule-deletion={date} --query [].name  -o tsv')
    x=output.split()
    for i in x:
        print("should be delete",i)
        exit_status =os.system(f'az group delete -n {i} -y')
        if(exit_status==0):
            print("deleted RG"+" --> "+ i)
        else:
            print("Command fail to execute with exit status -> %d" % exit_status)

def auth():
    authoutput=sp.getstatusoutput("az login --service-principal -u {} -p {} --tenant {}".format(username,password,tenantid))
    return authoutput
authout=auth()
if(authout[0]==0):
    print("Authentication is successed")
    delete()
else:
    print("Authentication failed",authout[1])
