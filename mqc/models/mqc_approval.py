# -*- coding: utf-8 -*-

from openerp import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
class MqcApproval(models.Model):
    _name = "mqc.dept.approval"
    _description = u'质控部门审批'
    name = fields.Char(u'单号', required=True, index=True, copy=False, default=u'新建')
    omitted_hospital_name = fields.Char(u'补报医院名称', default=lambda self: self.env.user.company_id.name, )
    company_id = fields.Many2one('res.company', string=u'补报医院', required=True,)
    omitted_date = fields.Char(u'补报年月', default=lambda self: self._default_omitted_date(),)
    omitted_dept = fields.Many2one('mqc.dept.type', string=u'补报部门', required=True,
                             )

    def _default_omitted_date(self):
        # utc_time = self.env['utils'].get_zero_time()
        today_datetime = datetime.today()
        last_month = (today_datetime - relativedelta(months=1)).strftime('%Y-%m')
        return last_month


    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('name', '新建'):
            vals['name'] = self.env['ir.sequence'].next_by_code('mqc.dept.approval') or '/'
        return super(MqcApproval, self).create(vals)

    # 正式启用要开启
    _sql_constraints = [
        ('company_dept_date_unique',
         'UNIQUE (company_id,omitted_dept,omitted_date)',
         u'一个医院的质控单位，只能创建一条审批记录')
    ]
