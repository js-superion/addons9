# -*- coding: utf-8 -*-
import datetime, pytz

from math import ceil

from openerp import models, fields,api,_
from openerp.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
class utils(models.Model):
    # def __init__(self,name):
    #     self.name = name;
    def get_zero_time(self):
        '''
        获取当前时区的utc时间
        :return:
        '''
        now_time = datetime.datetime.today()
        tz = self.env.user.tz or 'Asia/Shanghai'
        tz_timedelta = now_time.replace(tzinfo=pytz.timezone('UTC')) - now_time.replace(tzinfo=pytz.timezone(tz))
        zero_time = now_time - tz_timedelta
        zero_time = zero_time.replace(tzinfo=pytz.timezone('UTC'))
        return zero_time

    def _default_quarter_name(self):
        quarter_names = {1:u'一季度',2:u'二季度',3:u'三季度',4:u'四季度'}
        current_month = datetime.datetime.now().month - 1
        quarter = current_month // 3 + 1
        quarter_name = ""
        for key in quarter_names.keys():
            if key == quarter:
                quarter_name = quarter_names[key]
                break
        return quarter_name


    def _default_last_month(self):
        """ 校验当前日期，如果在 current_date 在 forbiden_date 以后，则提示不给上报,否则赋给默认值
         forbiden_date 通过参数来获取
        """
        utc_time = self.env['utils'].get_zero_time()
        current_date = utc_time.strftime('%d')
        forbiden_date = self.env["ir.config_parameter"].get_param("mqc_report_forbiden_date")
        today_datetime = datetime.datetime.today()
        last_month = (today_datetime - relativedelta(months=1)).strftime('%Y-%m')
        if int(current_date) > int(forbiden_date):
            #根据所在医院，质控单位，年月，查询查询审批结果
            company_id = self.env.user.company_id.id
            #获取质控单位类型
            type_code = self.env.user.employee_ids.department_id.type_code.id
            department_name = self.env.user.employee_ids.department_id.name
            if not type_code:
                raise ValidationError(_('您当前所在部门:%s 没有对应的质控类型!!\n请到部门菜单中，将信息填写完整!') % department_name)
            approval = self.env['mqc.dept.approval'].sudo().search([
            ('company_id', '=', company_id),
            ('omitted_dept', '=', type_code),
            ('omitted_date', '=', last_month)])
            if not approval:
                raise ValidationError(_('不允许填报,当前设置：每月%s号为填报截止日期!\n请联系上级部门') % forbiden_date)
        return last_month


