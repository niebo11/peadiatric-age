import pandas as pd


def treat_disease(disease, data):
    disease = disease[0:-1]
    for index, item in enumerate(disease):
        if item.find("1") != -1:
            name = item.replace("___1", "")
            data[name] = data[item]
            data.loc[data[disease[index + 1]] == 1, name] = 2
            data.loc[data[disease[index + 2]] == 2, name] = 3
            data = data.drop([item, disease[index + 1], disease[index + 2]], axis=1)
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
        data[A[i - 1]] = data[A[i - 1]].fillna(3)
        if data[A[i - 1]].min() == 0:
            data.loc[data[A[i - 1]] == 1, A[i - 1]] = 2
        data.loc[data[A[i]] == 1, A[i - 1]] = 0
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

    data["housemember_symptoms"] = data["housemember_symptoms___1"] + data["housemember_symptoms___2"] + data[
        "housemember_symptoms___3"] + data["housemember_symptoms___4"] + data["housemember_symptoms___5"]

    return data


def treat_school_symptoms(data):
    data["school_symptoms_member___1"] = data["school_symptoms_member___1"].fillna(0)
    data["school_symptoms_member___1"] = data["school_symptoms_member___1"].astype('int32')
    data["school_symptoms_member___2"] = data["school_symptoms_member___2"].fillna(0)
    data["school_symptoms_member___2"] = data["school_symptoms_member___2"].astype('int32')

    return data


def treat_na_int(data):
    # aqesta funció tracta els nans de forma basica i converteix a int


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

    data["flu_binary"] = data["flu_binary"].fillna(0)
    data["flu_binary"] = data["flu_binary"].astype('int32')

    data["vaccines_binary"] = data["vaccines_binary"].fillna(0)
    data["vaccines_binary"] = data["vaccines_binary"].astype('int32')

    # for columna in [item for item in data.columns.tolist() if data[item].dtype == "float64"]:
    #     data[columna] = data[columna].fillna(-1)
    #     data[columna] = data[columna].astype('int32')

    return data


def treat_symptoms(data, desc, yn):
    for columna in desc:
        data[columna] = data[columna].fillna(3)
        data[columna] = data[columna].astype('int32')

    for columna in yn:
        data[columna] = data[columna].fillna(0)
        data[columna] = data[columna].astype('int32')

    return data


def treat_virus(data, desc):
    for columna in desc:
        data[columna] = data[columna].fillna(3)
        data[columna] = data[columna].astype('int32')

    return data


def treat_covid(data):
    data["pcr_result"] = data["pcr_result"].fillna(0)
    data["pcr_result"] = data["pcr_result"].astype('int32')

    data["antigenic_result"] = data["antigenic_result"].fillna(0)
    data["antigenic_result"] = data["antigenic_result"].astype('int32')

    pcr_result = [item for item in data["pcr_result"]]
    ant_result = [item for item in data["antigenic_result"]]
    covid = pcr_result
    for i in range(len(data["pcr_result"].tolist())):
        if pcr_result[i] == 1:
            covid[i] = 1
        elif ant_result[i] == 1 and pcr_result[i] == 0:
            covid[i] = 1
        else:
            covid[i] = 0

    data.insert(0, "covid", covid)

    return data


def treat_coviral(data):
    data["coviral_binary"] = data["coviral_binary"].fillna(9)
    data["coviral_binary"] = data["coviral_binary"].astype('int32')

    data["coviral_type"] = data["coviral_type"].fillna(0)
    data["coviral_type"] = data["coviral_type"].astype('int32')

    data["coviral"] = data["coviral_type"] + data["coviral_binary"]

    data["bacterial_infection"] = data["bacterial_infection"].fillna(3)
    data["bacterial_infection"] = data["bacterial_infection"].astype('int32')

    data["antigenic_performed"] = data["antigenic_performed"].fillna(0)
    data["antigenic_performed"] = data["antigenic_performed"].astype('int32')
    data["pcr_performed"] = data["pcr_performed"].fillna(0)
    data["pcr_performed"] = data["pcr_performed"].astype('int32')

    return data


if __name__ == '__main__':
    rawData = pd.read_csv("data/preprocessed/COPEDICATClinicSympt_DATA_2020-12-17_1642.csv", header=0, delimiter=',')

    rawData = treat_sex(rawData)
    rawData = treat_symptoms_binary(rawData)
    rawData = treat_na_int(rawData)
    rawData = treat_school_symptoms(rawData)
    rawData = treat_covid(rawData)
    rawData = treat_coviral(rawData)

    viruses = ['vrs_result', 'adeno_result', 'flu_a_result', 'flu_b_result']
    rawData = treat_virus(rawData, viruses)

    attributes = rawData.columns.tolist()
    attributes_first = [item for item in attributes if item.find("_first") != -1]
    rawData = treat_obesity(rawData)
    rawData = treat_first(rawData, attributes_first, attributes)

    dropAttributes = ['othervirus_performed', "id", "bus", "participant_id", "recruit_date", "postal_code", "province",
                      "family_country",
                      "row_school", "sports_type", "m2", "floor_level", "rooms", "persons_home",
                      "survey_type", "cxr", "ct", "sero_date", "cxr_date", "pcr_date", "pcr_type", "antigenic_date",
                      "discharge_date", "adm_date", "comments", "survey_end_date", "housemember_symptoms___2",
                      "housemember_symptoms___3", "housemember_symptoms___4", "housemember_symptoms___5",
                      "housemember_symptoms___1", "school_symptoms_member___4", "school_symptoms_member___5",
                      "name_initials_of_the_inter", "otherviruses_date", "simptomatology_date", "date_fever",
                      "simptomatology_date",
                      "thoracic_ct_date", "adm_date", "discharge_date", "flu_date", "survey_end_date",
                      "school_symptoms", "highest_fever",
                      "total_days_fever", "end_fever", "home_confirmed", "sero", "sero_type_response", "sero_method",
                      "sero_response",
                      "sero_type_response_2", "cxr2", "ct2", "sat_hb_o2", "sat_hb_o2_value", 'other_simptomatology',
                      'other_simptomatology_3', 'other_simptomatology_4', 'other_simptomatology_lliure',
                      'final_diagnosis_text',
                      'adm_hospital', 'picu_adm', 'final_diagnosis_text', 'final_diagnosis_code', 'final_outcome',
                      'other_viruses_text',
                      'clinical_and_diagnosis_data_at_the_admission_time_complete', 'other',
                      'final_classification_of_th',
                      'final_outcome_complete', 'ag_test_mark', 'bacterial_type', 'coviral_type', 'coviral_binary',
                      'antigenic_sample',
                      ] + attributes_first

    symptomsDesc = ['fever', 'tos', 'crup', 'dysphonia', 'resp', 'tachypnea', 'wheezing', 'crackles',
                    'odynophagia', 'nasal_congestion', 'fatiga', 'headache', 'conjuntivitis', 'ocular_pain',
                    'gi_symptoms',
                    'abdominal_pain', 'vomiting', 'dyarrea', 'adenopathies', 'hepato', 'splenomegaly', 'hemorrhagies',
                    'irritability', 'shock', 'taste_smell', 'smell']

    symptomsYN = ['gi_symptoms', 'ausc_resp', 'dermatologic', 'rash', 'inflam_periferic', 'inflam_oral', 'neuro',
                  'confusion', 'seizures', 'nuchal_stiffness', 'hypotonia', 'peripheral_paralysis']

    rawData = treat_symptoms(rawData, symptomsDesc, symptomsYN)

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
    rawData_nCB = rawData_nCB[(rawData_nCB.pcr_performed != 0) | (rawData_nCB.antigenic_performed != 0)]

    rawData_CB = treat_disease(diseases, rawData)
    rawData_CB = rawData_CB[rawData_CB.comorbi_binary == 1]

    rawData_CB = rawData_CB.drop(dropAttributes, axis=1)

    rawData_CB.to_csv('data/processed/data1.csv', date_format='%B %d, %Y')
    rawData_nCB.to_csv('data/processed/data_nBC.csv', date_format='%B %d, %Y')
