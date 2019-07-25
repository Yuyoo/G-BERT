# -*- coding: utf-8 -*-
# @Time    : 2019-07-25 10:47
# @Author  : Yuyoo
# @Email   : sunyuyaoseu@163.com
# @File    : EDA.py

import pandas as pd
import re

d_diagnosis = pd.read_csv('/data3/MIMIC/v1_4/D_ICD_DIAGNOSES.csv')
diagnosis = pd.read_csv('/data3/MIMIC/v1_4/DIAGNOSES_ICD.csv')

icd9_10_dict = pd.read_csv('/data3/GNN/data/diagnosis_map_v1/ICD10_Formatted.csv', sep='|')


def icd9_map_icd10():
    icd9_10_dict['mimic_icd9'] = icd9_10_dict.ICD9.apply(lambda x:re.sub('\.', '', str(x)))

    d_icd9_2_icd10 = pd.merge(d_diagnosis, icd9_10_dict, left_on='ICD9_CODE', right_on='mimic_icd9')
    d_icd9_2_icd10_1v1 = d_icd9_2_icd10[d_icd9_2_icd10.ICD9_CODE.isin(d_icd9_2_icd10.ICD9_CODE.value_counts()[d_icd9_2_icd10.ICD9_CODE.value_counts()==1].index)]

    p_diagnosis_icd9_2_icd10_1v1 = pd.merge(diagnosis, d_icd9_2_icd10_1v1[['ICD9_CODE','ICD9','ICD10','ICD_name']], on='ICD9_CODE')
    p_diagnosis_icd9_2_icd10_1v1 = p_diagnosis_icd9_2_icd10_1v1.sort_values(by='ROW_ID').rename(columns={'ICD9_CODE':'MIMIC_icd9'})


    def norm_icd10_level1(x):
        """
        统一ICD编码粒度到小数点后一位
        :param x:
        :return:
        """
        x = str(x)
        if re.findall(r'\.', x):
            s1 = ''.join(re.findall(r'[a-zA-Z]|[0-9]', x.split('.')[0]))
            s2 = re.findall(r'[a-zA-Z]|[0-9]', x.split('.')[1][0])[0]
            return s1 + '.' + s2 + '00'
        else:
            s1 = ''.join(re.findall(r'[a-zA-Z]|[0-9]', x))
            return s1 + '.000'


    d_icd9_2_icd10_1v1 = d_icd9_2_icd10_1v1[d_icd9_2_icd10_1v1.ICD10.notna()]
    d_icd9_2_icd10_1v1['ICD10_level1'] = d_icd9_2_icd10_1v1.ICD10.apply(norm_icd10_level1)

    d_icd9_2_icd10_1v1.to_csv('/data3/GNN/data/diagnosis_map_v1/d_icd9_2_icd10_map_1v1.csv', index=False,sep='|')
