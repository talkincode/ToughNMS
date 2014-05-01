#coding:utf-8

from lib import pyforms
from rules import input_style,button_style
import rules

group_add_form = pyforms.Form(
    pyforms.Textbox("hostgroup_name", rules.is_alphanum3(6, 64), description=u"群组名称",required="required",**input_style),
    pyforms.Textbox("alias", rules.len_of(1,128), description=u"群组描述", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"主机群组增加"
)



group_update_form = pyforms.Form(
    pyforms.Textbox("hostgroup_name", rules.is_alphanum3(6, 64), description=u"群组名称",readonly="readonly",**input_style),
    pyforms.Textbox("alias", rules.len_of(1,128), description=u"群组描述", **input_style),
    pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"主机群组增加"
)