#coding:utf-8

from toughlib import btforms
from toughlib.btforms import rules
from toughlib.btforms.rules import button_style, input_style


def contact_add_form(groups=[]):
    return btforms.Form(
        btforms.Dropdown("contactgroup_name", description=u"联系人组",args=groups,required="required",**input_style),
        btforms.Textbox("contact_name", rules.len_of(1, 128), description=u"联系人名称",required="required",**input_style),
        btforms.Textbox("alias", rules.len_of(1, 128), description=u"联系人描述",required="required",**input_style),
        btforms.Textbox("email", rules.len_of(1, 128), description=u"电子邮件",required="required",**input_style),
        btforms.Textbox("pager", rules.len_of(1, 128), description=u"手机号码",required="required",**input_style),
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"联系人增加",
        action="/contact/add"
    )()


def contact_update_form(groups=[]):
    return btforms.Form(
        btforms.Dropdown("contactgroup_name", description=u"联系人组",args=groups,required="required",**input_style),
        btforms.Textbox("contact_name", rules.len_of(1, 128), description=u"联系人名称",readonly="readonly",**input_style),
        btforms.Textbox("alias", rules.len_of(1, 128), description=u"联系人描述",required="required",**input_style),
        btforms.Textbox("email", rules.len_of(1, 128), description=u"电子邮件",required="required",**input_style),
        btforms.Textbox("pager", rules.len_of(1, 128), description=u"手机号码",required="required",**input_style),
        btforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"联系人修改",
        action="/contact/update"
    )()

