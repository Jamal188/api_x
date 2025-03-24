import pandas as pd

# Input CSV file
input_csv = input("csv file name: ")

# Output Excel file
output_excel = input("the output name: *.xlsx")

# Read the CSV file into a DataFrame
df = pd.read_csv(input_csv, encoding="utf-8")

# Save the DataFrame to an Excel file
df.to_excel(output_excel, index=False, engine="openpyxl")

print(f"CSV file '{input_csv}' has been converted to Excel file '{output_excel}'.")

