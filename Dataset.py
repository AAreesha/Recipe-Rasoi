import pandas as pd

# Load the Excel file
file_path = 'NLP Dataset.xlsx'  # Change this to your file path
excel_file = pd.ExcelFile(file_path)

# Create an empty DataFrame to hold combined data
combined_data = pd.DataFrame()

# Loop through each sheet in the Excel file
for sheet_name in excel_file.sheet_names:
    # Read the sheet into a DataFrame
    sheet_data = excel_file.parse(sheet_name)
    
    # Add a new column to identify the category
    sheet_data['Category'] = sheet_name
    
    # Append the sheet data to the combined DataFrame
    combined_data = pd.concat([combined_data, sheet_data], ignore_index=True)

# Save the combined data to a new Excel file
combined_file_path = 'combined_data.xlsx'  # Change this to your desired output file path
combined_data.to_excel(combined_file_path, index=False)
