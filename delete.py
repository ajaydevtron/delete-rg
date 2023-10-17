from datetime import date
import subprocess as sp
from datetime import *
import os ,sys
import yaml
username=sys.argv[1]
password=sys.argv[2]
tenantid=sys.argv[3]


lock_list=[]
def lock_list_fun():
    command="az lock list -o yaml >locklist.yaml"
    result = sp.run(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    exit_code = result.returncode
    error=result.stderr
    if exit_code != 0 :
        print("Canot find the locklist having error====>")
        print(error)
        print('\n')
        exit()
    with open('locklist.yaml', 'r') as file:
        temp_list = yaml.safe_load(file)
    for i in temp_list:
        temp=i['resourceGroup']
        lock_list.append(temp)

    print("Locked RG are ====> ")
    print(lock_list)


def delete():
    lock_list_fun()
    print("\n\n\n")
    sp.getoutput('az group list --tag schedule-deletion   -o yaml > results.yaml')

    with open('results.yaml', 'r') as file:
        yaml_data = yaml.safe_load(file)

    for entry in yaml_data:
        rg_name=entry['name']
        date_taged=entry['tags']['schedule-deletion']
        date_taged = datetime.strptime(date_taged, "%Y-%m-%d").date()
        today_date = datetime.now().date()
        print(rg_name + "===========>" + str(date_taged))


        if today_date == date_taged or today_date > date_taged:
            if rg_name in lock_list:
                print(rg_name,"======>  This resource is locked so it canot be deleted.")
            else:
                command=f'az group delete -n {rg_name} -y'
                result = sp.run(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE,text=True)
                exit_code = result.returncode
                error=result.stderr
                if exit_code != 0 :
                    print(f"The resourceGroup {rg_name} is not deleted having exitcode {exit_code} with below reason ")
                    print(error)
                    print("\n")
                else:
                    print("Deleted RG=====>" + rg_name)
        else:
            print(f"{rg_name} resource group will be delete in {date_taged} after {(date_taged - today_date).days} days")


def auth():
    authoutput=sp.getstatusoutput("az login --service-principal -u {} -p {} --tenant {}".format(username,password,tenantid))
    return authoutput
authout=auth()
print("=================================================================")
if(authout[0]==0):
    print("Authentication is successed")
    delete()
else:
    print("Authentication failed",authout[1])
print("=================================================================")
