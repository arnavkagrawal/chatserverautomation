#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#definations
driver = webdriver.Firefox()
css_select = driver.find_element_by_css_selector 
wait=time.sleep

def add_property(property_name, property_value):
    p_n_field=css_select(".jive-table > table > tbody> tr:nth-of-type(1) > td:nth-of-type(2) > input")
    p_v_field=css_select(".jive-table > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > textarea")
    p_n_field.send_keys(property_name)
    p_v_field.send_keys(property_value)
    save_prop=css_select(".jive-table > table > tfoot > tr:nth-of-type(1) > td:nth-of-type(1) > input:nth-of-type(1)")
    save_prop.click()
    wait(1)
    return

def edit_property(property_name,value):
    search_string="//*[contains(text(),'"+ property_name +"')]"
    elem = driver.find_elements_by_xpath(search_string)
    elem[0].find_elements_by_xpath("ancestor::tr/td[3]/a")[0].click() 
    property_value=css_select(".jive-table > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > textarea")
    property_value.clear()
    property_value.send_keys(value)
    submit_but=css_select(".jive-table > table > tfoot > tr:nth-of-type(1) > td:nth-of-type(1) > input:nth-of-type(1)")
    submit_but.click()
    wait(1)
    return

#roster sharing by group creation
def create_group(group_name):
    user_group=css_select("#jive-nav >  ul > li:nth-of-type(2) > a")
    user_group.click()
    wait(1)
    group=css_select("#jive-subnav > ul > li:nth-of-type(2) > a")
    group.click()
    wait(1)
    group=css_select("#jive-subnav > ul > li:nth-of-type(2) > a")
    create_new_group=css_select("#jive-sidebar > ul > li:nth-of-type(2) > a")
    create_new_group.click()
    wait(1)
    group_name=css_select(".jive-contentBox > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2) > input ")
    group_name.send_keys(group_name)
    save_group=css_select(".jive-contentBox > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input:nth-of-type(1) ")
    save_group.click()
    wait(1)
    #roster sharing enable
    css_select(".jive-contentBox > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > input").click()
    wait(1)
    contact_list=css_select("#jive-roster > input")
    contact_list.send_keys(group_name)
    css_select("#cb101").click()
    wait(1)
    css_select(".jive-contentBox > table > tbody > tr:nth-of-type(3) > td:nth-of-type(2) > input").click()
    wait(1)
    return

#default adding of users to group
def registeration_property(group_name):
    driver.get("http://127.0.0.1:9090/plugins/registration/registration-props-form.jsp")
    default_group=css_select(".jive-contentBox > table > tbody > tr > td > input")
    default_group.clear()
    default.group.send_keys(group_name) 
    css_select(".jive-contentBox > input ").click()
    wait(1)
    css_select(".jive-contentBox > table > tbody > tr:nth-of-type(4) > td:nth-of-type(1) > input").click()
    wait(1)
    css_select(".jive-contentBox > input").click()
    wait(1)
    return


def add_admin_to_group(group_name,admin_username):
    driver.get("http://127.0.0.1:9090/group-edit.jsp?group="+group_name)
    add_user=css_select(".jive-contentBox > form > table > tbody > tr > td:nth-of-type(2) > input:nth-of-type(1)")
    add_user.send_keys(admin_username)
    css_select(".jive-contentBox > form > table > tbody > tr > td:nth-of-type(2) > input:nth-of-type(1)").click()
    wait(1)
    return

def allow_status_messages():
    driver.get("http://127.0.0.1:9090/plugins/presence/presence-service.jsp")
    css_select("#rb01").click()
    wait(1)
    css_select("#jive-main-content > form > input").click()
    wait(1)
    return

#configure settings here
group_name="everyone"
sql_username="root"
sql_password="knowing42"
#the username for intial user 
ini_username="admin"
#the password for intial user 
ini_password="admin"
#the new user created by w2p 
admin_username="normaluser_example.com"
server_name="arnav-inspiron-7520"


driver.get("http://127.0.0.1:9090/")

username_field = driver.find_element_by_name("username")
pass_field = driver.find_element_by_name("password")
#initial login
username_field.send_keys(ini_username)
pass_field.send_keys(ini_password)
login_button = css_select("input[type='submit']")
login_button.click()
#wait to load page
wait(1)

#group creation
create_group(group_name)

registeration_property(group_name)
allow_status_messages()

#db integration part
properties = css_select("#jive-sidebar > ul > li:nth-of-type(2) > a")
properties.click()
wait(1)

add_property("jdbcProvider.driver","com.mysql.jdbc.Driver")

#to change
add_property("jdbcProvider.connectionString","jdbc:mysql://localhost/<sahana database name>?user="+sql_username+"&password="+sql_password)

add_property("jdbcAuthProvider.passwordSQL","select password from auth_user where username=?")
add_property("jdbcAuthProvider.passwordType","plain")
add_property("jdbcUserProvider.loadUserSQL","select first_name,email from auth_user where username=?")
add_property("jdbcUserProvider.userCountSQL","select count(*) from auth_user")
add_property("jdbcUserProvider.allUsersSQL","select username from auth_user")
add_property("jdbcUserProvider.searchSQL","select username from auth_user where")
add_property("jdbcUserProvider.usernameField","username")
add_property("jdbcUserProvider.emailField","email")
add_property("jdbcUserProvider.nameField","first_name")

#tochange
add_property("admin.authorizedJIDs",admin_username+"@"+server_name)

#edit already present property
edit_property("provider.auth.className","org.jivesoftware.openfire.auth.JDBCAuthProvider ")
edit_property("provider.user.className","org.jivesoftware.openfire.user.JDBCUserProvider ")

add_admin_to_group(group_name,admin_username)
driver.close()
