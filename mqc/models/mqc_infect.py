# -*- coding: utf-8 -*-

from openerp import models, fields

class Infect(models.Model):
    _name = "mqc.infect"
    _description = u'医院感染发生情况'
    _inherits = {'mqc.mqc': 'mqc_id'}
    mqc_id = fields.Many2one('mqc.mqc', u'报表id', required=True,
                             ondelete='cascade')

    units_name = fields.Char(u'单位名称',
                             default=lambda self: self.env.user.company_id.name, )
    units_code = fields.Char(u'单位编码',
                             default=lambda self: self.env.user.company_id.units_code, )

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)

    year_month = fields.Char(u'年月', default=lambda self: self.env['utils']._default_last_month())
    quarter = fields.Char(u'季度', default=lambda self: self.env['utils']._default_quarter_name())
    _rec_name = 'year_month'

    out_case = fields.Integer( u'出院人次', )
    infect_pat = fields.Integer(u'医院感染人数',)
    infect_rate = fields.Float(u'医院感染发生率%',)
    infect_cases = fields.Integer( u'医院感染例次数',)
    infect_cases_rate = fields.Float( u'医院例次感染率%',)

    #ICU医院感染发生情况
    icu_monitor_num = fields.Integer(u'监测人数')
    icu_infect_pat = fields.Integer(u'感染人数', )
    icu_infect_rate = fields.Float(u'感染发生率%', )
    icu_infect_cases = fields.Integer(u'感染例次数', )
    icu_infect_cases_rate = fields.Float(u'例次感染率%', )
    icu_in_days = fields.Integer(u'住院总日数', )
    icu_day_infect_rate = fields.Float(u'日感染率%', )
    icu_incidence_rate = fields.Float(u'例次日感染发病率%', )
    icu_avg_severity = fields.Char(u'平均病情严重程度', )
    icu_adjust_day_infect = fields.Float(u'调整日感染率(%)', )
    icu_adjust_case_infect = fields.Float(u'调整例次日感染率%', )

    #手术部位感染监测
    opr_num = fields.Integer(u'手术患者人数', )
    site_infect_cases = fields.Integer(u'手术部位感染例次数')
    site_infect_rate = fields.Float(u'手术部位感染率%', )
    opr1_num = fields.Integer(u'I类手术患者人数', )
    opr1_incision_case = fields.Integer(u'I类手术切口感染例次', )
    opr1_incision_rate = fields.Float(u'I类手术切口感染例次率(%)', )

    #现患率调查
    xhl_std_num = fields.Integer(u'应查人数', )
    xhl_fct_num = fields.Integer(u'实查人数')
    xhl_fct_rate = fields.Float(u'实查率%', )
    xhl_ill_num = fields.Integer(u'现患人数', )
    xhl_ill_rate = fields.Float(u'现患率%', )
    xhl_ill_case = fields.Integer(u'现患例次', )
    xhl_ill_case_rate = fields.Float(u'现患例次率%', )

    #医院感染暴发情况
    gr_std_num = fields.Integer(u'出院人次', )
    gr_fct_num = fields.Integer(u'确认医院感染暴发次数')
    part_id = fields.Many2one('mqc.infect.part', u'医院感染暴发部位' )
    gr_ill_num = fields.Char(u'医院感染暴发病原体', )
    gr_ill_rate = fields.Char(u'法定传染病', )

    #继续教育情况
    country_pro = fields.Integer(u'专职人员(国家)', )
    country_other = fields.Integer(u'其它(国家)')
    province_pro = fields.Integer(u'专职人员(省)', )
    province_other = fields.Integer(u'其它(省)', )
    city_pro = fields.Integer(u'专职人员(市)', )
    city_other = fields.Integer(u'其它(市)', )
    exam_num = fields.Integer(u'参加“感控家园”理论考试人次', )
    avg_scores = fields.Integer(u'参加“感控家园”理论考试平均成绩', )


    part_ids = fields.One2many('mqc.infect.parts', 'infect_id', u'前五位感染部位',copy=True) #copy=true，同时复制明细
    hand_ids = fields.One2many('mqc.infect.hand',  'infect_id',u'手卫生监测情况',copy=True)
    env_ids = fields.One2many('mqc.infect.env',  'infect_id',u'环境卫生学监测情况',copy=True)
    devices_ids = fields.One2many('mqc.infect.devices',  'infect_id',u'器械相关感染监测',copy=True)
    rbm_ids = fields.One2many('mqc.infect.rbm',  'infect_id',u'耐药菌监测',copy=True)

    infect_icu_id = fields.Many2one('mqc.infect.icu', u'ICU医院感染发生情况',ondelete='cascade')
    ssi_id = fields.Many2one('mqc.infect.ssi',u'手术部位感染监测',ondelete='cascade')
    ill_id = fields.Many2one('mqc.infect.ill', u'现患率调查',ondelete='cascade')
    break_id = fields.Many2one('mqc.infect.break', u'医院感染暴发情况',ondelete='cascade')
    edu_id = fields.Many2one('mqc.infect.edu', u'继续教育情况',ondelete='cascade')


    # _sql_constraints = [
    #     ('year_month_uniq',
    #      'UNIQUE (year_month)',
    #      u'本月只能上报一次数据')
    # ]


#相关字典
class InfectPart(models.Model):
    _name = "mqc.infect.part"
    _description = u"感染部位"
    name = fields.Char(u'部位',)


class InfectDevice(models.Model):
    _name = "mqc.infect.device"
    _description = u"器械名称"
    name = fields.Char(u'器械名称', )

class InfectBacteria(models.Model):
    _name = "mqc.infect.bacteria"
    _description = u"耐药菌名称"
    name = fields.Char(u'耐药菌名称', )


class InfectParts(models.Model):
    _name = "mqc.infect.parts"
    _description = u"感染部位明细"
    infect_id = fields.Many2one('mqc.infect', u'感染主记录', required=True,ondelete='cascade')
    part_id = fields.Many2one('mqc.infect.part', u'部位', required=True)
    infect_cases = fields.Integer(u'例次数：')

class InfectHand(models.Model):
    _name = "mqc.infect.hand"
    _description = u"手卫生监测"
    infect_id = fields.Many2one('mqc.infect', u'感染主记录', required=True,ondelete='cascade')
    staff_type = fields.Selection([('01', u'医生'), ('02', u'护士'), ('03', u'实习、进修人员'), ('04', u'保洁人员')],
                                   u'人员类别')
    monitor_num = fields.Integer(u'监测人数')
    std_times = fields.Integer(u'应洗手次数')
    fct_times = fields.Integer(u'实洗手次数')
    correct_times = fields.Integer(u'正确次数')

class InfectEnv(models.Model):
    _name = "mqc.infect.env"
    _description = u"环境卫生监测"
    infect_id = fields.Many2one('mqc.infect', u'感染主记录', required=True,ondelete='cascade')
    sample_id = fields.Many2one('mqc.infect.sample',u'标本名',required=True, )
    monitor_num = fields.Integer(u'监测数')
    accept_num = fields.Integer(u'合格数')
    accept_rate = fields.Integer(u'合格率(%)')



class InfectSample(models.Model):
    _name = "mqc.infect.sample"
    _description = u"标本名称"
    name = fields.Char(u'标本名称', )

class InfectIcu(models.Model):
    _name = "mqc.infect.icu"
    _description = u"ICU医院感染发生情况"
    monitor_num = fields.Integer(u'监测人数')
    infect_pat = fields.Integer(u'感染人数',)
    infect_rate = fields.Float(u'感染发生率%',)
    infect_cases = fields.Integer( u'感染例次数',)
    infect_cases_rate = fields.Integer( u'例次感染率%',)

    in_days = fields.Integer( u'住院总日数',)
    day_infect_rate = fields.Float( u'日感染率%',)
    incidence_rate = fields.Float( u'例次日感染发病率%',)
    avg_severity = fields.Char( u'平均病情严重程度',)
    adjust_day_infect = fields.Float( u'调整日感染率(%)',)
    adjust_case_infect = fields.Float( u'调整例次日感染率%',)

class InfectDevices(models.Model):
    _name = "mqc.infect.devices"
    _description = u"器械相关感染监测"
    infect_id = fields.Many2one('mqc.infect', u'感染主记录', required=True, ondelete='cascade')
    device_id = fields.Many2one('mqc.infect.device', u'器械名称', required=True, )

    in_days = fields.Integer(u'住院总日数', )
    use_days = fields.Integer(u'器械使用天数')
    use_rate = fields.Float(u'器械使用率%',)
    infect_pat = fields.Integer(u'感染人数', )
    infect_rate = fields.Float(u'感染发生率%',)
    infect_cases = fields.Integer( u'感染例次',)
    infect_cases_rate = fields.Integer( u'例次感染率%',)

class InfectSsi(models.Model):
    _name = "mqc.infect.ssi" #ssi,Surgical SiteInfection，手术上的  部位感染
    _description = u"手术部位感染监测"
    # infect_id = fields.Many2one('mqc.infect', u'感染主记录', required=True, )

    opr_num = fields.Integer(u'手术患者人数', )
    site_infect_cases = fields.Integer(u'手术部位感染例次数')
    site_infect_rate = fields.Float(u'手术部位感染率%',)
    opr1_num = fields.Integer(u'I类手术患者人数', )
    opr1_incision_case = fields.Integer(u'I类手术切口感染例次',)
    opr1_incision_rate = fields.Float( u'I类手术切口感染例次率(%)',)

class InfectRbm(models.Model):
    _name = "mqc.infect.rbm" #rbm,resistance bacteria monitor，缩写 抵抗  细菌 监测
    _description = u"耐药菌监测"
    infect_id = fields.Many2one('mqc.infect', u'感染主记录', required=True, ondelete='cascade')
    bacteria_id = fields.Many2one('mqc.infect.bacteria', u'菌株名称', required=True, )
    bacteria_num = fields.Integer( u'检出株数',)

class InfectIll(models.Model):
    _name = "mqc.infect.ill" #ill rate 现患率
    _description = u"现患率调查"
    _rec_name = 'year_month'
    year_month = fields.Char(u'年月', default=lambda self: self.env['utils']._default_last_month())
    std_num = fields.Integer(u'应查人数', )
    fct_num = fields.Integer(u'实查人数')
    fct_rate = fields.Float(u'实查率%',)
    ill_num = fields.Integer(u'现患人数', )
    ill_rate = fields.Float(u'现患率%',)
    ill_case = fields.Integer( u'现患例次',)
    ill_case_rate = fields.Float( u'现患例次率%',)

class InfectBreak(models.Model):
    _name = "mqc.infect.break" #ill rate 现患率
    _description = u"医院感染暴发情况"
    _rec_name = 'year_month'
    year_month = fields.Char(u'年月', default=lambda self: self.env['utils']._default_last_month())
    std_num = fields.Integer(u'出院人次', )
    fct_num = fields.Integer(u'确认医院感染暴发次数')
    fct_rate = fields.Integer(u'医院感染暴发部位',)
    ill_num = fields.Integer(u'医院感染暴发病原体', )
    ill_rate = fields.Integer(u'法定传染病',)

class InfectEdu(models.Model):
    _name = "mqc.infect.edu" #ill rate 现患率
    _description = u"继续教育情况"
    _rec_name = 'year_month'
    year_month = fields.Char(u'年月', default=lambda self: self.env['utils']._default_last_month())
    country_pro = fields.Integer(u'专职人员(国家)', )
    country_other = fields.Integer(u'其它(国家)')
    province_pro = fields.Integer(u'专职人员(省)',)
    province_other = fields.Integer(u'其它(省)', )
    city_pro = fields.Integer(u'专职人员(市)',)
    city_other = fields.Integer(u'其它(市)',)
    exam_num = fields.Integer(u'参加“感控家园”理论考试人次',)
    avg_scores = fields.Integer(u'参加“感控家园”理论考试平均成绩',)
