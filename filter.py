import csv

# Path to the input and output CSV files
input_file = 'results.csv'
output_file = 'results_unique.csv'

# Read data from the input CSV and remove duplicates
def remove_duplicates(input_file, output_file):
    unique_rows = {}
    
    # Read the input CSV file
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        
        # Collect unique rows based on the admission_number
        for row in reader:
            admission_number = row['admission_number']
            if admission_number not in unique_rows:
                unique_rows[admission_number] = row
    
    # Write unique rows to the output CSV file
    with open(output_file, mode='w', newline='') as outfile:
        fieldnames = ['admission_number', 'name', 'gender', 'stream', 'school', 'total_score', 'subject_scores']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in unique_rows.values():
            writer.writerow(row)

# Call the function
remove_duplicates(input_file, output_file)

print(f"Unique data has been written to {output_file}")
