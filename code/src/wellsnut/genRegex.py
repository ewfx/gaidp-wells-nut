import pandas as pd
import re
from ydata_profiling import ProfileReport


#Function to apply Regex pattern to a specified column and filter the dataset
def filter_by_regex(data,field_name, regex_pattern):
    pattern = re.compile(regex_pattern)

    def is_valid(value):
        return bool(pattern.match(str(value)))

    if field_name not in data.columns:
        filtered_data = data[data[field_name].apply(is_valid)]
        return filtered_data
    else:
        print({field_name}, "not found in the dataset",data[field_name])
        return data





def mycall():
    #Load Dataset
    try:
        data = pd.read_csv("data.csv", delimiter=',', on_bad_lines='skip',encoding='utf-8')
        if data.empty:
            raise ValueError("The data file is empty. Please check its content.")
        else:
            print(data.head())
        patterns=pd.read_csv("rules.csv", delimiter=',', on_bad_lines='skip',encoding='utf-8')

        if patterns.empty:
            raise ValueError("The rules file is empty. Please check its content.")
        else:
            for index, row in patterns.iterrows():
                column = row['field_name']
                pattern = row['expressionRegex']
                if column not in data.columns:
                    data = filter_by_regex(data, column, pattern)
            if 'field_name' not in patterns.columns or 'expressionRegex' not in patterns.columns:
                raise ValueError("The CSV file must contain 'field_name' and expressionRegex columns.")
            #save the rules applied data in genProfileData.csv
            data.to_csv("result.csv", index=False)
            # Generate report
            profile = ProfileReport(data, explorative=True)
            profile.to_file("data_profile_report.html")
    except FileNotFoundError as e:
        print(f"Error: {e}")
mycall()