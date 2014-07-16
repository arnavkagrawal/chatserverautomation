#!/usr/bin/python
# Needs to be run in the web2py environment
# sudo python web2py.py -S eden -M -R chat_server.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

#definations
driver = webdriver.Firefox()
css_select = driver.find_element_by_css_selector 
wait=time.sleep
wait_t=1

#functions
def add_property(property_name, property_value):
    p_n_field=css_select(".jive-table > table > tbody> tr:nth-of-type(1) > td:nth-of-type(2) > input")
    p_v_field=css_select(".jive-table > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > textarea")
    enc_type=css_select(".jive-table > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input:nth-of-type(2)")
    enc_type.click()
    p_n_field.send_keys(property_name)
    p_v_field.send_keys(property_value)
    save_prop=css_select(".jive-table > table > tfoot > tr:nth-of-type(1) > td:nth-of-type(1) > input:nth-of-type(1)")
    save_prop.click()
    wait(wait_t)
    return

def edit_property(property_name,value):
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
    wait(wait_t)
    return


def add_plugin(plugin_name):
    search_string="//*[contains(text(),'"+ plugin_name +"')]"
    elem = driver.find_elements_by_xpath(search_string)
    elem[0].find_elements_by_xpath("ancestor::tr/td[8]/a")[0].click()
    wait(20)
    return

#roster sharing by group creation
def create_group(group_name):
    driver.get("http://127.0.0.1:9090/group-create.jsp")
    wait(wait_t)
    g_name=css_select("#gname")
    g_name.send_keys(group_name)
    save_group=css_select(".jive-contentBox > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input:nth-of-type(1) ")
    save_group.click()
    wait(wait_t)
    #roster sharing enable
    css_select(".jive-contentBox > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > input").click()
    wait(wait_t)
    contact_list=css_select("#jive-roster > input")
    contact_list.send_keys(group_name)
    css_select("#cb101").click()
    wait(wait_t)
    css_select(".jive-contentBox > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input").click()
    wait(wait_t)
    return

#default adding of users to group
def registeration_property(group_name):
    driver.get("http://127.0.0.1:9090/plugins/registration/registration-props-form.jsp")
    default_group=css_select("#jive-main-content > form:nth-of-type(3) > .jive-contentBox > table > tbody > tr:nth-of-type(1) > td:nth-of-type(1) > input")
    default_group.send_keys(group_name) 
    css_select("#jive-main-content > form:nth-of-type(3) >.jive-contentBox > input ").click()
    wait(wait_t)
    css_select("#jive-main-content > form:nth-of-type(1) >.jive-contentBox > table > tbody > tr:nth-of-type(4) > td:nth-of-type(1) > input").click()
    wait(wait_t)
    css_select("#jive-main-content > form:nth-of-type(1) >.jive-contentBox > input").click()
    wait(wait_t)
    return


def add_admin_to_group(group_name,admin_username):
    driver.get("http://127.0.0.1:9090/group-edit.jsp?group="+group_name)
    add_user=css_select(".jive-contentBox > form > table > tbody > tr > td:nth-of-type(2) > input:nth-of-type(1)")
    add_user.send_keys(admin_username)
    css_select(".jive-contentBox > form > table > tbody > tr > td:nth-of-type(2) > input:nth-of-type(1)").click()
    wait(wait_t)
    return

def allow_status_messages():
    driver.get("http://127.0.0.1:9090/plugins/presence/presence-service.jsp")
    css_select("#rb01").click()
    wait(wait_t)
    css_select("#jive-main-content > form > input").click()
    wait(wait_t)
    return

def login_with_initials(ini_username,ini_password):
    driver.get("http://127.0.0.1:9090/login.jsp")
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
    wait(wait_t)
    return server_name

#configure settings here
#the password for intial user 
ini_password="admin"
sahana_dbname="sahana"
openfire_db="open"
#A default group for everyone to be in
group_name="everyone"
#mysql settings
sql_username="root"
sql_password="knowing42"
#the new user created by w2p for chat admin
admin_username="chatadmin"
admin_password="eden"
admin_name="Chat Admin"
admin_email="chatadmin@example.com"
#configuration ends here

#The default username for intial login. Should not be changed
ini_username="admin"

#create chat admin user in sahana db
db.auth_user.insert(email=admin_email, username=admin_username, password=admin_password, first_name=admin_name)
db.commit()

#Server Setup
driver.get("http://127.0.0.1:9090/")
css_select("#jive-setup-save").click()
wait(wait_t)
css_select("#jive-setup-save").click()
wait(wait_t)
css_select("#rb02").click()
css_select("#jive-setup-save").click()
wait(wait_t)
css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) >  select > option[value='0']").click()
JDBC_Driver_Class=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > input")
JDBC_Driver_Class.clear()
JDBC_Driver_Class.send_keys("com.mysql.jdbc.Driver")
db_url=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input")
db_url.clear()
db_url.send_keys("jdbc:mysql://127.0.0.1:3306/"+openfire_db+"?rewriteBatchedStatements=true")
sq_user=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(5) > td:nth-of-type(2) > input")
sq_user.clear()
sq_user.send_keys(sql_username)
sq_pass=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(6) > td:nth-of-type(2) > input")
sq_pass.clear()
sq_pass.send_keys(sql_password)
css_select("#jive-setup-save").click()
wait(wait_t)
css_select("#jive-setup-save").click()
wait(wait_t)
adm_email=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > input")
adm_email.clear()
adm_email.send_keys(admin_email)
adm_pass=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > input")
adm_pass.clear()
adm_pass.send_keys(ini_password)
adm_conpass=css_select(".jive-contentBox > form > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input")
adm_conpass.clear()
adm_conpass.send_keys(ini_password)
css_select("#jive-setup-save").click()

wait(10)

server_name = login_with_initials(ini_username,ini_password)

#enable bosh
driver.get("http://127.0.0.1:9090/http-bind.jsp")
wait(wait_t)
css_select("#rb03").click()
css_select("#settingsUpdate").click()
wait(wait_t)

#install plugins
driver.get("http://127.0.0.1:9090/available-plugins.jsp")
wait(wait_t)
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
wait(30)


#relogin
server_name = login_with_initials(ini_username,ini_password)


#group creation
create_group(group_name)

registeration_property(group_name)
allow_status_messages()
#db integration part
driver.get("http://127.0.0.1:9090/server-properties.jsp")
wait(wait_t)
add_property("jdbcProvider.driver","com.mysql.jdbc.Driver")

add_property("jdbcProvider.connectionString","jdbc:mysql://localhost/"+sahana_dbname+"?user="+sql_username+"&password="+sql_password)

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
