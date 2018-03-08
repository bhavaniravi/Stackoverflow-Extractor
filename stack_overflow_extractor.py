"""
Stack_overflow_Extractor : Extracts user details based on the users stack-overflow link
"""
import ssl
import json
import urllib
from github import Github
from bs4 import BeautifulSoup
import validators
import requests

def git_repos(link):
    """
    :param links: Links extracted from the url using Stackoverflow()
    :return: Github repositories of the specific user
    :raise : ConnectionRefusedError, requests.Timeout, IndexError
    """
    repos = []
    github = Github()
    return [{"name":repo.name, "url":link, "description":repo.description} \
                for repo in github.get_user(link[19:len(link)]).get_repos(type="owner")[:10] \
                if "github" in link
            ]

def stackoverflow(url):
    """
    :param url: Takes Stack-overflow link as a string
    :return: Username, description, tags and links form the url
    :raise : ConnectionRefusedError, requests.Timeout
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "lxml")

    # Fetching the User-Name and Description
    user = soup.title.string.split("-")[0][5:]
    description = " ".join(i.get_text() for i in soup.find("div", {"class" : "bio"}).find_all("p"))
    #tags =  [i.string for i in soup.find("body").find("div", id="top-tags").find_all("a", limit=6)]
    links = [i["href"] for i in soup.find("body").find("div", "user-links").find_all("a")]
    #repos = git_repos(links)
    return {"user":user, "description":description, "links":links}
