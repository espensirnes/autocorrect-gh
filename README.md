# autocorrect_gh

REQUIRES THAT 
1. GIT IS INSTALLED

2. All names are in smallcaps without spaces

3. An assignment has been created:
   a) A repo has been created with name 
       i) for organization org_name
       ii) with name repo_name
       iii) as a template
   b) An assignment has been created in github classroom for the above repo
       i) for organization org_name
       ii) with name repo_name

4. A valid token
    go to "https://github.com/settings/tokens/new" to get a token

5. A correct answer file has been created:
     a) a python file (*.py)
     b) in this folder
     c) with name repo_name
     d) with a function "def check(assiginment,d)" that
           i) assigns results to dictionary d where keys can be any string
           ii) results are tuples containing two values (<fraction of maximum points as result>, <maximum ponts>)
        for example, the check function below gives 2 points if code_that_should_work gives expected_result, and zero otherwise: 

~~~~
def check(assignment,d):
    expected_result=10
    d['Managing to to the simplest thing']=(assignment.code_that_should_work('test input',1,2,3)==expected_result,2)
~~~~
