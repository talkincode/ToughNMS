#coding:utf-8

from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style


service_uses = {
    "generic-service":"generic-service"
} 

state = {"0":"disabled","1":u"enabled"}

def service_add_form():
    return btforms.Form(
        btforms.Dropdown("use", description=u"服务类型",args=service_uses.items(),required="required",**input_style),
        btforms.Textbox("host_name", description=u"主机名称",readonly="readonly",**input_style),
        btforms.Textbox("service_description", rules.len_of(1, 128), description=u"服务描述",required="required",**input_style),
        btforms.Textbox("check_command", rules.len_of(1, 512), description=u"检测命令",required="required",help=u"命令参考",**input_style),
        btforms.Textbox("max_check_attempts", rules.is_number, description=u"最大重试次数",required="required",**input_style),
        btforms.Textbox("normal_check_interval", rules.is_number, description=u"检测间隔时间（分）",value=5, required="required",**input_style),
        btforms.Textbox("retry_check_interval", rules.is_number, description=u"重试间隔时间（分）",value=1,required="required",**input_style),
        btforms.Dropdown("notifications_enabled", args=state.items(), description=u"启动通知",**input_style),  
        btforms.Dropdown("process_perf_data", args=state.items(), description=u"启动性能统计",**input_style),              
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"服务增加",
        action="/service/add"
    )()

def service_update_form():
    return btforms.Form(
        btforms.Dropdown("use", description=u"服务类型",args=service_uses.items(),required="required",**input_style),
        btforms.Textbox("host_name", description=u"主机名称",readonly="readonly",**input_style),
        btforms.Textbox("service_description", rules.len_of(1, 128), description=u"服务描述",required="required",**input_style),
        btforms.Textbox("check_command", rules.len_of(1, 512), description=u"检测命令",required="required",help=u"命令参考",**input_style),
        btforms.Textbox("max_check_attempts", rules.is_number, description=u"最大重试次数",required="required",**input_style),
        btforms.Textbox("normal_check_interval", rules.is_number, description=u"检测间隔时间（分）",value=5,required="required",**input_style),
        btforms.Textbox("retry_check_interval", rules.is_number, description=u"重试间隔时间（分）",value=1,required="required",**input_style),
        btforms.Dropdown("notifications_enabled", args=state.items(), description=u"启动通知",**input_style),        
        btforms.Dropdown("process_perf_data", args=state.items(), description=u"启动性能统计",**input_style),                      
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        btforms.Hidden("service_id",description=u"service_id"),
        title=u"服务修改",
        action="/service/update"
    )() 