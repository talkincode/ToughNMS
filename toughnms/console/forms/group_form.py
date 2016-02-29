#coding:utf-8

from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style


group_add_form = btforms.Form(
    btforms.Textbox("hostgroup_name", rules.is_alphanum3(6, 64), description=u"群组名称",required="required",**input_style),
    btforms.Textbox("alias", rules.len_of(1,128), description=u"群组描述", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"主机群组增加",
    action="/group/add"
)



group_update_form = btforms.Form(
    btforms.Textbox("hostgroup_name", rules.is_alphanum3(6, 64), description=u"群组名称",readonly="readonly",**input_style),
    btforms.Textbox("alias", rules.len_of(1,128), description=u"群组描述", **input_style),
    btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
    title=u"主机群组增加",
    action="/group/update"
)