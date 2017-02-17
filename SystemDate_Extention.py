
    # 57680b6b0009e8724ab4718bd8aed09b portfolioID for 2017
    # 57b3847e008ced8cfd57553dd3d7b3b5 test portfolioID 2017

    



###########################################################################################
#
# NOTES REGARDING THIS SCRIPT (Python v.2.7.12) VERSION 1.0 DECEMBER 2016 (Evans & Adkins)
#
###########################################################################################
#
# For The WorkFront 2017 Portfolio
# 
# This file was chartered by Quotit Plan Maintenance to work in conjunction with WorkFront
# The purpose of this file to update the planned completion date (pcd) field in WorkFront
#     for projects which are late. This happens when the pcd is one day before the current
# This means that the project is late from the original estimate, which will then get
#     surfaced to the brokers in iPro: problem.
# This script: after identifing projects which are late, updates the pcd by moving it
#     forward two weeks. This does not happen for 'Live' nor 'Discontinued' projects.
# Since some projects need to have their ETAs monitored and manually updated,
#     a new field in WorkFront (in the 'Quotit PM Tracking' custom form) allows the user
#     to turn off the auto-update. Default set to on.
# Windows Task Scheduler is setup to run this script every morning under the name:
#     'Update Expired Planned Completion Date in WorkFront'.
#
###########################################################################################


from api import StreamClient, ObjCode, AtTaskObject
from datetime import datetime, timedelta
import time
from PMtools import masking, mailsend



long_currentDate = str(datetime.today() + timedelta(days=-1))
currentDate , time = long_currentDate.split()
projIDlist = []

################################################################################

def getProject():
    global currentDate
    global projIDlist
    results = client.search(ObjCode.PROJECT,
                            {'portfolioID':'57680b6b0009e8724ab4718bd8aed09b', 
                             'plannedCompletionDate':str(currentDate),
                             '$$LIMIT':2000, 
                             'DE:project:Auto Update ETA':'Yes'},
                            fields=['plannedCompletionDate', 'name', 'status']
    )
    
    # 57680b6b0009e8724ab4718bd8aed09b portfolioID for 2017
    # 57b3847e008ced8cfd57553dd3d7b3b5 test-portfolioID 2017
         
    for p in results:
        project = AtTaskObject(p)
        if project.status == 'CPL':   # Live
            pass
        elif project.status == 'CUR': # Live with Current Update
            pass
        elif project.status == 'DED': # Disconintued
            pass
        elif project.status == 'IPT': # Discontinued for SEP
            pass
        else:                         # All Other Statuses
            projIDlist.append({'projID':project.ID,'projName':project.name})
    
def updateProjectPCD():
    global currentDate
    global projIDlist
    # Adding 2 weeks
    long_currentDatePlus2W = str(datetime.today() + timedelta(weeks=2))
    currentDatePlus2W, time = long_currentDatePlus2W.split()
    for p in projIDlist:
        results = client.put(
            ObjCode.PROJECT,
            p['projID'],
            {'plannedCompletionDate':currentDatePlus2W}
        )
    # Informs User of Result via the shell
    if len(projIDlist) < 1:
        print 'No projects to update'
    else:
        print 'Eta update complete'
        print str(len(projIDlist)) + ' project(s) updated'
        
def writeToFile(listData):
    outFile = open('Change.log','a+')
    if len(listData) < 1:
        outFile.write(str(datetime.now().strftime("%Y-%m-%d %H:%M")) + ' | No update' + '\n') 
    else:
        templistforemail = []
        # Records to Change.log and Appends the record to a temp list 
        for item in listData:
            outFile.write(str(datetime.now().strftime("%Y-%m-%d %H:%M")) + ' | ' + item['projID'] + ' | ' + item['projName'] + '\n')
            templistforemail.append(str(datetime.now().strftime("%Y-%m-%d %H:%M")) + ' | ' + item['projID'] + ' | ' + item['projName'] + '\n')
        # Sends email to each person in email list
        names = ['brian.evans@quotit.com','matthew.smithson@quotit.com','andrew.kaplan@quotit.com']
        for name in names:
            mailsend.sendmail(''.join(templistforemail), name)
    outFile.close()

    # Because it is awesome and we can
def wizardCall():
    with open('wizard.txt', 'r') as fin:
        print fin.read()
    fin.close()

################################################################################

# Main()
if __name__ == '__main__':
    wizardCall()
    username = 'brian.evans@quotit.com'
    password = 'CCllrMzGU' # encrypted password
    client = StreamClient('https://wordandbrown.attask-ondemand.com/attask/api/')
    client.login(username,masking.unmask(password))
    getProject()
    updateProjectPCD()
    writeToFile(projIDlist)
    


