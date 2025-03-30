import os
from box.exceptions import BoxValueError
import yaml
from default_predictor import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import pandas as pd
from streamlit.components.v1 import html


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read YAML files and returns
    
    Args:
        path_to_yaml (str): path of the YAML file
        
    Raises:
        ValueError: If the YAML file is empty
        e: empty file
        
    Returns:
        ConfigBox: ConfigBox type file
    """
    
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file {path_to_yaml} loaded successfuly")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as e:
        raise e
    


@ensure_annotations
def check_schema(path_of_csv: Path, schema: dict , path_of_status_file: Path) -> bool:
    """
    Validates the schema of the csv
    
    Args:
        path_of_csv (Path): The path of the CSV
        path_of_status_file (Path): The path of the status file
        
    Returns:
        str: If the CSV is validated
    
    """
    
    data = pd.read_csv(path_of_csv)
    all_columns = list(data.columns)
    all_schema = schema.keys()
    
    validation_status = None
    
    with open(path_of_status_file, 'w') as f:
        f.write(f"Validation status: Not Started")

    for col in all_columns:
        if col not in all_schema:
            validation_status = False
            with open(path_of_status_file, 'w') as f:
                f.write(f"Validation status:  {validation_status}")
        else:
            validation_status = True
            with open(path_of_status_file, 'w') as f:
                f.write(f"Validation status: {validation_status}")
    return validation_status

@ensure_annotations
def months_since_last(row):
    for i, value in enumerate(row):
        if value>0:
            return i
    return len(row) 
    
@ensure_annotations
def clean_df(path_of_csv: Path) -> pd.DataFrame:
    """
    cleaning the submitted pandas dataframe.
    """
    
    data = pd.read_csv(path_of_csv)
    
    #remove nature of business columns
    data = data.loc[:, ~data.columns.str.startswith('NATURE')]
    
    #reduce dimensions by adding fee together
    data['LATE_PAY_FEE']=data['LATE_PAY_FEE_1']+data['LATE_PAY_FEE_2']+data['LATE_PAY_FEE_3']+data['LATE_PAY_FEE_4']+data['LATE_PAY_FEE_5']+data['LATE_PAY_FEE_6']
    data['OVER_LIMIT_FEE']=data['OVER_LIMIT_FEE_1']+data['OVER_LIMIT_FEE_2']+data['OVER_LIMIT_FEE_3']+data['OVER_LIMIT_FEE_4']+data['OVER_LIMIT_FEE_5']+data['OVER_LIMIT_FEE_6']
    data=data.drop(columns=['LATE_PAY_FEE_1','LATE_PAY_FEE_2','LATE_PAY_FEE_3','LATE_PAY_FEE_4','LATE_PAY_FEE_5','LATE_PAY_FEE_6'])
    data=data.drop(columns=['OVER_LIMIT_FEE_1','OVER_LIMIT_FEE_2','OVER_LIMIT_FEE_3','OVER_LIMIT_FEE_4','OVER_LIMIT_FEE_5','OVER_LIMIT_FEE_6'])
    
    #remove Ascore
    data=data.drop(columns=['A_SCORE_VALUE'])
    
    #get average of total_os due to high correlation
    data['TOTAL_OS']=(data['TOTAL_OS_1']+data['TOTAL_OS_2']+data['TOTAL_OS_3']+data['TOTAL_OS_4']+data['TOTAL_OS_5']+data['TOTAL_OS_6'])/6
    data=data.drop(columns=['TOTAL_OS_1','TOTAL_OS_2','TOTAL_OS_3','TOTAL_OS_4','TOTAL_OS_5','TOTAL_OS_6'])
    
    #adding time series features
    spend_columns = ['TOT_SPEND_AMT_1', 'TOT_SPEND_AMT_2', 'TOT_SPEND_AMT_3', 'TOT_SPEND_AMT_4', 'TOT_SPEND_AMT_5', 'TOT_SPEND_AMT_6']
    pay_columns = ['PAYMENT_AMT_1', 'PAYMENT_AMT_2', 'PAYMENT_AMT_3', 'PAYMENT_AMT_4', 'PAYMENT_AMT_5', 'PAYMENT_AMT_6']
    settler_columns = ['REV_SETT_1_SETTLER', 'REV_SETT_2_SETTLER', 'REV_SETT_3_SETTLER', 'REV_SETT_4_SETTLER', 'REV_SETT_5_SETTLER', 'REV_SETT_6_SETTLER']
    revolver_columns = ['REV_SETT_1_REVOLVER', 'REV_SETT_2_REVOLVER', 'REV_SETT_3_REVOLVER', 'REV_SETT_4_REVOLVER', 'REV_SETT_5_REVOLVER', 'REV_SETT_6_REVOLVER']
    
    df_3_spend = data[spend_columns]
    df_3_pay = data[pay_columns]
    df_3_set = data[settler_columns]
    df_3_rev = data[revolver_columns]
    
    data['SPENDING_MONTHS'] = (df_3_spend>0).sum(axis=1)
    data['PAYMENT_MONTHS'] = (df_3_pay>0).sum(axis=1)
    
    data['MONTHS_SINCE_LAST_SPEND'] = df_3_spend.gt(0).idxmax(axis=1).apply(lambda x: int(x.split('_')[-1]) - 1)
    data['MONTHS_SINCE_LAST_SPEND'] = data['MONTHS_SINCE_LAST_SPEND'].where(df_3_spend.gt(0).any(axis=1), len(spend_columns))
    
    data['MONTHS_SINCE_LAST_PAY'] = df_3_pay.gt(0).idxmax(axis=1).apply(lambda x: int(x.split('_')[-1]) - 1)
    data['MONTHS_SINCE_LAST_PAY'] = data['MONTHS_SINCE_LAST_PAY'].where(df_3_pay.gt(0).any(axis=1), len(pay_columns))
    
    data['MONTHS_SINCE_LAST_SETTLER'] = df_3_set.gt(0).idxmax(axis=1).apply(lambda x: int(x.split('_')[2]) - 1)
    data['MONTHS_SINCE_LAST_SETTLER'] = data['MONTHS_SINCE_LAST_SETTLER'].where(df_3_set.gt(0).any(axis=1), len(settler_columns))
    
    data['MONTHS_SINCE_LAST_REVOLVER'] = df_3_rev.gt(0).idxmax(axis=1).apply(lambda x: int(x.split('_')[2]) - 1)
    data['MONTHS_SINCE_LAST_REVOLVER'] = data['MONTHS_SINCE_LAST_REVOLVER'].where(df_3_rev.gt(0).any(axis=1), len(revolver_columns))

    return data
        

    