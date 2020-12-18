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


if __name__ == '__main__':
    rawData = pd.read_csv("data/preprocessed/COPEDICATClinicSympt_DATA_2020-12-17_1642.csv", header=0, delimiter=',')
    attributes = rawData.columns.tolist()
    rawData = treat_obesity(rawData)
    print(rawData['obesity'])

    dropAttributes = ["id", "participant_id", "recruit_date", "postal_code", "province", "family_country",
                      "row_school", "sports_type", "m2", "floor_level", "rooms", "persons_home",
                      "survey_type", "cxr", "ct", "sero_date", "cxr_date", "pcr_date", "pcr_type", "antigenic_date",
                      "discharge_date", "adm_date", "comments", "survey_end_date"]

    rawData = rawData.drop(dropAttributes, axis=1)

    # TODO modificar els housemember symptoms
    # TODO simptomatology_date
    # TODO eliminar els first?
