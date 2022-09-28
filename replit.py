import re   
import requests

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  
def check(email):   

    if(re.search(regex,email)):   
        return True
    else:   
        return False

def signup(name,email):
    body = {
      "user": {
        "Name":name,
        "Email":email,
      }
    }
    url = "https://api.sheety.co/21d95537cb39f8e2e273584f8133a12c/copyOfFlightDeals/users"
    res = requests.post( url=url,
      json=body
    )
    print(res.text)
    print("welcome to the club!!")

email = ''
verifiedMail = ''
name = ''

name = input("enter yor name: ")
email = input("enter your email: ")
verifiedMail = input('verify your email: ')

if email != verifiedMail:
  print('email doesnt match')
else:
  if check(email):
    signup(name,email)
  else:
    print("please enter a valid email")
  