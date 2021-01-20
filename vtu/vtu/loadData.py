
import os
import sys
sys.path.append('VTU/vtu')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vtu.settings")
from models import TrackNotesDownlods,OTPValidate,ContactUs,TermsAndConditions, AdminEmailId, EmailConfig,MasterSemesters,MasterBranches,MasterNotes, MasterSubjects, MasterServiceHits,MasterQuestionPapers, MasterVideoLab, DeviceAuth, AppVersion, AppForceUpdateRequired, MasterSyllabusCopy,MasterAbout



def main():
  f = open("Scripts/data.txt", "r")
  for x in f:
    print(x)
    print(x.split())
#     ws_semester = MasterSemesters.objects.filter(sem_name = sem).first()
#      ws_branch = MasterBranches.objects.filter(branch_name = branch).first()
#subject_branch
#subject_semester
#subject_code
#subject_name
#Description
if __name__ == '__main__':
    main()