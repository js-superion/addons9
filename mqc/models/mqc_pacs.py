# -*- coding: utf-8 -*-

from openerp import models, fields,api

class Pacs(models.Model):
    _name = "mqc.pacs"
    _description = u'医学影像质控'
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
    #介入放射指标
    # intervene_id = fields.Many2one('mqc.pacs.intervene', u'介入放射', required=True,ondelete='cascade')
    details = fields.One2many('mqc.pacs.detail', 'pacs_id', u'指标', copy=True)

    @api.multi
    def unlink(self):
        for item in self:
            item.mqc_id.unlink()
        return super(Pacs, self).unlink()


    # _sql_constraints = [
    #     ('year_month_uniq',
    #      'UNIQUE (year_month)',
    #      u'本月只能上报一次数据')
    # ]

class PacsIntervene(models.Model):
    _name = 'mqc.pacs.intervene'
    _description = u'介入放射指标'
    year_month = fields.Char(u'年月', default=lambda self: self.env['utils']._default_last_month())
    _rec_name = 'year_month'
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)
    # 诊断部分
    open_bed_case = fields.Integer(u'开放床位数', )
    inp_case = fields.Integer(u'入院病人数', )
    outp_case = fields.Integer(u'出院病人数', )
    bed_use_rate = fields.Float(u'床位使用率(%)', )
    in_out_accord_diag = fields.Float(u'入出院诊断符合率(%)', )
    self_pay_case = fields.Integer(u'自费例数', )
    insurance_pats = fields.Integer(u'医保例数', )
    critical_pat_case = fields.Integer(u'危重病例数', )
    serial_rescue_case = fields.Integer(u'危重病例抢救成功数', )

    avg_adm_days = fields.Float(u'平均住院日', )
    outp_avg_charge = fields.Float(u'出院者平均医疗费用', )
    drug_ratio = fields.Float(u'药品占总费用比例', )
    opr_complication_rate = fields.Float(u'术后并发症发生率(%)', )
    antibiotics_prevent_rate = fields.Float(u'预防抗生素使用率(%)', )
    inblood_cure_case = fields.Integer(u'血管内治疗人数', )
    unblood_cure_case = fields.Integer(u'非血管治疗人数', )
    internal_medicine_case = fields.Integer(u'内科治疗人数', )
    sjjr_case = fields.Integer(u'神经介入诊疗人数', )
    opr_complication_rate2 = fields.Float(u'术后并发症数/率(%)', )
    inhos_infect_rate = fields.Float(u'院内感染数/率(%)', )
    accord_diag_rate = fields.Float(u'临床与病理诊断符合数/率(%)', )
    outhos_cure_case = fields.Integer(u'出院治愈人数', )
    outhos_better_case = fields.Integer(u'出院好转人数', )
    outhos_uncure_case = fields.Integer(u'出院未愈人数', )
    outhos_death_case = fields.Integer(u'出院死亡人数', )
    outhos_other_case = fields.Integer(u'其他（例）', )
    outhos_better_rate = fields.Float(u'出院好转率(%)', )
    #手术并发症
    hematoma_case = fields.Integer(u'血肿例数', ) #hematoma 血肿
    fa_case = fields.Integer(u'假性动脉瘤例数', ) #FA; false aneurysm
    vf_case = fields.Integer(u'静脉瘘例数', ) #venous fistula 静脉瘘
    vw_tear_case = fields.Integer(u'血管壁撕裂例数', ) #vascular wall
    opr_infect_case = fields.Integer(u'术后感染例数', )
    em_case = fields.Integer(u'异位栓塞例数', ) #Ectopic embolism






class PacsDevice(models.Model):
    _name = "mqc.pacs.device"
    _description = u"医学影像设备"
    name = fields.Char(u'设备名称', )


class PacsDetail(models.Model):
    _name = 'mqc.pacs.detail'
    _description = u'医学影像指标明细（CT,MRI,普放）'
    pacs_id = fields.Many2one('mqc.pacs', u'医学影像主记录', required=True, ondelete='cascade')
    device_id = fields.Many2one('mqc.pacs.device',u'影像设备')

    # 影像工作量指标
    outp_exam_case = fields.Integer(u'门诊检查人数', )
    outp_total = fields.Integer(u'门诊总量', )
    inp_exam_case = fields.Integer(u'住院检查人数', )
    adm_exam_case = fields.Integer(u'住院总量', )

    # 影像检查阳性率
    zjcrc = fields.Integer(u'总检查人次', )
    jcyxrs = fields.Integer(u'检查阳性人数', )
    jcyxxl = fields.Float(u'检查阳性率', )

    # 影像检查项目
    zqjcrs = fields.Integer(u'增强检查人数', )
    zqjczb = fields.Float(u'增强检查占比', )
    tscxjsrc = fields.Integer(u'特殊成像技术人次', )
    tscxjszb = fields.Float(u'特殊成像技术占比', )

    # 影像检查质量指标
    ccls = fields.Integer(u'抽查例数', )
    yjpls = fields.Integer(u'一级片例数', )
    yjpl = fields.Float(u'一级片率', )
    # 影像报告质量指标
    pgls = fields.Integer(u'评估例数', )
    hege = fields.Integer(u'合格', )
    hgl = fields.Float(u'合格率', )

    # 随访病例诊断符合率
    sfls = fields.Integer(u'随访例数', )
    dwzdzqs = fields.Integer(u'定位诊断准确数', )
    dwzdzql = fields.Float(u'定位诊断准确率', )
    dxzdzqs = fields.Integer(u'定性诊断准确数', )
    dxzdzql = fields.Float(u'定性诊断准确率', )

    # 影像科工作效率指标
    jzbgcyjcls = fields.Integer(u'急诊报告抽样检查例数', )
    jzbgjswcl = fields.Float(u'急诊报告及时完成率', )
    mzbgccls = fields.Integer(u'门诊报告抽查例数', )
    mzbgjswcl = fields.Float(u'门诊报告及时完成率', )
    zybgccls = fields.Integer(u'住院报告抽查例数', )
    zybgjswcl = fields.Float(u'住院报告及时完成率', )
    # 对比剂不良反应指标
    qd = fields.Integer(u'轻度', )
    zd = fields.Integer(u'中度', )
    zhongdu = fields.Integer(u'重度', )

    # 影像科服务质量指标
    mzjcrs = fields.Integer(u'门诊检查人数', )
    brtscs = fields.Integer(u'病人投诉次数', )
    dsfdcmyd = fields.Integer(u'第三方调查满意度', )
