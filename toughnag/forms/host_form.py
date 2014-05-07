#coding:utf-8

from lib import pyforms
from rules import input_style,button_style
import rules

host_uses = {
    "generic-host":"generic-host",
    "linux-server":"linux-server",
    "generic-switch":"generic-switch"
} 

def host_add_form(groups=[]):
    return pyforms.Form(
        pyforms.Dropdown("use", description=u"主机类型",args=host_uses.items(),required="required",**input_style),
        pyforms.Dropdown("group_name", description=u"主机分组",args=groups,required="required",**input_style),
        pyforms.Textbox("host_name", rules.len_of(1, 128), description=u"主机名称",required="required",**input_style),
        pyforms.Textbox("alias", rules.len_of(1, 128), description=u"主机描述",required="required",**input_style),
        pyforms.Textbox("address", rules.len_of(1, 128), description=u"主机地址",required="required",**input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"主机增加",
        action="/manage/host/add"

    )()

def host_update_form(groups=[]):
    return pyforms.Form(
        pyforms.Dropdown("use", description=u"主机类型",args=host_uses.items(),required="required",**input_style),
        pyforms.Dropdown("group_name", description=u"主机分组",args=groups,required="required",**input_style),
        pyforms.Textbox("host_name", rules.len_of(1, 128), description=u"主机名称",readonly="readonly",**input_style),
        pyforms.Textbox("alias", rules.len_of(1, 128), description=u"主机描述",required="required",**input_style),
        pyforms.Textbox("address", rules.len_of(1, 128), description=u"主机地址",required="required",**input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"主机修改",
        action="/manage/host/update"
    )()



