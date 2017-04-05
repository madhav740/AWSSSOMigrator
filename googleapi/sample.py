
import httplib2
import os
import time
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import inspect
#SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
#SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
SCOPES = 'https://www.googleapis.com/auth/admin.directory.group' 
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Directory API Python Quickstart'
try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

def get_credentials():
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,'admin-directory_v1-python-quickstart.json')
	store = oauth2client.file.Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow,store,flags)
		else:
			credentials = tools.run(flow,store)
		print "Stroring crdentials to " +credential_path
	return credentials

def main():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('admin','directory_v1',http = http)
	#results = service.users().list(customer='my_customer',us).execute()
	#print results
	#results = service.users().list(customer='my_customer',orderBy='email').execute()
	#results = service.users().get(userKey="madhav@boomerangcommerce.com").execute()
	#results = service.verificationCodes().list(userKey="madhav@boomerangcommerce.com").execute()
        group_to_deletable_email_map = dict() 



#        with open("suspendedusers.csv") as f:
#            for line in f:
#                pair = line.rstrip('\n').rstrip('\r').split(",")
#                group_to_deletable_email_map[pair[1]] = pair[0]
#
#        for group in group_to_deletable_email_map:
#            time.sleep(2)
#            try:
#                service.members().delete(groupKey=group.rstrip("\n"),memberKey=group_to_deletable_email_map[group]).execute()
#                print group+","+group_to_deletable_email_map[group]+",DELETED"
#            except Exception,e:
#                print group+","+group_to_deletable_email_map[group]+",FAILED"
#
	
	#group_email_id = get_emaiid_from_group(service,"infra@boomerangcommerce.com")
	#print group_email_id
	#signed_status = read_signed_status()
	#get_user_unenrolled_for_two_step(signed_status,group_email_id)
	#match_dev_email_list(group_email_id,"india-dev-list.csv")

def get_all_users(service):
	token = None
	users = list()
	while(True):
		results = service.users().list(customer='my_customer',orderBy='email',pageToken = token).execute()
		users = users + results.get('users',[])
		if 'nextPageToken' in results.keys() and results['nextPageToken'] != '':
			token = results['nextPageToken']
			print token
		else:
			print "no more next token"
			break
	print len(users)
	return users

def get_user_unenrolled_for_two_step(signed_status,group_email_id):
	print "Total email in boomerang domain" +str(len(signed_status))
	print "Total email in india dev" +str(len(group_email_id))
	for items in group_email_id:
		if signed_status[items] == "Disabled":
			print items

def get_emaiid_from_group(service,group_name):
	group_email_list = list()
	results = service.members().list(groupKey=group_name).execute()
	members = results['members']
	for items in members:
		group_email_list.append(items['email'])
	return group_email_list
 	

def get_filtered_email_from_group(service,group_name):
	group_email_list = list()
	results = service.members().list(groupKey=group_name).execute()
	members = results['members']
	for items in members:
		group_email_list.append(items['email'])
	return group_email_list



def match_dev_email_list(group_email_id,file_name):
	emails = list()
	with open(file_name) as file_object:
		for line in file_object:
			emails.append(line.rstrip())
	print emails.sort()
	print "\n"
	print group_email_id.sort()
	non_matched_email = list(set(group_email_id)-set(emails))
	for items in non_matched_email:
		print items
	

def create_user_aws_sso(users):
	if not users:
		print "no users found in the domain"
	else:
		print "users:"
		for user in users:
			print user['primaryEmail']
			#Code to create aws sso for an user
			print user['name']
			print user['name']['fullName']
			json_body = '{"customSchemas":{"SSO": {"role": [{value: "#comma separated iam role and aws saml google",customType: "Developer"}]}}}'
			response = user.patch(userkey=user['primaryEmail'],body=json_body)
			print response


def read_signed_status():
    file_name = "final_result.csv"
    user_status = dict()
    with open(file_name) as f:
        lines = f.readlines()
    for items in lines:
        items = items.rstrip()
        pair = items.split(",")
        user_status[pair[0]] = pair[1]
    #print user_status
    return user_status

if __name__ == '__main__':
	main()
