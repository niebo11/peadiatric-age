import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
from collections import Counter

rawData = pd.read_csv("data/preprocessed/COPEDICATClinicSympt_DATA_2020-12-17_1642.csv", header=0, delimiter=',')

attributes = rawData.columns.tolist()

dropAttributes = ["id", "participant_id", "recruit_date", "postal_code", "province", "family_country",
              "row_school", "sports_type", "m2", "floor_level", "rooms","persons_home",
              "survey_type", "cxr", "ct", "sero_date", "cxr_date", "pcr_date", "pcr_type", "antigenic_date",
              "discharge_date", "adm_date", "comments", "survey_end_date"]

rawData = rawData.drop(dropAttributes, axis=1)

# TODO modificar els housemember symptoms
# TODO simptomatology_date
# TODO eliminar els first?
