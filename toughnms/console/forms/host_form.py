#coding:utf-8

from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style


host_uses = {
    "linux-server":"linux-server",
    "windows-server":"windows-server"
} 
state = {"0":"disabled","1":u"enabled"}

def host_add_form(groups=[]):
    return btforms.Form(
        btforms.Dropdown("use", description=u"主机类型",args=host_uses.items(),required="required",**input_style),
        btforms.Dropdown("group_name", description=u"主机分组",args=groups,required="required",**input_style),
        btforms.Textbox("host_name", rules.len_of(1, 128), description=u"主机名称",required="required",**input_style),
        btforms.Textbox("alias", rules.len_of(1, 128), description=u"主机描述",required="required",**input_style),
        btforms.Textbox("address", rules.len_of(1, 128), description=u"主机地址",required="required",**input_style),
        btforms.Dropdown("notifications_enabled", args=state.items(), description=u"启动通知",**input_style), 
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"主机增加",
        action="/host/add"

    )()

def host_update_form(groups=[]):
    return btforms.Form(
        btforms.Dropdown("use", description=u"主机类型",args=host_uses.items(),required="required",**input_style),
        btforms.Dropdown("group_name", description=u"主机分组",args=groups,required="required",**input_style),
        btforms.Textbox("host_name", rules.len_of(1, 128), description=u"主机名称",readonly="readonly",**input_style),
        btforms.Textbox("alias", rules.len_of(1, 128), description=u"主机描述",required="required",**input_style),
        btforms.Textbox("address", rules.len_of(1, 128), description=u"主机地址",required="required",**input_style),
        btforms.Dropdown("notifications_enabled", args=state.items(), description=u"启动通知",**input_style), 
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"主机修改",
        action="/host/update"
    )()



