import webbrowser
from github import Github
import os
import sys
import shutil
import importlib
import numpy as np
import stat
import time

#REQUIRES THAT 
#1. GIT IS INSTALLED
#
#2. All names are in smallcaps without spaces
#
#3. An assignment has been created:
#   a) A repo has been created with name 
#       i) for organization org_name
#       ii) with name repo_name
#       iii) as a template
#   b) An assignment has been created in github classroom for the above repo
#       i) for organization org_name
#       ii) with name repo_name
#
#4. A valid token
#    go to "https://github.com/settings/tokens/new" to get a token
#
#5. A correct answer file has been created:
#     a) a python file (*.py)
#     b) in this folder
#     c) with name repo_name
#     d) with a function "def check(assiginment,d)" that
#           i) assigns results to dictionary d where keys can be any string
#           ii) results are tuples containing two values (<fraction of maximum points as result>, <maximum ponts>)
#        for example, the check function below gives 2 points if code_that_should_work gives expected_result, and zero otherwise: 
#
#def check(assignment,d):
#    expected_result=10
#    d['Managing to to the simplest thing']=(assignment.code_that_should_work('test input',1,2,3)==expected_result,2)


PATH='temp' 
CUR_DIR=os.getcwd()
 
def check_answers(correcting_function,repo_name,token,org_name):
    repo_name=repo_name.replace(' ','-')
    g=Github(token)
    org = g.get_organization(org_name)
    d={}
    tbl=[['Student ID','total points','max points','percentage','grade']]
    for i in org.get_repos('private'):
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        os.chdir(PATH)        
        a=check_member(i,org,d,repo_name,correcting_function,token)
        if not a is None:
            tbl.append(a)
        os.chdir(CUR_DIR)
    delete_folder(PATH)
    save_table(tbl, repo_name)
    
def grading(p):
    letters_art=np.array(['an A','a B','a C','a D','an E','an F'])
    letters=np.array(['A','B','C','D','E','F'])
    limits=np.array([1.01,.85,.7,.55,.45,.3,-.01])
    sel=(limits[1:]<p)*(limits[:-1]>=p)
    return letters[sel][0],letters_art[sel][0]
        
def check_member(member,org,d,repo_name_orig,correcting_function,token):
    repo_name_orig=repo_name_orig.lower()
    n=len(repo_name_orig)
    organization_name,repo_name=member.full_name.split('/')
    if not repo_name_orig+'-'==repo_name[:n+1]:
        return
    repo=org.get_repo(member.name)
    repo_url=repo.url.replace('api.github.com/repos',token+'@github.com')
    
    #Cloning:
    os.system(f"git clone {repo_url}")
    
    #Checking:
    student_name=repo_name[n+1:]
    d[student_name],tbl_row=check_answer(repo_name,correcting_function,student_name)
    os.chdir(repo_name)
    
    #Pushing:
    os.system("git add feedback.md")
    os.system('git commit -a -m "gave feedback"')
    os.system("git push -f")

    return tbl_row
    

def delete_folder(folder):
    print("Cleaning up ...")
    for root, dirs, files in os.walk(folder):  
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    for i in range(20):
        try:
            shutil.rmtree(folder)
            break
        except Exception as e:
            #print(e)
            time.sleep(1)
    print ("... done")
        

    
def check_answer(repo_name,correcting_function,student_name):
    #loading the student's answer as a modue, assuming the file name 'assginment.py'
    spec = importlib.util.spec_from_file_location("assignment", f'./{repo_name}/assignment.py')
    answ_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(answ_module)
    
    #creating a dictionary to store the results, and checking the module/answer
    d={}
    correcting_function(answ_module,d)
    
    #calculating points:
    p=0
    tp=0
    for i in d:
        result,max_points,comment=d[i]
        points=result*max_points
        p+=points
        tp+=max_points
        percent=np.round(float(p)/tp,1)
        d[i]=[result,max_points,points,comment,percent]
    d['Sum points']=p
    d['Sum max points']=tp
    d['Percentage score']=np.round(100*p/tp,1)
    d['grade']=grading(p/tp)
    dict_to_markdown(d,  f'./{repo_name}')
    tbl_row=[student_name,d['Sum points'],d['Sum max points'],d['Percentage score'],d['grade'][0]]
    print(
        f"Student {student_name}: {d['Percentage score']}%, {d['grade'][0]}"
    )    
    return d,tbl_row
    
    
def dict_to_markdown(d,fpath):
    s=(f"# You got {d['grade'][1]}.\n"
        f"### Your score: {d['Percentage score']}% ({float(d['Sum points'])}/{float(d['Sum max points'])})\n\n"
       "|Task|Maximum points|Points obtained|%|Comment|\n"
       "|-|-:|-:|-:|-:|\n")
    for i in d:
        if not (i in ['Evaluation',
                      'Percentage score',
                      'Sum points',
                      'Sum max points',
                      'grade']):
            result,max_points,points,comment,percent=d[i]
            if percent==1:
                percent=f'100.0%'
            elif percent>0:
                percent=f'{percent}%'
            else:
                percent=f'<span style="color:red">0.0 %</span>'
            s+=f"|{i}|{max_points}|{points}|{percent}|{comment}|\n"
    if d['Percentage score']==1:
        percent='100.0%'
    elif d['Percentage score']>0:
        percent=f'{d["Percentage score"]}%'
    else:
        d['Percentage score']='0.0%'    
    s+=f"|**Total**|**{d['Sum max points']}**|**{d['Sum points']}**|**{percent}**||\n"
    f=open(fpath+'/feedback.md','w')
    f.write(s)
    f.close()

def save_table(tbl,repo_name):
    path="./results"
    s=f"# Test summary for {repo_name}:\n\n"
    s+=f"|{'|'.join(tbl[0])}|\n"
    s+="|:-"+"|-:"*(len(tbl[0])-1)+'|\n'
    for i in range(1,len(tbl)):
        s+=f"{'|'.join(tbl[0])}|"
    f_name='summary '+repo_name
    if not os.path.exists(path):
        os.makedirs(path)    
    f=open(os.path.join(path,f_name+'.md'),'w')
    f.write(s)
    f.close()
    np.savetxt(os.path.join(path,f_name+'.csv'),np.array(tbl,dtype=str),fmt='%s')

def import_module(name):
    for i in [name,name.replace('-',''),name.replace('-','').lower()]:    
        try:
            return importlib.import_module(i)
        except ModuleNotFoundError:
            pass
    raise RuntimeError(f"Could not find a module in the working directory '{os.getcwd()}' that matches the repo name '{NAME_OF_ORIG_REPO}'")   
    
