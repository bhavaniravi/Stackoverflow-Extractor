import string
import ssl
import re
import sys
import json
try:
    import requests
except:
    print("Package missing, need to install requests")
try:
    from github import Github
except:
    print("Package missing, need to install github API")
try:
    import urllib
except:
    print("Package missing, need to install urllib")
try:
    from bs4 import BeautifulSoup
except:
    print("Package missing, need to install BeautifulSoup")


def stackoverflow(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    html=urllib.request.urlopen(url,context=ctx).read()
    soup=BeautifulSoup(html,"lxml")

    ''' Fetching the User-Name and Description'''

    title=soup.title.string
    description=soup.p.string
    user=""
    count=0
    for i in range(len(title)):
        if title[i]==" " and count!=1:
            count+=1
            for j in range(i+1,len(title)):
                if title[j]!="-":
                    user=user+title[j]
                else:
                    break
        else:
           if count==1:
               break
    #print(user)
    #print(description)

    ''' Extracting TOP TAGS and other inter-linked LINKS'''
    
    tags=soup.find("body").find("div",id="top-tags").find_all("a",limit=6)
    links=soup.find("body").find("div","user-links").find_all("a")

    tags=[i.string for i in tags]
    links=[i["href"] for i in links]

    # Displaying the TOP TAGS
    
    #for i in range(len(tags)):
    #    print(tags[i])

    return user,description,tags,links


def git_repos(links):
    
    ''' Goes through the users github profile to get the Repo Names'''
    
    for i in links:
        if "github" in i:
            gh = Github()
            name=i[19:len(i)]
            repos=[repo.name for repo in gh.get_user(name).get_repos()]
    #        for i in repos:
    #            print(i)

    return repos


def convert_to_json(user,description,tags,links,repos):
    
    ''' Writing data to a json file'''

    with open("result.json","w") as f:
        json.dump(user,f)
        f.write("\n\n")
        json.dump(description,f)
        f.write("\n\n\n")
        f.write("TOP TAGS \n\n")
        for i in range(len(tags)):
            json.dump(tags[i],f)
            f.write("\n")
        f.write("\n\n")
        f.write("Github REPOS \n\n")
        for i in repos:
            json.dump(i,f)
            f.write("\n")

            
def main():

    ''' Getting the URL and Extracting the content''' 

    url=input()
    user,description,tags,links=stackoverflow(url)
    repos=git_repos(links)
    convert_to_json(user,description,tags,links,repos)
            

if __name__ == "__main__":
    main()
