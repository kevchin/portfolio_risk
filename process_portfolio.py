import csv

def filter_and_rewrite_csv(input_file, output_file, column_name):
    """
    Reads a CSV file, retains rows with a value in the specified column,
    and writes the result to a new CSV file.
    """
    with open(input_file, 'r', newline='') as infile, \
         open(output_file, 'w', newline='') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read the header
        header = next(reader)
        writer.writerow(header)
        
        # Find the index of the column to check
        try:
            column_index = header.index(column_name)
        except ValueError:
            print(f"Error: Column '{column_name}' not found in the CSV file.")
            return
            
        # Process the remaining rows
        for row in reader:
            # Check if the row has enough columns and the target column is not empty
            if len(row) > column_index and row[column_index].strip():
                writer.writerow(row)

if __name__ == "__main__":
    input_csv = 'Portfolio_Positions_Nov-09-2025.csv'
    output_csv = 'portfolio.csv'
    column_to_check = 'Last Price'
    filter_and_rewrite_csv(input_csv, output_csv, column_to_check)
    print(f"Filtered data from '{input_csv}' has been written to '{output_csv}'.")
