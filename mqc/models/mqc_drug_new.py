# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Drug(models.Model):
    _name = "mqc.drug.new"  # 药事管理指标
    _description = u"药事管理指标"
    _inherits = {'mqc.mqc': 'mqc_id'}
    mqc_id = fields.Many2one('mqc.mqc', u'报表id', required=True,
                             ondelete='cascade')
    year_month = fields.Char(u'年月', default=lambda self: self.env['utils']._default_last_month())
    _rec_name = 'year_month'
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)
    units_name = fields.Char(u'单位名称',
                             default=lambda self: self.env.user.company_id.name, )
    units_code = fields.Char(u'单位编码',
                             default=lambda self: self.env.user.company_id.units_code, )

    # 1、一 般信息：
    ypcg_rate = fields.Float(u'药品采供率(%)')
    tpypcmccl = fields.Float(u'调配药品出门差错率(%)')
    yjkpdjewcl = fields.Float(u'一级库盘点金额误差率(%)')
    ejkpdjewcl = fields.Float(u'二级库盘点金额误差率(%)')
    mjypzwxfl = fields.Float(u'麻精药品帐物相符率(%)')
    mjypcftphgl = fields.Float(u'麻精药品处方调配合格率(%)')
    cfhgl = fields.Float(u'处方合格率(%)')
    ypblfytbsl = fields.Integer(u'药品不良反应填报数量')
    xdjyzdypblfysl = fields.Integer(u'新的及严重的药品不良反应数量')
    xdjyzdypblfyzb = fields.Float(u'新的及严重的药品不良反应占比（%）')
    zyhzywblfysbl = fields.Float(u'住院患者药物不良反应上报率（%）')
    mzcfzs = fields.Integer(u'门诊处方总数')
    jzcfzs = fields.Integer(u'急诊处方总数')
    ysshmzbhlcfbgydcfsl = fields.Integer(u'药师审核门诊不合理处方并干预的处方数量')
    ysshjzbhlcfbgydcfsl = fields.Integer(u'药师审核急诊不合理处方并干预的处方数量')
    ysshzybhlyybgyyyyzdhzsl = fields.Integer(u'药师审核住院不合理用药并干预用药医嘱的患者数量')
    yjkzzts = fields.Integer(u'一级库周转天数')
    ejkzzts = fields.Integer(u'二级库周转天数')
    cyhzs = fields.Integer(u'出院患者数')

    # 专业信息（抗菌药物）
    mzhzkjywsyl = fields.Float(u'门诊患者抗菌药物使用率（%）')
    jzhzkjywsyl = fields.Float(u'急诊患者抗菌药物使用率(%)')
    zyhzkjywsyl = fields.Float(u'住院患者抗菌药物使用率（%）')
    zyhzkjywsyqd = fields.Float(u'住院患者抗菌药物使用强度（DDD）')
    zyhzkjywsybyxzsjl = fields.Float(u'住院患者抗菌药物使用病原学总送检率(%)')
    zyhzxzjkjywsybyxsjl = fields.Float(u'住院患者限制级抗菌药物使用病原学送检率(%)')
    zyhztsjkjywsybyxsjl = fields.Float(u'住院患者特殊级抗菌药物使用病原学送检率(%)')
    xpyzsypydbfl = fields.Float(u'血培养占所有培养的百分率(%)')
    kjywfyzzyfdbfb = fields.Float(u'抗菌药物费用占总药费的百分率(%)')
    tssykjywylzkjywyldbfl = fields.Float(u'“特殊使用”抗菌药物用量占抗菌药物用量的百分率（DDDs%）(%)')
    jrssskjywyfsyl = fields.Float(u'甲乳疝手术抗菌药物预防使用率(%)')
    jrsssyfjypzhgl = fields.Float(u'甲乳疝手术预防给药品种合格率(%)')
    jrsssyfjysjhgl = fields.Float(u'甲乳疝手术预防给药时机合格率(%)')
    jrsssyfjylchgl = fields.Float(u'甲乳疝手术预防给药疗程合格率(%)')
    jrsssyfjylhyyl = fields.Float(u'甲乳疝手术预防给药联合用药率(%)')
    xgjrkjywyfsyl = fields.Float(u'血管介入抗菌药物预防使用率(%)')
    bnzsskjywyfsyl = fields.Float(u'白内障手术抗菌药物预防使用率(%)')

    # 专业信息（临床药学）
    cylchzsl = fields.Integer(u'参与临床会诊数量')
    rjkzlccfgz = fields.Integer(u'人均开展临床查房工作（次/周）')
    rjkzyxcfgz = fields.Integer(u'人均开展药学查房工作（次/周）')
    lcysshszlcksyyyzsfgdhzrs = fields.Integer(u'临床药师审核所在临床科室用药医嘱所覆盖的患者人数')
    lcysssqcyxjhdhzrs = fields.Integer(u'临床药师实施全程药学监护的患者人数')
    lcysszlckscyhzrs = fields.Integer(u'临床药师所在临床科室出院患者人数')

    # _sql_constraints = [
    #     ('year_month_uniq',
    #      'UNIQUE (year_month)',
    #      u'本月只能上报一次数据')
    # ]
    @api.multi
    def unlink(self):
        for drug in self:
            drug.mqc_id.unlink()
        return super(Drug, self).unlink()
