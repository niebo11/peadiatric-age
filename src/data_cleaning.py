import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
from collections import Counter


def treat_disease(disease, data):
    disease = disease[0:-1]
    for index, item in enumerate(disease):
        if item.find("1") != -1:
            name = item.replace("___1", "")
            data[name] = data[item]
            data.loc[data[disease[index+1]] == 1, name] = 2
            data.loc[data[disease[index+2]] == 2, name] = 3
            data = data.drop([item, disease[index+1], disease[index+2]], axis=1)
    return data


# This function cleans the column obesity, for each NaN value is changed for "no" otherwise is changed to "yes"
def treat_obesity(data):
    obesity = [item.lower() for item in rawData['obesity'].fillna('no')]
    for i, value in enumerate(obesity):
        if value != 0 and value != 'si':
            if value.find('obesitat') != -1:
                obesity[i] = "si"
            elif value == "sí":
                obesity[i] = "si"
            else:
                try:
                    if float(value) >= 30:
                        obesity[i] = "si"
                    else:
                        obesity[i] = "no"
                except ValueError:
                    obesity[i] = "no"
    data['obesity'] = obesity
    return data


def treat_first(data, attr_f, A):
    for attr in attr_f:
        i = data.columns.get_loc(attr)
        data[A[i-1]] = data[A[i-1]].fillna(3)
        if data[A[i-1]].min() == 0:
            data.loc[data[A[i-1]] == 1, A[i-1]] = 2
        data.loc[data[A[i]] == 1, A[i-1]] = 0
    return data


def treat_sex(data):
    data = data.drop(data[data['sex'].isna()].index)
    data['sex'] = data['sex'].astype('int32')
    return data


def treat_symptoms_binary(data):
    data = data.drop(data[data['symptoms_binary'].isna()].index)
    data['symptoms_binary'] = data['symptoms_binary'].astype('int32')
    return data


def treat_housemember_symptoms(data):
    data["housemember_symptoms___1"] = data["housemember_symptoms___1"].fillna(0)
    data["housemember_symptoms___1"] = data["housemember_symptoms___1"].astype('int32')
    data["housemember_symptoms___2"] = data["housemember_symptoms___2"].fillna(0)
    data["housemember_symptoms___2"] = data["housemember_symptoms___2"].astype('int32')
    data["housemember_symptoms___3"] = data["housemember_symptoms___3"].fillna(0)
    data["housemember_symptoms___3"] = data["housemember_symptoms___3"].astype('int32')
    data["housemember_symptoms___4"] = data["housemember_symptoms___4"].fillna(0)
    data["housemember_symptoms___4"] = data["housemember_symptoms___4"].astype('int32')
    data["housemember_symptoms___5"] = data["housemember_symptoms___5"].fillna(0)
    data["housemember_symptoms___5"] = data["housemember_symptoms___5"].astype('int32')

    data["housemember_symptoms"] = data["housemember_symptoms___1"] + data["housemember_symptoms___2"] + data["housemember_symptoms___3"] + data["housemember_symptoms___4"] + data["housemember_symptoms___5"]

    return data


def treat_school_symptoms(data):
    data["school_symptoms_member___1"] = data["school_symptoms_member___1"].fillna(0)
    data["school_symptoms_member___1"] = data["school_symptoms_member___1"].astype('int32')
    data["school_symptoms_member___2"] = data["school_symptoms_member___2"].fillna(0)
    data["school_symptoms_member___2"] = data["school_symptoms_member___2"].astype('int32')

    return data



def treat_na_int(data):
    '''
    aqesta funció tracta els nans de forma basica i converteix a int
    '''

    data["sports"] = data["sports"].fillna(1)
    data["sports"] = data["sports"].astype('int32')

    data["smokers_home"] = data["smokers_home"].fillna(-1)
    data["smokers_home"] = data["smokers_home"].astype('int32')

    data["inclusion_criteria"] = data["inclusion_criteria"].fillna(-1)
    data["inclusion_criteria"] = data["inclusion_criteria"].astype('int32')

    data["sympt_epi"] = data["sympt_epi"].fillna(0)
    data["sympt_epi"] = data["sympt_epi"].astype('int32')

    data["school_confirmed"] = data["school_confirmed"].fillna(0)
    data["school_confirmed"] = data["school_confirmed"].astype('int32')

    # for columna in [item for item in data.columns.tolist() if data[item].dtype == "float64"]:
    #     data[columna] = data[columna].fillna(-1)
    #     data[columna] = data[columna].astype('int32')

    return data

def treat_covid(data):


    data["pcr_result"] = data["pcr_result"].fillna(0)
    data["pcr_result"] = data["pcr_result"].astype('int32')

    data["antigenic_result"] = data["antigenic_result"].fillna(0)
    data["antigenic_result"] = data["antigenic_result"].astype('int32')

    return data

if __name__ == '__main__':
    rawData = pd.read_csv("data/preprocessed/COPEDICATClinicSympt_DATA_2020-12-17_1642.csv", header=0, delimiter=',')

    rawData = treat_sex(rawData)
    rawData = treat_symptoms_binary(rawData)
    rawData = treat_na_int(rawData)
    rawData = treat_school_symptoms(rawData)
    rawData = treat_covid(rawData)

    attributes = rawData.columns.tolist()
    attributes_first = [item for item in attributes if item.find("_first") != -1]
    rawData = treat_obesity(rawData)
    rawData = treat_first(rawData, attributes_first, attributes)

    dropAttributes = ["id", "bus", "participant_id", "recruit_date", "postal_code", "province", "family_country",
              "row_school", "sports_type", "m2", "floor_level", "rooms","persons_home",
              "survey_type", "cxr", "ct", "sero_date", "cxr_date", "pcr_date", "pcr_type", "antigenic_date",
              "discharge_date", "adm_date", "comments", "survey_end_date", "housemember_symptoms___2",
              "housemember_symptoms___3", "housemember_symptoms___4", "housemember_symptoms___5",
              "housemember_symptoms___1", "school_symptoms_member___4", "school_symptoms_member___5",
              "name_initials_of_the_inter"] + attributes_first

    # No comorbi_binary
    nCB_data = rawData[rawData.comorbi_binary == 0]

    diseases = ['comorbi_binary', 'cardiopathy___1', 'cardiopathy___2', 'cardiopathy___3', 'hypertension___1',
                'hypertension___2', 'hypertension___3', 'pulmonar_disease___1', 'pulmonar_disease___2',
                'pulmonar_disease___3', 'asma___1', 'asma___2', 'asma___3', 'nephrology___1', 'nephrology___2',
                'nephrology___3', 'hepatic___1', 'hepatic___2', 'hepatic___3', 'neurologic___1', 'neurologic___2',
                'neurologic___3', 'diabetes___1', 'diabetes___2', 'diabetes___3', 'tuberculosi___1', 'tuberculosi___2',
                'tuberculosi___3', 'idp___1', 'idp___2', 'idp___3', 'neoplasia___1', 'neoplasia___2', 'neoplasia___3',
                'kawasaki___1', 'kawasaki___2', 'kawasaki___3', 'inflammation___1', 'inflammation___2',
                'inflammation___3', 'vih_others___1', 'vih_others___2', 'vih_others___3', 'comorbidities_complete']

    # comorbidities_complete unverified remove and incomplete try to complete
    rawData_nCB = nCB_data.drop(dropAttributes + diseases, axis=1)
    rawData_nCB = rawData_nCB[(rawData_nCB.pcr_performed != 0) & (rawData_nCB.antigenic_performed != 0)]

    rawData_CB = treat_disease(diseases, rawData)
    rawData_CB = rawData_CB[rawData_CB.comorbi_binary == 1]

    rawData_CB = rawData_CB.drop(dropAttributes, axis=1)


    rawData_CB.to_csv('data/processed/data1.csv', date_format = '%B %d, %Y')
    rawData_nCB.to_csv('data/processed/data_nBC.csv', date_format = '%B %d, %Y')


#print(rawData.columns.tolist())
    # TODO simptomatology_date
    # TODO fever, symptoms, drop dates, school

