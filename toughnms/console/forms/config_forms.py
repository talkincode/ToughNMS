#coding:utf-8

from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style

boolean = {0: u"否", 1: u"是"}
booleans = {'0': u"否", '1': u"是"}
timezones = {'CST-8': u"Asia/Shanghai"}

default_form = btforms.Form(
    btforms.Dropdown("debug", args=booleans.items(), description=u"开启DEBUG", help=u"开启此项，可以获取更多的系统日志纪录",**input_style),
    btforms.Dropdown("tz", args=timezones.items(), description=u"时区", **input_style),
    btforms.Textbox("secret", description=u"安全密钥", readonly="readonly", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"系统配置管理",
    action="/config/default/update"
)

dbtypes = {'mysql': u"mysql", 'sqlite': u"sqlite"}

database_form = btforms.Form(
    btforms.Dropdown("echo", args=booleans.items(), description=u"开启数据库DEBUG", help=u"开启此项，可以在控制台打印SQL语句",**input_style),
    btforms.Dropdown("dbtype", args=dbtypes.items(), description=u"数据库类型", **input_style),
    btforms.Textbox("dburl", description=u"数据库连接字符串", **input_style),
    btforms.Textbox("pool_size", description=u"连接池大小", **input_style),
    btforms.Textbox("pool_recycle", description=u"连接池回收间隔（秒）", **input_style),
    btforms.Textbox("backup_path", description=u"数据库备份路径",hr=True, **input_style),
    btforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    btforms.Textbox("mongodb_url", description=u"日志数据库(MongoDB)地址", **input_style),
    btforms.Textbox("mongodb_port", description=u"日志数据库(MongoDB)端口", **input_style),
    title=u"数据库配置管理",
    action="/config/database/update"
)

nagios_form = btforms.Form(
    btforms.Textbox("nagios_bin", rules.len_of(1, 128), description=u"Nagios执行文件", readonly="readonly", **input_style),
    btforms.Textbox("nagios_service", rules.len_of(1, 128), description=u"Nagios服务名", readonly="readonly", **input_style),
    btforms.Textbox("nagios_cfg", rules.len_of(1, 128), description=u"Nagios配置文件", readonly="readonly", **input_style),
    btforms.Textbox("nagios_host_group_cfg", rules.len_of(1, 128), description=u"Nagios主机组配置文件", readonly="readonly", **input_style),
    btforms.Textbox("nagios_contact_cfg", rules.len_of(1, 128), description=u"Nagios联系人配置文件", readonly="readonly", **input_style),
    btforms.Textbox("nagios_host_cfg_dir", rules.len_of(1, 128), description=u"Nagios主机配置目录", readonly="readonly", **input_style),    
    btforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"nagios配置管理",
    action="/config/nagios/update"
)

mail_form = btforms.Form(
    btforms.Textbox("smtp_server", description=u"SMTP服务器", **input_style),
    btforms.Textbox("smtp_port", description=u"SMTP服务器端口", **input_style),
    btforms.Textbox("smtp_from", description=u"SMTP邮件发送地址", **input_style),
    btforms.Textbox("smtp_user", description=u"SMTP用户名", **input_style),
    btforms.Textbox("smtp_pwd", description=u"SMTP密码", help=u"如果密码不是必须的，请填写none", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>更新</b>", **button_style),
    title=u"邮件服务配置",
    action="/param/update?active=mailcfg"
)
