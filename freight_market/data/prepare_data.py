import pandas as pd
import csv
import os

ZIP3_MAPPING = {
    "900": {"city": "Los Angeles", "state": "CA", "region": "West"},
    "606": {"city": "Chicago", "state": "IL", "region": "Midwest"},
    "100": {"city": "New York", "state": "NY", "region": "Northeast"},
    "750": {"city": "Dallas", "state": "TX", "region": "South"},
    "770": {"city": "Atlanta", "state": "GA", "region": "Southeast"},
    "303": {"city": "Denver", "state": "CO", "region": "Mountain"},
    "981": {"city": "Seattle", "state": "WA", "region": "West"},
    "331": {"city": "Miami", "state": "FL", "region": "Southeast"},
    "191": {"city": "Philadelphia", "state": "PA", "region": "Northeast"},
    "850": {"city": "Phoenix", "state": "AZ", "region": "West"},
    "381": {"city": "Memphis", "state": "TN", "region": "Southeast"},
    "941": {"city": "San Francisco", "state": "CA", "region": "West"},
    "482": {"city": "Detroit", "state": "MI", "region": "Midwest"},
    "021": {"city": "Boston", "state": "MA", "region": "Northeast"},
    "802": {"city": "Burlington", "state": "VT", "region": "Northeast"},
    "554": {"city": "Minneapolis", "state": "MN", "region": "Midwest"},
    "462": {"city": "Indianapolis", "state": "IN", "region": "Midwest"},
    "282": {"city": "Charlotte", "state": "NC", "region": "Southeast"},
    "641": {"city": "Kansas City", "state": "MO", "region": "Midwest"},
    "432": {"city": "Columbus", "state": "OH", "region": "Midwest"},
    "212": {"city": "New York", "state": "NY", "region": "Northeast"},
    "972": {"city": "Dallas", "state": "TX", "region": "South"},
    "372": {"city": "Nashville", "state": "TN", "region": "Southeast"},
    "441": {"city": "Cleveland", "state": "OH", "region": "Midwest"},
    "336": {"city": "Greensboro", "state": "NC", "region": "Southeast"},
}

def create_zip3_mapping():
    """Create CSV file mapping zip3 codes to states and regions"""
    with open('zip3_mapping.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['zip3', 'city', 'state', 'region'])
        
        for zip3, info in sorted(ZIP3_MAPPING.items()):
            writer.writerow([zip3, info['city'], info['state'], info['region']])
    
    print("Created: zip3_mapping.csv")
    print(f"Total zip3s mapped: {len(ZIP3_MAPPING)}")


def organize_dat_data():
    """Combine all DAT files into one master reference table"""
    
    dat_files = [
        'Spot_Flatbeds_Region_30.csv',
        'Spot_Flatbeds_Region_30_Fuel.csv',
        'Spot_Flatbeds_State_30.csv',
        'Spot_Flatbeds_State_30_Fuel.csv',
        'Spot_Reefers_Region_30.csv',
        'Spot_Reefers_Region_30_Fuel.csv',
        'Spot_Reefers_State_30.csv',
        'Spot_Reefers_State_30_Fuel.csv',
        'Spot_Vans_Region_30.csv',
        'Spot_Vans_Region_30_Fuel.csv',
        'Spot_Vans_State_30.csv',
        'Spot_Vans_State_30_Fuel.csv'
    ]
    
    all_data = []
    
    for file in dat_files:
        if not os.path.exists(file):
            print(f"Skipping: {file} (not found)")
            continue
            
        print(f"Processing: {file}")
        
        parts = file.replace('.csv', '').split('_')
        equipment = parts[1].lower()
        geography = parts[2].lower()
        fuel_included = 'Fuel' in file
        
        try:
            df = pd.read_csv(file, header=1)
            
            origin_col = df.columns[0]
            
            for idx, row in df.iterrows():
                origin = row[origin_col]
                if pd.isna(origin):
                    continue
                    
                for dest in df.columns[1:]:
                    rate = row[dest]
                    if pd.isna(rate):
                        continue
                    
                    all_data.append({
                        'equipment': equipment,
                        'geography': geography,
                        'fuel_included': fuel_included,
                        'origin': str(origin).strip(),
                        'destination': str(dest).strip(),
                        'rate': float(rate)
                    })
                    
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
            continue
    
    if all_data:
        master_df = pd.DataFrame(all_data)
        master_df.to_csv('DAT_master_reference.csv', index=False)
        print(f"\nCreated: DAT_master_reference.csv")
        print(f"Total rate records: {len(master_df):,}")
        
        summary = master_df.groupby(['equipment', 'geography', 'fuel_included']).size().reset_index(name='count')
        summary.to_csv('DAT_summary.csv', index=False)
        print(f"Summary saved: DAT_summary.csv")
        
        return master_df
    else:
        print("No DAT data processed")
        return None

def clean_mpact_data():
    """Filter and clean MPACT data, adding state mapping"""
    
    mpact_filename = 'mpact_rates.csv'
    
    if not os.path.exists(mpact_filename):
        print(f"MPACT file not found: {mpact_filename}")
        print("Please ensure mpact_rates.csv is in the current directory.")
        return None
    
    print(f"Loading MPACT data from: {mpact_filename}")
    
    try:
        mpact_df = pd.read_csv(mpact_filename)
        print(f"Original MPACT data shape: {mpact_df.shape}")
        
        filters_applied = []
        
        if 'include_fuel' in mpact_df.columns:
            mpact_df = mpact_df[mpact_df['include_fuel'] == True]
            filters_applied.append("include_fuel = True")
        
        if 'days_window' in mpact_df.columns:
            mpact_df = mpact_df[mpact_df['days_window'] <= 45]
            filters_applied.append("days_window ≤ 45")
        
        if 'orders' in mpact_df.columns:
            mpact_df = mpact_df[mpact_df['orders'] >= 5]
            filters_applied.append("orders ≥ 5")
        
        print(f"Filters applied: {', '.join(filters_applied)}")
        print(f"Cleaned shape: {mpact_df.shape}")
        
        zip3_map = pd.read_csv('zip3_mapping.csv')
        state_dict = dict(zip(zip3_map['zip3'], zip3_map['state']))
        
        mpact_df['origin_zip3_str'] = mpact_df['origin_zip3'].astype(str)
        mpact_df['destination_zip3_str'] = mpact_df['destination_zip3'].astype(str)
        
        mpact_df['origin_state'] = mpact_df['origin_zip3_str'].map(state_dict)
        mpact_df['destination_state'] = mpact_df['destination_zip3_str'].map(state_dict)
        
        unmapped_orig = mpact_df[mpact_df['origin_state'].isna()]['origin_zip3'].unique()
        unmapped_dest = mpact_df[mpact_df['destination_state'].isna()]['destination_zip3'].unique()
        
        if len(unmapped_orig) > 0:
            print(f"Unmapped origin zip3s: {unmapped_orig}")
        if len(unmapped_dest) > 0:
            print(f"Unmapped destination zip3s: {unmapped_dest}")
        
        mpact_df.to_csv('mpact_cleaned.csv', index=False)
        print(f"\nCreated: mpact_cleaned.csv")
        
        summary_stats = {
            'total_records': len(mpact_df),
            'unique_origins': mpact_df['origin_zip3'].nunique(),
            'unique_destinations': mpact_df['destination_zip3'].nunique(),
            'unique_lanes': mpact_df[['origin_zip3', 'destination_zip3']].drop_duplicates().shape[0],
        }
        
        if 'orders' in mpact_df.columns:
            summary_stats['avg_orders'] = mpact_df['orders'].mean()
        
        if 'average' in mpact_df.columns:
            summary_stats['avg_rate'] = mpact_df['average'].mean()
        
        with open('mpact_summary.txt', 'w') as f:
            for key, value in summary_stats.items():
                f.write(f"{key}: {value}\n")
        
        print(f"Summary saved: mpact_summary.txt")
        
        return mpact_df
        
    except Exception as e:
        print(f"Error cleaning MPACT data: {str(e)}")
        return None

def main():
    print("=" * 60)
    print("PORTFOLIO DATA PREPARATION")
    print("=" * 60)
    
    print("\nSTEP 1.1: Creating Zip3 to State Mapping...")
    create_zip3_mapping()
    
    print("\nSTEP 1.2: Organizing DAT Data...")
    dat_master = organize_dat_data()
    
    print("\nSTEP 1.3: Cleaning MPACT Data...")
    mpact_cleaned = clean_mpact_data()
    
    print("\n" + "=" * 60)
    print("DATA PREPARATION COMPLETE")
    print("=" * 60)
    print("\nOutput Files Created:")
    print("1. zip3_mapping.csv - Zip3 to state mapping")
    print("2. DAT_master_reference.csv - All DAT rates consolidated")
    print("3. DAT_summary.csv - DAT data summary")
    print("4. mpact_cleaned.csv - Filtered MPACT data")
    print("5. mpact_summary.txt - MPACT data summary")

if __name__ == "__main__":
    main()