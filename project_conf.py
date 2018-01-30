# -*-coding: utf-8-*-

from collections import defaultdict
from config import *
from login_api import *

def project_conf():
    project_name = ["普瑞逸（Pre-HC）-遗传性肿瘤基因检测-男性套餐", "普瑞逸（Pre-HC）-遗传性肿瘤基因检测-女性套餐",
                   "普瑞安（Pre-BRCA）-BRCA1/2基因检测", "普瑞畅（Pre-CRC）-Septin9 DNA甲基化检测",
                   "普诺-肿瘤预后分子检测靶标：Prognosis-MSI", "普诺-乳腺癌21基因检测（Prognosis-BC21）",
                   "普晟畅（Personal-CRC）-结直肠癌靶向用药12基因检测-组织版", "普晟畅（Personal-CRC）-结直肠癌靶向用药12基因检测-血液版",
                   "普晟朗（Personal-Lung）-肺癌靶向用药15基因检测-组织版", "普晟朗（Personal-Lung）-肺癌靶向用药15基因检测-血液版",
                   "普晟和-肿瘤靶向化疗用药83基因检测-组织版", "普晟和-肿瘤靶向化疗用药83基因检测-血液版",
                   "普益康-肿瘤个体化诊疗620基因检测-组织版", "普益康-肿瘤个体化诊疗620基因检测-血液版",
                   "普晟惠（Personal-Benefit）-化疗药物敏感性及毒副作用检测",
                    "肿瘤精准免疫治疗套餐", "普晟惠 - PD-L1及CD8蛋白表达检测", "普晟惠 - PD-L1及CD8A",
                    "mRNA表达检测（仅限科研，不可单选）", "普晟惠 - PD-L1+CD8蛋白表达+微卫星不稳定性",
                    "普晟惠 - MSI微卫星不稳定性检测","普晟安—肿瘤突变负荷检测"]
    return project_name

def lims_cc_projetc_conf():
    project_name = defaultdict()
    project_name = {"普瑞逸（Pre-HC）-遗传性肿瘤基因检测-男性套餐": "肿瘤全外显子组检测",
                    "普瑞安（Pre-BRCA）-BRCA1/2基因检测": "BRCA1/2基因检测",
                   "普瑞畅（Pre-CRC）-Septin9 DNA甲基化检测": "Septin9 DNA甲基化检测",
                    "普诺-肿瘤预后分子检测靶标：Prognosis-MSI": "Prognosis-MSI",
                   "普诺-乳腺癌21基因检测（Prognosis-BC21）": "Prognosis-BC21",
                    "普晟畅（Personal-CRC）-结直肠癌靶向用药12基因检测-组织版": "结直肠癌靶向用药12基因检测",
                   "普晟畅（Personal-CRC）-结直肠癌靶向用药12基因检测-血液版": "结直肠癌靶向用药12基因检测",
                    "普晟朗（Personal-Lung）-肺癌靶向用药15基因检测-组织版": "肺癌靶向用药15基因检测",
                   "普晟朗（Personal-Lung)-肺癌靶向用药15基因检测-血液版": "肺癌靶向用药15基因检测",
                    "普晟和-肿瘤靶向化疗用药83基因检测-组织版": "肿瘤靶向化疗用药83基因检测",
                   "普晟和-肿瘤靶向化疗用药83基因检测-血液版": "肿瘤靶向化疗用药83基因检测",
                    "普益康-肿瘤个体化诊疗620基因检测-组织版": "肿瘤个体化诊疗620基因检测",
                   "普益康-肿瘤个体化诊疗620基因检测-血液版": "肿瘤个体化诊疗620基因检测",
                    "普晟惠（Personal-Benefit）-化疗药物敏感性及毒副作用检测": "化疗药物敏感性及毒副作用检测",
                    "肿瘤精准免疫治疗套餐":"",
                   "普晟惠-PD-L1及CD8蛋白表达检测": "PD-L1及CD8蛋白表达检测",
                   "普晟惠-PD-L1及CD8A": "PD-L1及CD8A",
                    "mRNA表达检测":"mRNA表达检测",
                   "普晟惠-PD-L1+CD8蛋白表达+微卫星不稳定性":"微卫星不稳定性",
                    "普晟惠-MSI微卫星不稳定性检测": "MSI微卫星不稳定性检测",
                    "普晟安-肿瘤突变负荷检测":"肿瘤突变负荷检测"}
    return project_name


def new_wechat_project():
    project_name = defaultdict()
    project_name = {"普瑞逸-遗传性肿瘤基因检测-男性套餐": "遗传性肿瘤基因检测-男性套餐",
                    "普瑞逸-遗传性肿瘤基因检测-女性套餐": "遗传性肿瘤基因检测-女性套餐",
                    "普瑞安-BRCA1/2基因检测": "BRCA1/2基因检测",
                    "遗传性林奇综合征（5个基因）": "林奇综合征（5个基因）",
                    "遗传性乳腺癌/卵巢癌/子宫内膜癌（25个基因）": "乳腺癌/卵巢癌/子宫内膜癌（25个基因）",
                    "遗传性胰腺癌（21个基因）": "胰腺癌（21个基因）",
                    "遗传性结直肠癌（18个基因）": "结直肠癌（18个基因）",
                    "遗传性胃癌（16个基因）": "胃癌（16个基因）",
                    "遗传性肾癌（12个基因）": "肾癌（12个基因）",
                    "遗传性前列腺癌（11个基因）": "前列腺癌（11个基因）",
                    "遗传性副神经节/嗜咯细胞瘤（10个基因）": "副神经节/嗜咯细胞瘤（10个基因）",
                    "遗传性甲状腺癌（8个基因）": "甲状腺癌（8个基因）",
                    "遗传性甲状旁腺癌（4个基因）": "甲状旁腺癌（4个基因）",
                    "遗传性黑色素瘤（5个基因）": "黑色素瘤（5个基因）",
                    "遗传性多发性神经纤维瘤（2个基因）": "多发性神经纤维瘤（2个基因）",
                    "遗传性多发性神经内分泌瘤（3个基因）": "多发性神经内分泌瘤（3个基因）",
                    "遗传性视网膜母细胞瘤（1个基因）": "遗传性视网膜母细胞瘤（1个基因）",
                    "遗传性软骨肉瘤（2个基因）": "软骨肉瘤（2个基因）",
                    "遗传性肾母细胞瘤（1个基因）": "肾母细胞瘤（1个基因）",
                    "遗传性贝克威思-威德曼综合征（1个基因）": "贝克威思-威德曼综合征（1个基因）",
                    "遗传性布罗姆综合征（1个基因）": "布罗姆综合征（1个基因）",
                    "遗传性结节性硬化症（2个基因）": "结节性硬化症（2个基因）",
                    "普诺-微卫星不稳定性检测": "微卫星不稳定性检测",
                    "普诺-乳腺癌21基因检测": "乳腺癌21基因检测",
                    "普晟畅-结直肠癌靶向用药12基因检测": "结直肠癌靶向用药12基因检测",
                    "普晟朗-肺癌靶向用药15基因检测": "肺癌靶向用药15基因检测",
                    "普晟和-肿瘤靶向化疗用药83基因检测": "肿瘤靶向化疗用药83基因检测",
                    "普益康-肿瘤个体化诊疗620基因检测": "肿瘤个体化诊疗620基因检测",
                    "普晟惠-化疗药物敏感性及毒副作用检测": "化疗药物敏感性及毒副作用检测",
                    "普晟惠-靶向药物伴随检测": "靶向药物伴随检测",
                    "ProDimi-EGFR T790M": "ProDimi-EGFR T790M",
                    "肿瘤精准免疫治疗套餐": "肿瘤精准免疫治疗套餐",
                    "普晟惠-PD-L1及CD8蛋白表达检测": "PD-L1及CD8蛋白表达检测",
                    "（仅限科研）普晟惠-PD-L1及CD8A mRNA表达检测": "PD-L1及CD8A mRNA表达检测",
                    "普晟惠-PD-L1+CD8蛋白表达+微卫星不稳定性": "PD-L1+CD8蛋白表达+微卫星不稳定性",
                    "普晟惠-MSI微卫星不稳定性检测": "MSI微卫星不稳定性检测",
                    "普晟安-肿瘤全外显子组检测": "全外显子组检测",
                    "肿瘤化疗用药23基因检测":"肿瘤化疗用药23基因检测"}
    return project_name

def cc_project_ngs_noNgs():
    project_name = defaultdict()
    project_name = {"普瑞逸-遗传性肿瘤基因检测-男性套餐": "ngs",
                    "普瑞逸-遗传性肿瘤基因检测-女性套餐": "ngs",
                    "普瑞安-BRCA1/2基因检测": "noNgs",
                    "遗传性林奇综合征（5个基因）": "noNgs",
                    "遗传性乳腺癌/卵巢癌/子宫内膜癌（25个基因）": "noNgs",
                    "遗传性胰腺癌（21个基因）": "noNgs",
                    "遗传性结直肠癌（18个基因）": "noNgs",
                    "遗传性胃癌（16个基因）": "noNgs",
                    "遗传性肾癌（12个基因）": "noNgs",
                    "遗传性前列腺癌（11个基因）": "noNgs",
                    "遗传性副神经节/嗜咯细胞瘤（10个基因）": "noNgs",
                    "遗传性甲状腺癌（8个基因）": "noNgs",
                    "遗传性甲状旁腺癌（4个基因）": "noNgs",
                    "遗传性黑色素瘤（5个基因）": "noNgs",
                    "遗传性多发性神经纤维瘤（2个基因）": "noNgs",
                    "遗传性多发性神经内分泌瘤（3个基因）": "noNgs",
                    "遗传性视网膜母细胞瘤（1个基因）": "noNgs",
                    "遗传性软骨肉瘤（2个基因）": "noNgs",
                    "遗传性肾母细胞瘤（1个基因）": "noNgs",
                    "遗传性贝克威思-威德曼综合征（1个基因）": "noNgs",
                    "遗传性布罗姆综合征（1个基因）": "noNgs",
                    "遗传性结节性硬化症（2个基因）": "noNgs",
                    "普诺-微卫星不稳定性检测": "noNgs",
                    "普诺-乳腺癌21基因检测": "ngs",
                    "普晟畅-结直肠癌靶向用药12基因检测": "ngs",
                    "普晟朗-肺癌靶向用药15基因检测": "ngs",
                    "普晟和-肿瘤靶向化疗用药83基因检测": "ngs",
                    "普益康-肿瘤个体化诊疗620基因检测": "ngs",
                    "普晟惠-化疗药物敏感性及毒副作用检测": "ngs",
                    "普晟惠-靶向药物伴随检测": "noNgs",
                    "ProDimi-EGFR T790M": "noNgs",
                    "肿瘤精准免疫治疗套餐": "noNgs",
                    "普晟惠-PD-L1及CD8蛋白表达检测": "noNgs",
                    "（仅限科研）普晟惠-PD-L1及CD8A mRNA表达检测": "noNgs",
                    "普晟惠-PD-L1+CD8蛋白表达+微卫星不稳定性": "noNgs",
                    "普晟惠-MSI微卫星不稳定性检测": "noNgs",
                    "普晟安-肿瘤全外显子组检测": "ngs"}
    return project_name


def main():
    import re
    mysql = Mysql(table_name="GLORIA_MYSQL")
    sql = "select h_chinese_name from h_clinic_project;"
    data = mysql.fetch_all(sql)
    project = {}
    project_new = new_wechat_project()
    not_match = []
    for i in data:
        for keys, values in project_new.items():
        # for i in data:
            if re.search(r'%s' % values, i[0]):
                print("match", values, i[0])
                project[values] = i[0]
    print(len(project.keys()))

def test1():
    # with open("lims_project.txt",'r') as f1:
    #     info = []
    #     for lines in f1:
    #         line = lines.strip()
    #         if line not in info:
    #             info.append(line)
    #     # print(info)
    db = Mysql(table_name="GLORIA_MYSQL")
    data = new_wechat_project()
    print(data.keys())
    for keys in data.keys():
        sql = """insert into projectName values(UUID(),"%s",now(),"1.0","");""" % keys
        db.execute(sql)
    db.commit()

def test2():
    ngs_noNgs = cc_project_ngs_noNgs()
    project = new_wechat_project()
    db =  Mysql(table_name="REPORT_MYSQL")
    for keys,values in project.items():
        if keys in ngs_noNgs.keys():
            sql = """select * from projectName where projectName=\"%s\";""" % keys
            data = db.fetch_one(sql)
            if data:
                continue
            else:
                sql = """insert into projectName values(UUID(),\"%s\",now(),'1.0',"",\"%s\","何霞清");"""  % (keys, ngs_noNgs[keys])
                db.execute(sql)
    db.commit()



if __name__ == "__main__":
    # main()
    # test2()
    db = Mysql(table_name='REPORT_MYSQL')
    sql = "insert into template values(UUID(),'1ff3aaaa-ffe5-11e7-952a-3cf724cf9faf',now(),'pdl1.xml','/home/khl/web/word')"
    db.execute(sql)
    db.commit()