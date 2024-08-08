from datetime import datetime
import pandas as pd
import os
# Path to your FORD CSV file
if os.path.exists("OutputResultFolder/Ford_result.csv"):
    FORDfile_path = "OutputResultFolder/Ford_result.csv"  # Replace with the path to your CSV file
    # Path to your CSV file
    # file_path = "path/to/your/file.csv"  # Replace with the path to your CSV file

    # Load the CSV file into a DataFrame
    df = pd.read_csv(FORDfile_path)

    # Ensure 'Date_of_Work' column is in datetime format
    df['Date_of_Work'] = pd.to_datetime(df['Date_of_Work'], errors='coerce')

    # Convert the 'Date_of_Work' column to the desired format
    df['Date_of_Work'] = df['Date_of_Work'].dt.strftime("%d-%m-%Y")

    # Save the modified DataFrame back to a CSV file if needed
    df.to_csv("FormattedResultFolder/Ford_Outputfile.csv",encoding='utf-8', index=False)  # Replace with the desired output path
else:
    ('Ford result File Not Found')
##++++++++++++++++++++++++++++++++++++++++++++++++++AIRBUS+++++++++++++++++++++++++++++++++++++++++


# Path to your FORD CSV file
if os.path.exists("OutputResultFolder/AirBus_result.csv"):
    AirBusfile_path = "OutputResultFolder/AirBus_result.csv"  # Replace with the path to your CSV file

    # Path to your CSV file
    # file_path = "path/to/your/file.csv"  # Replace with the path to your CSV file

    # Load the CSV file into a DataFrame
    df = pd.read_csv(AirBusfile_path)

    # Ensure 'Date_of_Work' column is in datetime format
    df['Date_of_Work'] = pd.to_datetime(df['Date_of_Work'], errors='coerce')

    # Convert the 'Date_of_Work' column to the desired format
    df['Date_of_Work'] = df['Date_of_Work'].dt.strftime("%d-%m-%Y")

    # Save the modified DataFrame back to a CSV file if needed
    df.to_csv("FormattedResultFolder/AirBus_Outputfile.csv",encoding='utf-8', index=False)  # Replace with the desired output path
else:
    ("AirBus result File Not Found")

##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++ICON++++++++++++++++++++++++++++++++++++++++++++
if os.path.exists("OutputResultFolder/ICON_result.csv"):
    # Path to your FORD CSV file
    ICONfile_path = "OutputResultFolder/ICON_result.csv"  # Replace with the path to your CSV file

    # Path to your CSV file
    # file_path = "path/to/your/file.csv"  # Replace with the path to your CSV file

    # Load the CSV file into a DataFrame
    df = pd.read_csv(ICONfile_path)

    # Ensure 'Date_of_Work' column is in datetime format
    df['Date_of_Work'] = pd.to_datetime(df['Date_of_Work'], errors='coerce')

    # Convert the 'Date_of_Work' column to the desired format
    df['Date_of_Work'] = df['Date_of_Work'].dt.strftime("%d-%m-%Y")

    # Save the modified DataFrame back to a CSV file if needed
    df.to_csv("FormattedResultFolder/ICON_Outputfile.csv",encoding='utf-8', index=False)  # Replace with the desired output path
else:
    print("ICON result File Not Found")
##++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++





















