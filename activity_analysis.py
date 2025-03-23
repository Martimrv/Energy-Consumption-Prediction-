import pandas as pd
from datetime import datetime
from rich.table import Table
from rich.console import Console

# Initialize the console
console = Console()

def process_activity_data(df):
    """Process activity data to extract relevant information."""
    # Convert timestamp to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Calculate end time (start time + duration)
    df['end_timestamp'] = df.apply(lambda row: row['Time'] + pd.Timedelta(hours=1), axis=1)
    
    # Format timestamps as strings
    df['start_datetime'] = df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['end_datetime'] = df['end_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    return df

def display_activity_data(df):
    """Display activity data in a formatted table."""
    # Process the data
    processed_df = process_activity_data(df)
    
    # Create a formatted table with only essential columns
    table = Table(title="Activity Data")
    table.add_column("Index", style="cyan")
    table.add_column("Start DateTime", style="green")
    table.add_column("End DateTime", style="green")
    table.add_column("Energy Usage", style="yellow")
    
    # Add rows to the table
    for idx, row in processed_df.iterrows():
        table.add_row(
            str(idx),
            row['start_datetime'],
            row['end_datetime'],
            str(row['qps_power.e_usage'])
        )
    
    console.print(table)

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv('C:/Users/marti/OneDrive/Desktop/3rd Year/ML Research/Energy-data-2025-03-22 16_47_12.csv', 
                     skiprows=1,
                     names=['Time', 'qps_power.e_usage'])
    
    # Process the data
    processed_df = process_activity_data(df)
    
    # Select and rename columns for the new CSV
    output_df = processed_df[['start_datetime', 'end_datetime', 'qps_power.e_usage']]
    output_df.columns = ['Start_DateTime', 'End_DateTime', 'Energy_Usage']
    
    # Save to new CSV file
    output_file = 'processed_energy_data.csv'
    output_df.to_csv(output_file, index=False)
    print(f"\nProcessed data saved to {output_file}")
    
    # Display the data
    display_activity_data(df)

