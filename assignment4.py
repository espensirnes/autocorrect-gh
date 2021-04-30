
import autocorrect

#Fill inn these:
ORGANIZATION_NAME='uit-sok-1003-h21'
REPO_NAME='Assignment 4'
TOKEN='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'
#go to "https://github.com/settings/tokens/new" to get a token

#see comments in autocorrect for more information about creating selv correcting tests


#This is the check function that needs to be customized for each assignment

def check(assignment,d):
    """'assignment' is the module where the students write their answer. Students should be asked to write a function with a
    specific name, which you refere to here when writing this checking code.
    
    d is a dictionary where you store the result. For each key, the result should be a tuple of size 2, on the form
    (<fraction of total points obtained>,<total points>) """
    
    d['Handled only ints']  =[assignment.only_ints(1,1)==True,2]
    d['Handled str,int']    =[assignment.only_ints('s',1)==True,4]
    d['Handled int,str']    =[assignment.only_ints(1,1)==True,3]


autocorrect.check_answers(check, REPO_NAME, TOKEN, ORGANIZATION_NAME)