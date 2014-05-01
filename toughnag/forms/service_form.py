#coding:utf-8

from lib import pyforms
from rules import input_style,button_style
import rules


service_uses = {
    "generic-service":"generic-service",
    "local-service":"local-service"
} 

notify_state = {"0":"disabled","1":u"enabled"}

def service_add_form():
    return pyforms.Form(
        pyforms.Dropdown("use", description=u"服务类型",args=service_uses.items(),required="required",**input_style),
        pyforms.Textbox("host_name", description=u"主机名称",readonly="readonly",**input_style),
        pyforms.Textbox("service_description", rules.len_of(1, 128), description=u"服务描述",required="required",**input_style),
        pyforms.Textbox("check_command", rules.len_of(1, 512), description=u"检测命令",required="required",**input_style),
        pyforms.Dropdown("notifications_enabled", args=notify_state.items(), description=u"启动通知",required="required",**input_style),        
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"服务增加",
        action="/manage/service/add"
    )()

def service_update_form():
    return pyforms.Form(
        pyforms.Dropdown("use", description=u"服务类型",args=service_uses.items(),required="required",**input_style),
        pyforms.Textbox("host_name", description=u"主机名称",readonly="readonly",**input_style),
        pyforms.Textbox("service_description", rules.len_of(1, 128), description=u"服务描述",required="required",**input_style),
        pyforms.Textbox("check_command", rules.len_of(1, 512), description=u"检测命令",required="required",**input_style),
        pyforms.Dropdown("notifications_enabled", args=notify_state.items(), description=u"启动通知",required="required",**input_style),        
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        pyforms.Hidden("service_id",description=u"service_id"),
        title=u"服务修改",
        action="/manage/service/update"
    )() 