
import csv
import openai

print("This line will be printed.")

with open('allowable_values_full_112.csv', mode ='r') as file:
       csvFile = csv.DictReader(file)
       for lines in csvFile:
            print(lines)

openai.api_key = 'test'

