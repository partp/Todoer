import sys
import requests
from urllib.parse import urlencode
from getpass import getpass
from datetime import datetime

BASE_URL = "https://api.todoist.com/API/"

class Todoer:
  api_token = None
  
  def __init__(self):
    if self.api_token is None:
      logged_in = self.check_login_file()
    if not logged_in:
      self.calls("login")
      
  def check_login_file(self):
    try:
      login_data = open("login_data", 'r')
      self.api_token = login_data.readline()
      login_data.close()
      return True
    except:
      print("**Error** Couldn't read login_data file!!")
    return False
  
  def store_login_data(self):
    try:
      login_data = open('login_data', 'w')
      login_data.write(self.api_token)
      login_data.close()
    except:
      print("**Error** Couldn't write to login_data file!!")
  
  def params_dict(self, api_call):
    if api_call == "login":
      email = input("Enter your Todoist registered email id\t:")
      password = getpass()
      params_dict = {
	'email': email,
	'password': password
      }
    elif api_call == "getProjects":
      params_dict = {
	'token': self.api_token
      }
    return params_dict
    
  
  def login(self, j_data):
    if j_data:
      self.api_token = j_data["api_token"]
      self.store_login_data()
    else:
      print("**Failed** Check your email or password\n")
      sys.exit(0)

  def getProjects(self, j_data):
    if j_data:
      sorted_list = sorted(j_data, key=lambda k: k["item_order"]) 
      elegant_projects(sorted_list)
    else:
      print("It's time to buckle up and create new projects :)")
      return
    
  def calls(self, api_call):
    if api_call:
      url = BASE_URL + api_call
      params = urlencode(self.params_dict(api_call))
      
      try:
        resp_data = requests.get(url, params = params)
        j_data = resp_data.json()
        methodToCall = getattr(Todoer, api_call)
        methodToCall(self, j_data)
        return True
      except Exception:
        print("\n**Failed**\n")
        return False

def elegant_projects(j_data):
  for project in j_data:
    if not (project["is_deleted"] or project["is_archived"]):
      for i in range(project["indent"] - 1):
        print("\t", end="")
      if project["collapsed"]:
        print("--------------------------------------------------")
      else:
        if "inbox_project" in project and project["inbox_project"]:
          print("✉ ", end="")
        print("{0} ({1})\t{2:>50}".format(project["name"], project["cache_count"], str(datetime.fromtimestamp(int(float(project["last_updated"]))))))

if __name__ == "__main__":
  new_todoer = Todoer()
  
  new_todoer.calls("getProjects")
  