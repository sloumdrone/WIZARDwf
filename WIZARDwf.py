###########################################################################################
#
# NOTES REGARDING THIS SCRIPT (Python v.2.7.12) VERSION 1.0 DECEMBER 2016 (Evans & Adkins)
#
###########################################################################################
# UPDATES ALL EXPIRED PROJECTS TO HAVE A NEW DEADLINE TWO WEEKS OUT PROVIDED THE PROJECTS
# EXPIRED THE DAY BEFORE THE RUN DAY. USE WITH A CHRON JOB TO RUN DAILY.
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
                            {'portfolioID':'IDgoeshere', 
                             'plannedCompletionDate':str(currentDate),
                             '$$LIMIT':2000, 
                             'DE:project:Auto Update ETA':'Yes'},
                            fields=['plannedCompletionDate', 'name', 'status']
    )
    
         
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
        names = ['foo@bar.com','person@domain.com']
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
    username = 'foo@bar.com'
    password = 'hashed-pw' #an actual password has would go here
    client = StreamClient('https://somedomain.attask-ondemand.com/attask/api/')
    client.login(username,masking.unmask(password))
    getProject()
    updateProjectPCD()
    writeToFile(projIDlist)
    


