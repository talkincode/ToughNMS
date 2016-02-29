#coding:utf-8

from lib import pyforms
from rules import input_style,button_style
import rules


def contact_add_form(groups=[]):
    return pyforms.Form(
        pyforms.Dropdown("contactgroup_name", description=u"联系人组",args=groups,required="required",**input_style),
        pyforms.Textbox("contact_name", rules.len_of(1, 128), description=u"联系人名称",required="required",**input_style),
        pyforms.Textbox("alias", rules.len_of(1, 128), description=u"联系人描述",required="required",**input_style),
        pyforms.Textbox("email", rules.len_of(1, 128), description=u"电子邮件",required="required",**input_style),
        pyforms.Textbox("pager", rules.len_of(1, 128), description=u"手机号码",required="required",**input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"联系人增加",
        action="/manage/contact/add"
    )()


def contact_update_form(groups=[]):
    return pyforms.Form(
        pyforms.Dropdown("contactgroup_name", description=u"联系人组",args=groups,required="required",**input_style),
        pyforms.Textbox("contact_name", rules.len_of(1, 128), description=u"联系人名称",readonly="readonly",**input_style),
        pyforms.Textbox("alias", rules.len_of(1, 128), description=u"联系人描述",required="required",**input_style),
        pyforms.Textbox("email", rules.len_of(1, 128), description=u"电子邮件",required="required",**input_style),
        pyforms.Textbox("pager", rules.len_of(1, 128), description=u"手机号码",required="required",**input_style),
        pyforms.Button("submit", type="submit", html=u"<b>提交</b>", **button_style),
        title=u"联系人修改",
        action="/manage/contact/update"
    )()

