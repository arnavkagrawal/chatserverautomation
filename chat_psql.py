#!/usr/bin/python
# Needs to be run in the web2py environment
# sudo python web2py.py -S eden -M -R chat_psql.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os

#definations
driver = webdriver.Firefox()
css_select = driver.find_element_by_css_selector 
wait=time.sleep
wait_t=30

#functions
def wait_for_elements(css_locator):
    element = WebDriverWait(driver, wait_t).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_locator))
            )
    return

def add_property(property_name, property_value):
    print "Adding Property: ",property_name
    wait_for_elements(".jive-table > table > tbody> tr:nth-of-type(1) > td:nth-of-type(2) > input")
    p_n_field=css_select(".jive-table > table > tbody> tr:nth-of-type(1) > td:nth-of-type(2) > input")
    p_v_field=css_select(".jive-table > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > textarea")
    enc_type=css_select(".jive-table > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input:nth-of-type(2)")
    enc_type.click()
    p_n_field.send_keys(property_name)
    p_v_field.send_keys(property_value)
    save_prop=css_select(".jive-table > table > tfoot > tr:nth-of-type(1) > td:nth-of-type(1) > input:nth-of-type(1)")
    save_prop.click()
    return

def edit_property(property_name,value):
    print "Editing Property: ",property_name
    wait_for_elements(".jive-table > table > tfoot > tr:nth-of-type(1) > td:nth-of-type(1) > input:nth-of-type(1)")
    search_string="//*[contains(text(),'"+ property_name +"')]"
    elem = driver.find_elements_by_xpath(search_string)
    elem[0].find_elements_by_xpath("ancestor::tr/td[3]/a")[0].click() 
    enc_type=css_select(".jive-table > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input:nth-of-type(2)")
    enc_type.click()
    property_value=css_select(".jive-table > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > textarea")
    property_value.clear()
    property_value.send_keys(value)
    submit_but=css_select(".jive-table > table > tfoot > tr:nth-of-type(1) > td:nth-of-type(1) > input:nth-of-type(1)")
    submit_but.click()
    return


def add_plugin(plugin_name):
    print "Adding Plugin: ",plugin_name
    search_string="//*[contains(text(),'"+ plugin_name +"')]"
    elem = driver.find_elements_by_xpath(search_string)
    elem[0].find_elements_by_xpath("ancestor::tr/td[8]/a")[0].click()
    wait(wait_t)
    return

#roster sharing by group creation
def create_group(group_name):
    print "Creating Group: ",group_name
    driver.get("http://127.0.0.1:9090/group-create.jsp")
    wait_for_elements("#gname")
    g_name=css_select("#gname")
    g_name.send_keys(group_name)
    save_group=css_select(".jive-contentBox > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input:nth-of-type(1) ")
    save_group.click()
    #roster sharing enable
    wait_for_elements(".jive-contentBox > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > input")
    css_select(".jive-contentBox > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > input").click()
    wait_for_elements("#jive-roster > input")
    contact_list=css_select("#jive-roster > input")
    contact_list.send_keys(group_name)
    css_select("#cb101").click()
    wait_for_elements(".jive-contentBox > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input")
    css_select(".jive-contentBox > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input").click()
    return

#default adding of users to group
def registeration_property(group_name):
    print "Adding user to group",group_name
    driver.get("http://127.0.0.1:9090/plugins/registration/registration-props-form.jsp")
    wait_for_elements("#jive-main-content > form:nth-of-type(3) > .jive-contentBox > table > tbody > tr:nth-of-type(1) > td:nth-of-type(1) > input")
    default_group=css_select("#jive-main-content > form:nth-of-type(3) > .jive-contentBox > table > tbody > tr:nth-of-type(1) > td:nth-of-type(1) > input")
    default_group.send_keys(group_name) 
    css_select("#jive-main-content > form:nth-of-type(3) >.jive-contentBox > input ").click()
    wait_for_elements("#jive-main-content > form:nth-of-type(1) >.jive-contentBox > table > tbody > tr:nth-of-type(4) > td:nth-of-type(1) > input")
    css_select("#jive-main-content > form:nth-of-type(1) >.jive-contentBox > table > tbody > tr:nth-of-type(4) > td:nth-of-type(1) > input").click()
    wait_for_elements("#jive-main-content > form:nth-of-type(1) >.jive-contentBox > input")
    css_select("#jive-main-content > form:nth-of-type(1) >.jive-contentBox > input").click()
    return


def add_admin_to_group(group_name,admin_username):
    print "Adding admin to group ",group_name
    driver.get("http://127.0.0.1:9090/group-edit.jsp?group="+group_name)
    wait_for_elements(".jive-contentBox > form > table > tbody > tr > td:nth-of-type(2) > input:nth-of-type(1)")
    add_user=css_select(".jive-contentBox > form > table > tbody > tr > td:nth-of-type(2) > input:nth-of-type(1)")
    add_user.send_keys(admin_username)
    css_select(".jive-contentBox > form > table > tbody > tr > td:nth-of-type(2) > input:nth-of-type(1)").click()
    return

def allow_status_messages():
    print "Allowing Status Messages"
    driver.get("http://127.0.0.1:9090/plugins/presence/presence-service.jsp")
    wait_for_elements("#rb01")
    css_select("#rb01").click()
    wait_for_elements("#jive-main-content > form > input")
    css_select("#jive-main-content > form > input").click()
    return

def login_with_initials(ini_username,ini_password):
    print "Loggin in"
    driver.get("http://127.0.0.1:9090/login.jsp")
    wait_for_elements("input[type='submit']")
    username_field = driver.find_element_by_name("username")
    pass_field = driver.find_element_by_name("password")
    username_field.send_keys(ini_username)
    pass_field.send_keys(ini_password)
    login_button = css_select("input[type='submit']")
    login_button.click()
    server_name=css_select(".info-table > tbody > tr:nth-of-type(4) > td:nth-of-type(2)").get_attribute('innerHTML')
    #the server name
    server_name=server_name.strip()
    #wait to load page
    wait_for_elements("#jive-body")
    return server_name

#configure settings here
#the password for intial user 
ini_password="admin"
sahana_dbname="sahana"
openfire_db="open"
#A default group for everyone to be in
group_name="everyone"
#psql settings
psql_username="arnav"
psql_password="knowing42"
#the new user created by w2p for chat admin
admin_username="chatadmin"
admin_password="eden"
admin_name="Chat Admin"
admin_email="chatadmin@example.com"
#depends on internet connection higher for slow connections
wait_plugin=30  
#depends upon sql speed higher for lower speed
wait_psql=10
#depends upon server restart speed higher for lower speed
wait_restart=30
#configuration ends here

#The default username for intial login. Should not be changed
ini_username="admin"

#create chat admin user in sahana db
db.auth_user.insert(email=admin_email, username=admin_username, password=admin_password, first_name=admin_name)
db.commit()

#Server Setup
print "Server setup Starting"
driver.get("http://127.0.0.1:9090/")
wait_for_elements("#jive-setup-save")
css_select("#jive-setup-save").click()
wait_for_elements("#jive-setup-save")
css_select("#jive-setup-save").click()
wait_for_elements("#rb02")
css_select("#rb02").click()
wait_for_elements("#jive-setup-save")
css_select("#jive-setup-save").click()
wait_for_elements(".jive-contentBox > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) >  select > option[value='0']")
css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) >  select > option[value='0']").click()
wait_for_elements("#jive-setup-save")
css_select("#jive-setup-save").click()
wait_for_elements(".jive-contentBox > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > input")
JDBC_Driver_Class=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > input")
JDBC_Driver_Class.clear()
JDBC_Driver_Class.send_keys("com.mysql.jdbc.Driver")
wait_for_elements(".jive-contentBox > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input")
db_url=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input")
db_url.clear()
db_url.send_keys("jdbc:postgresql://127.0.0.1:5432/"+openfire_db)
wait_for_elements(".jive-contentBox > form > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > input")
sq_user=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > input")
sq_user.clear()
sq_user.send_keys(psql_username)
wait_for_elements(".jive-contentBox > form > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2) > input")
sq_pass=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2) > input")
sq_pass.clear()
sq_pass.send_keys(psql_password)
wait_for_elements("#jive-setup-save")
css_select("#jive-setup-save").click()
wait_for_elements("#jive-setup-save")
css_select("#jive-setup-save").click()
wait_for_elements(".jive-contentBox > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > input")
adm_email=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > input")
adm_email.clear()
adm_email.send_keys(admin_email)
adm_pass=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > input")
adm_pass.clear()
adm_pass.send_keys(ini_password)
wait_for_elements(".jive-contentBox > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input")
adm_conpass=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input")
adm_conpass.clear()
adm_conpass.send_keys(ini_password)
wait_for_elements("#jive-setup-save")
css_select("#jive-setup-save").click()

wait(wait_psql)
server_name = login_with_initials(ini_username,ini_password)

#enable bosh
print "Enabling Bosh"
driver.get("http://127.0.0.1:9090/http-bind.jsp")
wait_for_elements("#rb03")
css_select("#rb03").click()
wait_for_elements("#settingsUpdate")
css_select("#settingsUpdate").click()

#install plugins
print "Installing Plugins"
driver.get("http://127.0.0.1:9090/available-plugins.jsp")
#download plugin list
try:
    css_select("#reloaderID > a").click()
    wait(10)
except:
    pass
plugin_list=["Broadcast","Client Control","Presence Service","Registration","User Creation","User Import Export"]
for i in plugin_list:
    add_plugin(str(i))

os.system("sudo /opt/openfire/bin/openfire restart")
wait(wait_restart)


#relogin
server_name = login_with_initials(ini_username,ini_password)


#group creation
create_group(group_name)

registeration_property(group_name)
allow_status_messages()
#db integration part
driver.get("http://127.0.0.1:9090/server-properties.jsp")
add_property("jdbcProvider.driver","org.postgresql.Driver")

add_property("jdbcProvider.connectionString","jdbc:postgresql://localhost:5432/"+sahana_dbname+"?user="+psql_username+"&password="+psql_password)

add_property("jdbcAuthProvider.passwordSQL","select password from auth_user where username=?")
add_property("jdbcAuthProvider.passwordType","plain")
add_property("jdbcUserProvider.loadUserSQL","select first_name,email from auth_user where username=?")
add_property("jdbcUserProvider.userCountSQL","select count(*) from auth_user")
add_property("jdbcUserProvider.allUsersSQL","select username from auth_user")
add_property("jdbcUserProvider.searchSQL","select username from auth_user where")
add_property("jdbcUserProvider.usernameField","username")
add_property("jdbcUserProvider.emailField","email")
add_property("jdbcUserProvider.nameField","first_name")
add_property("admin.authorizedJIDs",str(admin_username+"@"+server_name))

#edit already present property
edit_property("provider.auth.className","org.jivesoftware.openfire.auth.JDBCAuthProvider")
edit_property("provider.user.className","org.jivesoftware.openfire.user.JDBCUserProvider")
os.system("sudo /opt/openfire/bin/openfire restart")
wait(30)
server_name = login_with_initials(admin_username,admin_password)
add_admin_to_group(group_name,admin_username)
os.system("sudo /opt/openfire/bin/openfire restart")
driver.close()
