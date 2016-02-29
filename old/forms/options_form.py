#coding:utf-8

from lib import pyforms
from rules import input_style,button_style
import rules


option_update_form = pyforms.Form(
    pyforms.Textbox("system_name", rules.len_of(6, 64), description=u"系统名称", size=64,required="required",**input_style),
    pyforms.Textbox("version", rules.len_of(1,32), description=u"系统版本", size=32, required="required",**input_style),
    pyforms.Textbox("admin_name", rules.len_of(1, 32), description=u"管理员名", size=32, required="required", **input_style),
    pyforms.Textbox("nagios_bin", rules.len_of(1, 128), description=u"Nagios执行文件", readonly="readonly", **input_style),
    pyforms.Textbox("nagios_service", rules.len_of(1, 128), description=u"Nagios服务名", readonly="readonly", **input_style),
    pyforms.Textbox("nagios_cfg", rules.len_of(1, 128), description=u"Nagios配置文件", readonly="readonly", **input_style),
    pyforms.Textbox("nagios_host_group_cfg", rules.len_of(1, 128), description=u"Nagios主机组配置文件", readonly="readonly", **input_style),
    pyforms.Textbox("nagios_contact_cfg", rules.len_of(1, 128), description=u"Nagios联系人配置文件", readonly="readonly", **input_style),
    pyforms.Textbox("nagios_host_cfg_dir", rules.len_of(1, 128), description=u"Nagios主机配置目录", readonly="readonly", **input_style),    
    pyforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"系统参数更新",
    action="/manage/option"
)


passwd_update_form = pyforms.Form(
    pyforms.Textbox("admin_name", description=u"管理员名", size=32, readonly="readonly", **input_style),
    pyforms.Password("admin_pwd", rules.len_of(1, 32), description=u"管理员密码", size=32,value="", required="required", **input_style),
    pyforms.Password("admin_pwd_chk", rules.len_of(1, 32), description=u"确认管理员密码", size=32,value="", required="required", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"管理密码更新",
    action="/manage/passwd"
)