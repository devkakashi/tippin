#!/usr/bin/python3

# 
import datetime ; import random
import json ; import glob
import sys ; import re
import subprocess
import requests
#

def console(CMD):

    try:
        return [True, subprocess.check_output(CMD).decode().split('\n')]
    except:
        return [False]

def setdatabase(username=None, password=None, userid=None, txinput=[], txoutput=[]):
    
    MakeDict = {
        'database' : {'username' : username, 'password' : password, 'userid' : userid}, 
        'transaction' : {'input' : txinput, 'output' : txoutput}
    }

    local = '/home/{0}/a72d85ec25eb5286191e7346449deb1a.db'.format(console(['whoami'])[1][0])

    file = open(local,'w')
    file.write(str(MakeDict))
    file.close()

    return True

def metrics():

    sourcecode = requests.get('https://twitter.com/i/js_inst?c_name=ui_metrics').text.replace(';','\n')
    
    for text in sourcecode.split():

        if "{'rf':{" in text:
            sourcecode = text
            break

    Hash, Last = (re.findall('[a-z 0-9]{64}', sourcecode), None)

    Metricdict = {'rf' : {}, 's'  : ''}

    for L in range(0, len(Hash)):

        if Hash[L] != Last:

            Metricdict['rf'].update(
                {Hash[L] : random.randint(-30, 250)
            })

            Last = Hash[L]
    
    for L in sourcecode.split():

        if "'s':" in L:

            DT = L.replace(':','\n').replace('}','').split()

            Metricdict['s'] = DT[len(DT) - 1].replace("'","")

            return Metricdict

def twitter():

    login = session.get('https://twitter.com/login', headers={'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'})

    authtoken = re.findall('value="[\w]+', login.text)[0].replace('value="','')

    sessions = session.post('https://twitter.com/sessions', cookies=login.cookies, data={
        'session[username_or_email]' : username, 'session[password]'  : password,
        'authenticity_token' : authtoken, 'ui_metrics' : metrics(),
        'scribe_log' : '', 'redirect_after_login' : '',
        'authenticity_token' : authtoken, 'remember_me' : 1
    }, headers={
        'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36', 
        'referer' : 'https://twitter.com/login', 'origin': 'https://twitter.com'
    }, allow_redirects=True)

    if sessions.url == 'https://twitter.com/':
        return [True, login, sessions]
    else:
        return [False, login, sessions]

def oauthapp(twittercookies):

    oauthaction = session.get('https://tippin.me/twOauthAction.php', headers={
      'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36', 
      'referer' : 'https://tippin.me/',
      'origin'  : 'https://tippin.me/'
    }, allow_redirects=True)

    authenticate = session.get(oauthaction.url, headers={
      'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36', 
      'origin'  : 'https://api.twitter.com'  
    }, cookies=twittercookies, allow_redirects=True)

    callbackurl, loopcount = ('', 0)

    for text in authenticate.text.split():

        if 'href=' in text and loopcount == 8:

                callbackurl = text.replace('href="','').replace('">clique', '').replace(';','&') ; break

        elif 'href=' in text:

                loopcount += 1

    callback = session.get(callbackurl, headers={'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}, data={
        'oauth_token' : re.findall('oauth_token=[\w]+', callbackurl)[0].replace('oauth_token=','')
      }, cookies=authenticate.cookies, allow_redirects=True)

    dashboard = session.get('https://tippin.me/dashboard.php', headers={'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}, cookies=authenticate.cookies, allow_redirects=True)

    if re.findall('@'+username, dashboard.text):

        return [True, session, dashboard, authenticate]
    else:
        return [False, session, dashboard, authenticate]

def cashout(session, dashboard, authenticate, payreq):

    csrf = re.findall("csrf: '[\w]+',", dashboard.text)[0]
    csrf = csrf.replace("csrf: '", "")
    csrf = csrf.replace("',","")

    while True:
        try:

            return json.loads(
                session.post('https://tippin.me/lndreq/cashout.php', data={'payreq' : payreq, 'csrf'   : csrf}, headers={
                    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
                }, cookies=authenticate.cookies
            ).text)

        except:
            continue

def newinvoice(amount=0):

    while True:
        try:
            return json.loads(requests.post('https://tippin.me/lndreq/newinvoice.php', data={
                'userid' : userid,
                'username' : username, 
                'userplan' : '',
                'istaco' : 0, 
                'customAmnt' : 0, 
                'customMemo' : '', 
                'customSat' : amount
            }).text)
        except:
            continue

def lookupinvoice(rhash):

    while True:
        try:
            return json.loads(requests.post('https://tippin.me/lndreq/lookupinvoice.php', data={
                'rhash' : rhash,
                'node_id' : 1
            }).text)
        except:
            continue

whoami = console(['whoami'])[1][0]
local  = '/home/{}/a72d85ec25eb5286191e7346449deb1a.db'.format(whoami)

if whoami == 'root':

    print('[!] Please do not run this software in root mode for security.')
    exit()

if len(glob.glob(local)) == 0:

    setdatabase()

try:
    database = eval(open(glob.glob(local)[0],'r').read())
except:
    print('[!] Directory /home does not exist on your system, you can create a folder named /home in the directory /')
    exit()

session  = requests.session()

username = database['database']['username']
password = database['database']['password']
userid   = database['database']['userid']

transaction = database['transaction']

#

for parameter in sys.argv:

    #
    if parameter == '-u':

        if not '-p' in sys.argv:
   
            print('[!] You did not add it to your password')
            exit()

        while True:
            try:

                tippin = requests.get('https://tippin.me/@' + sys.argv[2]).text

                if re.findall("This user doesn't exist", tippin):
                    print("[!] This user doesn't exist")
                    break

                userid = re.findall('var_userid = [\d]+', tippin)[0].split()[2]

                setdatabase(username=sys.argv[2], password=sys.argv[4], userid=userid, txinput=transaction['input'], txoutput=transaction['output'])

                print('\n[!] Your credentials have been successfully added.\n')
                break

            except:
                continue
        exit()
    #

    elif parameter == '--newinvoice':

        try:
            amount = int(sys.argv[2])
        except:
            amount = 0

        invoicedata = newinvoice(amount=amount)

        transaction['input'].append({
            invoicedata['message'] : {'rhash' : invoicedata['rhash'], 'amount' : amount, 'status' : None}
        })

        setdatabase(username=username, password=password, userid=userid, txinput=transaction['input'], txoutput=transaction['output'])

        print('\n[Donate Me](https://tippin.me/@devkakashi)\n')
        print('${} SATS -> {} \n'.format(amount, invoicedata['message']))

        exit()

    elif parameter == '--cashout':

        Twitter, OauthApp = (None, None)

        if len(sys.argv) != 3:
            print('\n[!] You did not enter the invoice to be paid\n')
            exit()
            
        elif sys.argv[2][:2] != 'ln':
            print('\n[!] Invalid invoice.\n')
            exit()

        while True:
            try:
                Twitter = twitter()

                if Twitter[0] == True:

                    Twitter = Twitter
                    break

                else:
                    Twitter = None
                    print('\n[!] Your login credentials are incorrect please enter again.\n')
                    print('\n./tippin.py -u username -p password\n')
                    break
            except:
                continue

        if Twitter == None:
            exit()
        while True:
            try:
                OauthApp = oauthapp(Twitter[2].cookies)

                if OauthApp[0] == True:

                    OauthApp = OauthApp
                    break

                else:
                    OauthApp = None
                    print("[!] To make tippin's oauth not working try again later or visit https://tippin.me/login to see if it's ok")
                    break
            except:
                continue

        if OauthApp == None:
            exit()

        paynow = cashout(OauthApp[1], OauthApp[2], OauthApp[3], sys.argv[2])
  
        if paynow['error'] == True:

            print('\n[!] {} \n'.format(paynow['message']))
            exit()

        transaction['output'].append({sys.argv[2] : {'amount' : paynow['amount'], 'status' : True}})

        setdatabase(username=username, password=password, userid=userid, txinput=transaction['input'], txoutput=transaction['output'])

        print('\n[Donate Me](https://tippin.me/@devkakashi)\n')
        print('\n[!] {} \n'.format(paynow['message']))

        exit()
    #

    elif parameter == '--status':
        
        if len(sys.argv) != 3:

            print('\n[!] You did not specify your invoice\n')
            exit()

        tx, count = (None, 0)

        for data in transaction['input']:

            if sys.argv[2] in data.keys():

                tx = data ; count += 1
                break

        if tx == None:

            print('\n[!] Unable to deal with transactions with this invoice.\n')
            exit()
        
        check = lookupinvoice(tx[sys.argv[2]]['rhash'])['settled'] == True
    
        for index in range(0, len(transaction['input'])):

            if sys.argv[2] in transaction['input'][index].keys():
                
                data = transaction['input'][index][sys.argv[2]]

                transaction['input'][index][sys.argv[2]] = {'rhash' : data['rhash'], 'amount' : data['amount'], 'status' : check}

        setdatabase(username=username, password=password, userid=userid, txinput=transaction['input'], txoutput=transaction['output'])

        print('\n[Donate Me](https://tippin.me/@devkakashi)\n')
        print({True : 'Your invoice has been paid :)\n', False : 'Your bill has not been paid :(\n'}[check])
    #

if username == None or password == None:

    print('[!] Please enter your twitter credentials to access your tippin account')
    print(' ./tippin -u username -p password')

    exit()

elif len(sys.argv) == 1:

    print('\n[Donate Me](https://tippin.me/@devkakashi)')
    print()
    print(' ./tippin.py -u username -p password | Add twitter credentials to tippin.')
    print(' ./tippin.py --newinvoice amount     | Generate a new payment invoice.')
    print(' ./tippin.py --cashout invoice       | Pay an invoice.')
    print(' ./tippin.py --status invoice        | check the status of an invoice.')
    print()
    exit()
