import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
from collections import Counter


# This function cleans the column obesity, for each NaN value is changed for "no" otherwise is changed to "yes"
def treat_obesity(data):
    obesity = [item.lower() for item in rawData['obesity'].fillna('no')]
    for i, value in enumerate(obesity):
        if value != 'no':
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


def treat_na(data):
    '''
    aqesta funció tracta els nans de forma basica i converteix a int
    '''

    data["sports"] = data["sports"].fillna(1)
    data["sports"] = data["sports"].astype('int32')

    data["smokers_home"] = data["smokers_home"].fillna(-1)
    data["smokers_home"] = data["smokers_home"].astype('int32')

    '''el inclusion criteria te com 66% de nans, el podem eliminar o usar per fer una mostra de nomes surveys presencials idk'''
    data["inclusion_criteria"] = data["inclusion_criteria"].fillna(-1)
    data["inclusion_criteria"] = data["inclusion_criteria"].astype('int32')

    data["sympt_epi"] = data["sympt_epi"].fillna(0)
    data["sympt_epi"] = data["sympt_epi"].astype('int32')

    return data


if __name__ == '__main__':
    rawData = pd.read_csv("data/preprocessed/COPEDICATClinicSympt_DATA_2020-12-17_1642.csv", header=0, delimiter=',')
    attributes = rawData.columns.tolist()
    attributes_first = [item for item in attributes if item.find("_first") != -1]
    rawData = treat_obesity(rawData)
    rawData = treat_first(rawData, attributes_first, attributes)

    dropAttributes = ["id", "bus", "participant_id", "recruit_date", "postal_code", "province", "family_country",
              "row_school", "sports_type", "m2", "floor_level", "rooms","persons_home",
              "survey_type", "cxr", "ct", "sero_date", "cxr_date", "pcr_date", "pcr_type", "antigenic_date",
              "discharge_date", "adm_date", "comments", "survey_end_date"] + attributes_first

    rawData = rawData.drop(dropAttributes, axis=1)

    rawData = treat_obesity(rawData)
    rawData = treat_sex(rawData)
    rawData = treat_na(rawData)


print(rawData.columns.tolist())
    # TODO modificar els housemember symptoms
    # TODO simptomatology_date
    # TODO eliminar els first?
