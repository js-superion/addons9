# -*- coding: utf-8 -*-
from openerp import models, fields,api

class Lab(models.Model):
    _name = "mqc.lab"
    _description = u"临床检验"
    _inherits = {'mqc.mqc': 'mqc_id'}
    mqc_id = fields.Many2one('mqc.mqc', u'报表id', required=True,
                              ondelete='cascade')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)
    units_name = fields.Char(u'单位名称',
                             default=lambda self: self.env.user.company_id.name, )
    units_code = fields.Char(u'单位编码',
                             default=lambda self: self.env.user.company_id.units_code, )
    year_month = fields.Char(u'年月', default=lambda self: self.env['utils']._default_last_month())
    _rec_name = 'year_month'

    bblxcwl = fields.Float(u'标本类型错误率(%)', )
    bbrqcwl = fields.Float(u'标本容器错误率(%)', )
    bbcjlcwl = fields.Float(u'标本采集量错误率(%)', )
    xpyfal = fields.Float(u'血培养污染率(%)', )
    knbbnjl = fields.Float(u'抗凝标本凝集率(%)', )
    jqyzzsjzws = fields.Float(u'检验前周转时间中位数(min)', )
    snzkxmkzl = fields.Float(u'室内质控项目开展率(%)', )
    snzkxmbyxsbhgl = fields.Float(u'室内质控项目变异系数不合格率(%)', )
    snzpxmcjl = fields.Float(u'室间质评项目参加率(%)', )
    snzpxmbhgl = fields.Float(u'室间质评项目不合格率(%)', )
    sysjbdl = fields.Float(u'实验室间比对率(%)', )
    sysnzzsjzws = fields.Float(u'实验室内周转时间中位数(min)', )
    jybgcwl = fields.Float(u'检验报告不正确率(%)', )
    wjztbl = fields.Float(u'危急值通报率(%)', )
    wjztbjsl = fields.Float(u'危急值通报及时率(%)', )

    # _sql_constraints = [
    #     ('year_month_uniq',
    #      'UNIQUE (year_month)',
    #      u'本月只能上报一次数据')
    # ]

    @api.multi
    def unlink(self):
        for lba in self:
            lba.mqc_id.unlink()
        return super(Lab, self).unlink()

