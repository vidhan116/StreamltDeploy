##Impoting Libraries

import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO
from datetime import datetime
import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Selecting Client timesheet
st.header("Apexon projects employee timesheet conversion automation platform.")
st.title("Convert time sheets(excel, csv file) to Nest standard format.")

## AIRBUS CLIENT TIMESHEET

# Define the paths for bridge files and log file
airbus_bridge_file = 'Employee master/AirBus bridge file.xlsx'
log_file_path = 'LogFolder/AirBusLog_file.txt'

# Sidebar select box for project selection
project = st.sidebar.selectbox("Select Project", ("--Select--", "Airbus", "Ford"))


# Initialize log file
def initialize_log():
    with open(log_file_path, 'w') as log_file:
        log_file.write('Log File\n\n')


# Function to update log file
def update_log(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')


# Function to process timesheets

def process_timesheets(bridge_df, project_name, input_file):
    result_df = pd.DataFrame(
        columns=['SlNo', 'Project Name', 'Date_of_Work', 'Hours', 'Description', 'Is_Billable', 'Unique Employee ID'])

    for uploaded_file in input_file:
        if uploaded_file is not None:
            workbook = openpyxl.load_workbook(BytesIO(uploaded_file.read()), data_only=True)
            timesheet_found = False
            employee_found = False

            for sheetname in workbook.sheetnames:
                sheet = workbook[sheetname]

                if sheet['B6'].value == 'Name':
                    timesheet_found = True
                    employee_name = sheet['D6'].value

                    employee_row = bridge_df[bridge_df['EmployeeName'] == employee_name]
                    if not employee_row.empty:
                        employee_found = True
                        emp_id = employee_row['EmpID'].values[0]

                        if sheet['F11'].value == 'Date' and sheet['G11'].value == 'Hours':
                            temp_df = pd.DataFrame(
                                columns=['SlNo', 'Project Name', 'Date_of_Work', 'Hours', 'Description', 'Is_Billable',
                                         'Unique Employee ID'])
                            for row in range(12, 43):
                                work_date = sheet[f'F{row}'].value
                                hours = sheet[f'G{row}'].value
                                if work_date and hours:
                                    temp_df = pd.concat([temp_df, pd.DataFrame([{
                                        'SlNo': len(result_df) + len(temp_df) + 1,
                                        'Project Name': project_name,
                                        'Date_of_Work': work_date,
                                        'Hours': hours,
                                        'Description': 'Approved',
                                        'Is_Billable': 'YES',
                                        'Unique Employee ID': emp_id
                                    }])], ignore_index=True)
                            result_df = pd.concat([result_df, temp_df], ignore_index=True)
                        else:
                            update_log(f'{uploaded_file.name}: F11 or G11 does not contain the expected headers.')
                    else:
                        update_log(
                            f'{uploaded_file.name}: Employee {employee_name} not found in {project_name} bridge file.')

                    break

            if not timesheet_found:
                update_log(f'{uploaded_file.name}: Timesheet not found.')
            elif not employee_found:
                update_log(f'{uploaded_file.name}: Employee not found.')

    return result_df


# Main function to execute the app
def main():
    initialize_log()
    if project == "Airbus":

        input_file = st.file_uploader("Upload AirBus project employee timesheet files.", type='XLSX',
                                      accept_multiple_files=True)
        airbus_bridge_df = pd.read_excel(airbus_bridge_file)
        result_df = process_timesheets(airbus_bridge_df, "Airbus", input_file)

        # Save result to CSV
        result_csv_path = 'OutputResultFolder/AirBus_result.csv'
        result_df.to_csv(result_csv_path, encoding='utf-8', index=False)

        # Display results and download link
        generate_result = st.button('Click here to generate AirBus output result')
        if generate_result:
            st.write(result_df)
        download = st.download_button(
            label="Download AirBus Result CSV",
            data=open(result_csv_path, 'rb').read(),
            file_name='AirBus_result.csv',
            mime='text/csv'
        )

        # Display log and download link
        st.download_button(
            label="Download AirBus log txt",
            data=open(log_file_path, 'rb').read(),
            file_name='AirBusLog_file.txt',
            mime='text/csv'
        )
    ##++++++++++++++++++++++++++++++++++++++++++++++++++++++++FORD PROJECT INITIATION++++++++++++++++++++++++++++++++++++++++++++++++
    elif project == "Ford":
        # Read the input CSV file
        input_file = st.file_uploader("Upload Ford project employee timesheet files.", type='CSV')
        if input_file:
            df = pd.read_csv(input_file)

            # Extract the required columns
            columns_to_extract = ['File Id', 'Timesheet Status', 'Candidate Name', 'Work Date', 'Hours', 'Work Task']
            extracted_df = df[columns_to_extract]

        # File paths
        # output_csv = 'FilteredDataFolder/Filtered_data.csv'
        ford_excel = 'Employee master/Ford Client Details.xlsx'
        Ford_result_csv = 'OutputResultFolder/Output_result.csv'

        # st.write("Click on submit to generate Output result file")
        submit = st.button("Click here to generate output result.")

        if submit:
            # Read the Ford client details Excel file
            ford_df = pd.read_excel(ford_excel)

            # Merge the dataframes on File Id
            merged_df = pd.merge(extracted_df, ford_df[['File Id', 'EmpID']], on='File Id', how='inner')

            # Filter rows based on conditions
            filtered_df = merged_df[
                (merged_df['Work Task'] != 'NBILL') &
                (merged_df['Work Date'].notna()) &
                (merged_df['Hours'].notna()) &
                (merged_df['Hours'] != 0)
                ]

            # Create the result dataframe with the specified columns
            result_df = pd.DataFrame({
                'SlNo': range(1, len(filtered_df) + 1),
                'Project Name': 'FORD MAGNIT',
                'Date_of_Work': filtered_df['Work Date'],
                # 'Date_of_Work': filtered_df[formatted_date],
                'Hours': filtered_df['Hours'],
                'Description': filtered_df['Timesheet Status'],
                'Is_Billable': 'YES',
                'Unique Employee ID': filtered_df['EmpID']
            })

            # Write the result to a CSV file
            result_df.to_csv(Ford_result_csv, encoding='utf-8', index=False)

            # Display results and download link
            st.write(result_df)
            st.download_button(
                label="Download Ford Result CSV",
                data=open(Ford_result_csv, 'rb').read(),
                file_name='Ford_result.csv',
                mime='text/csv'
            )

            print(f"Resulting CSV file has been created: {Ford_result_csv}")

        ##+++++++++++++++++++++++++++++++++GENERATING LOG FILES+++++++++++++++++++++++++++++++++++++++++++++++
        # st.write("Click on Generate log file to create log")

        Generate_LogFile = st.button("Click here to generate log file.")

        if Generate_LogFile:
            # File paths
            log_csv = 'LogFolder/Log_file.csv'

            # Read the Ford client details Excel file
            ford_df = pd.read_excel(ford_excel)
            # Merge the dataframes on File Id
            lmerged_df = pd.merge(extracted_df, ford_df[['File Id', 'EmpID']], on='File Id', how='inner')

            # Filter rows based on conditions
            logged_df = lmerged_df[
                (lmerged_df['Work Task'] == 'NBILL') |
                (lmerged_df['Work Date'].isna()) |
                (lmerged_df['Hours'].isna()) |
                (lmerged_df['Hours'] == 0)
                ]

            # Create the result dataframe with the specified columns
            log_df = pd.DataFrame({
                'SlNo': range(1, len(logged_df) + 1),
                'Project Name': 'FORD MAGNIT',
                'Date_of_Work': logged_df['Work Date'],
                'Hours': logged_df['Hours'],
                'Description': logged_df['Timesheet Status'],
                'Is_Billable': 'YES',
                'Unique Employee ID': logged_df['EmpID'],
                'Work Tasks': logged_df['Work Task']
            })

            # Write the result to a CSV file
            log_df.to_csv(log_csv, encoding='utf-8', index=False)
            # Display logs and download link
            st.write(log_df)
            st.download_button(
                label="Download Ford log file",
                data=open(log_csv, 'rb').read(),
                file_name='Ford_logfile.csv',
                mime='text/csv'
            )

            print(f"Resulting CSV file has been created: {log_csv}")
            # st.write(" Log file has been generated successfully in the respective folder")





        else:
            st.write("Please upload timesheet files and select a project.")

        ##++++++++++++++++++++++++++++++++++++++++++++Ford process Ends+++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    else:
        st.write("Please select a project & upload timesheet files.")


if __name__ == "__main__":
    main()