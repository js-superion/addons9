# -*- coding: utf-8 -*-
from openerp import models, fields,api

class Index(models.Model):
    _name = "mqc.index" #index 医疗质量指标
    _description = u"医疗质量信息"
    _inherits = {'mqc.mqc': 'mqc_id'}
    mqc_id = fields.Many2one('mqc.mqc', u'报表id', required=True,
                              ondelete='cascade')
    units_name = fields.Char(u'单位名称',
                             default=lambda self: self.env.user.company_id.name, )
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)
    units_code = fields.Char(u'单位编码',
                             default=lambda self: self.env.user.company_id.units_code, )
    year_month = fields.Char(u'年月', default=lambda self: self.env['utils']._default_last_month())
    _rec_name = 'year_month'

    #1、一般指标：
    outpat_capacity = fields.Integer(u'门诊量')
    discharged_case = fields.Integer(u'出院人数')
    accord_diag_case = fields.Float(u'出入院诊断符合率(%)')
    rescue_rate = fields.Float(u'抢救成功率(%)')
    avg_adm_days = fields.Float(u'平均住院天数')
    bed_use_rate = fields.Float(u'床位使用率(%)')
    mr_grade_a_rate = fields.Float(u'甲级病案率(%)') #mr medical record
    #2、专项指标：
    opr_three_four = fields.Float(u'四/三级手术率（三/二级医院）(%)')
    unplanned_opr_two = fields.Float(u'非计划二次手术率/例')
    antibiotics_use_rate = fields.Float(u'抗菌药物使用率/强度') #antibiotics抗生素
    cp_disease = fields.Float(u'临床路径开展病种数/例数') #cp clinic path

    #3、医疗纠纷情况：
    dispute_case = fields.Float(u'纠纷投诉发生例数')
    attacked_case = fields.Float(u'医务人员受人身冲击数')

    #4、落实患者安全目标（是/否）：
    protect_pat1 = fields.Selection([('1', u'是'), ('0', u'否')],u'是否落实手术安全核查、风险评估、术者亲自沟通制度')
    protect_pat2 = fields.Selection([('1', u'是'), ('0', u'否')],u'是否有患者身份识别与手术部位标识')
    protect_pat3 = fields.Selection([('1', u'是'), ('0', u'否')],u'是否主动报告医疗隐患、医疗不良事件')

    # 5、临床路径管理：
    is_cp = fields.Float(u'是否开展临床路径')
    cp_discharged_case = fields.Float(u'出院病例总数')
    cp_accord_diag_case = fields.Float(u'符合进入临床路径标准的病例数')
    dept_with_cp = fields.Float(u'实施临床路径专业数')
    disease_case_in_cp = fields.Float(u'实施临床路径病种数')
    cp_case = fields.Float(u'进入临床路径的病例数')
    cp_variation = fields.Float(u'发生变异的病例数')
    cp_quit = fields.Float(u'退出路径的病例数')
    cp_finish = fields.Float(u'完成路径的病例数')

    # 6、医疗质量管理与控制体系建设：
    kzjysjzpxm_case = fields.Float(u'开展检验室间质评项目数量')
    jcjyjg_1 = fields.Float(u'三基医院检查、检验结果互认项目数量')
    jcjyjg_2 = fields.Float(u'三级医院与二级医院间检查、检验结果互认项目数量')
    ndkzycblhz_case = fields.Float(u'年度开展远程病理会诊病例数')
    ndkzycyxzdhz_case = fields.Float(u'年度开展远程影像诊断会诊病例数')

    # 7、疾病诊疗质量连续化管理：
    kzzlzllxhgljb_case = fields.Float(u'开展诊疗质量连续化管理的疾病数量')
    xgbzxzsl = fields.Float(u'相关病种下转数量')

    # 8、日间手术质量精细化管理
    sfjlrjsszlaqglzd = fields.Selection([('1', u'是'), ('0', u'否')],u'是否建立日间手术质量安全管理制度')
    kzrjssbz_case = fields.Float(u'开展日间手术的病种数')
    rjssjsml_case = fields.Float(u'日间手术技术目录数')
    kzrjss_case = fields.Float(u'开展日间手术总例数')
    cqqsmzrjss_case = fields.Float(u'采取全身麻醉的日间手术例数')
    rjsshzbfzfs_case = fields.Float(u'日间手术患者并发症发生例数')
    rjsshzsh48_case = fields.Float(u'日间手术患者术后48小时内收入院例数')
    rjsshzshsf_case = fields.Float(u'日间手术患者术后随访例数')

    #9、提升县医院和民营医院质量安全水平
    sfkzjrzljs = fields.Selection([('1', u'是'), ('0', u'否')],u'是否开展介入诊疗技术')
    sfkzsjysnjzljs = fields.Selection([('1', u'是'), ('0', u'否')],u'是否开展三级以上内镜诊疗技术')
    sfkzxyjhjs = fields.Selection([('1', u'是'), ('0', u'否')],u'是否开展血液净化技术')

    # _sql_constraints = [
    #     ('year_month_uniq',
    #      'UNIQUE (year_month)',
    #      u'本月只能上报一次数据')
    # ]

    @api.multi
    def unlink(self):
        for index in self:
            index.mqc_id.unlink()
        return super(Index, self).unlink()


