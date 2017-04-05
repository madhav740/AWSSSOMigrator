import sys
import os
import getpass
import time
from selenium import webdriver

def read_user_info(driver,url):
	url += "&flyout=security"
	driver.get(url)
	time.sleep(15)
#	show_more_query = "document.getElementsByClassName('FJDE1KC-wf-a')[0].click();" 
#	driver.execute_script(show_more_query)
#	time.sleep(3)
#	security_expand_query ="document.getElementsByClassName('FJDE1KC-yc-r')[4].childNodes[0].click();" 
#	driver.execute_script(security_expand_query)
#	time.sleep(3)
	#driver.find_elements_by_class_name('strong-auth-enabled').find_element_by_tag_name('span')
	#status_query = "document.getElementsByClassName('strong-auth-enabled')[0].textContent;"

	#driver.execute_script(statusquery)
	#time.sleep(3)
	status = driver.find_element_by_class_name("strong-auth-enabled").text
	if status == None or status == "":
		status = driver.find_element_by_class_name("strong-auth-disabled").text
	#email = driver.find_elements_by_class_name('FJDE1KC-E-E')[0].text
	email = driver.find_elements_by_class_name('gwt-Label')[5].text
	result = email+ ","+status
	print result
	return result

def read_email_id(file_name):
	email_href_list = list()
	with open(file_name) as file_handler:
		lines = file_handler.readlines()
	for items in lines:
		email_url= items.rstrip()
		email_href_list.append(email_url)
	return email_href_list

def read_fileterd_email(file_name,email_map_file):
	email_list = list()
	final_list = list()
	with open(file_name) as file_object:
		lines = file_object.readlines()
	for items in lines:
		email_list.append(items.rstrip())
	email_to_url_map = dict()
	with open(email_map_file) as file_object:
		lines = file_object.readlines()
	for items in lines:
		pair = items.rstrip().split(",")
		email_to_url_map[pair[0]] = pair[1]
	print email_to_url_map
	for items in email_list:
		final_list.append(email_to_url_map[items])
	return final_list


def start_authentication():
	driver = webdriver.Chrome()
	all_users_url = "https://admin.google.com/boomerangcommerce.com/AdminHome?fral=1#UserList:org=3eu4us2351ny2h" 
	driver.get(all_users_url)
	username = "" #"emial id of user"
	driver.find_element_by_id('Email').clear();
	driver.find_element_by_id('Email').send_keys(username);
	driver.find_element_by_id('next').click();
	time.sleep(5)
	driver.find_element_by_id('Passwd').clear();
	password = getpass.getpass('Password:')
	driver.find_element_by_id('Passwd').send_keys(password);
	driver.find_element_by_id('signIn').click();
	driver.implicitly_wait(5)
	otp_code = getpass.getpass('OTP Code:')
	driver.find_element_by_id('totpPin').send_keys(otp_code);
	driver.find_element_by_id('submit').click();
	time.sleep(10)
	return driver

if __name__ == "__main__":
	driver = start_authentication()
	file_name = "email_id.csv"
	#email_href_list = read_email_id(file_name)
	email_href_list = read_fileterd_email("us-fte.csv","email_to_userid.csv")
	result_list = list()
	for items in email_href_list:
		result_list.append(read_user_info(driver,items))
	fw = open("status_list.csv",'w')
	for items in result_list:
		fw.write(items)
	fw.close()
