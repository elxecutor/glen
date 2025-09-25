import pandas as pd

# Load the data
df = pd.read_csv('/home/atsuomi/Documents/projects/glen/Fashion + Makeup Choices Survey 🎀 .csv')

# Drop unnecessary columns
df = df.drop(columns=['Timestamp', '  Do trends influence your choices?  ', '  Would you like a machine/AI to recommend accessories & makeup for you?  ', 'Where are you located?'])

# Clean column names: strip spaces and standardize
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('?', '').str.replace('(', '').str.replace(')', '').str.replace('/', '_').str.replace('🎀', '')

# Strip whitespace from all string columns
for col in df.select_dtypes(include=['object']):
    df[col] = df[col].str.strip()

# Handle missing values
# For features, fill with 'Unknown'
feature_cols = ['age_group', 'what_type_of_event_are_you_going_for', 'what_kind_of_vibe_are_you_going', 'what_outfit_are_you_wearing', 'outfit_neckline_shape']
for col in feature_cols:
    df[col] = df[col].fillna('Unknown')

# For targets (accessories), fill with 'None'
target_cols = ['what_type_of_earrings_would_you_wear', 'what_kind_of_necklace_would_you_wear', 'what_kind_of_bracelets_hand_accessories']
for col in target_cols:
    df[col] = df[col].fillna('None')

# For multi-select makeup and other accessories, fill with empty string or 'None'
df['what_makeup_look_do_you_usually_pick_for_this_situation_select_all_that_apply'] = df['what_makeup_look_do_you_usually_pick_for_this_situation_select_all_that_apply'].fillna('')
df['other_accessories_optional_select_all_that_apply'] = df['other_accessories_optional_select_all_that_apply'].fillna('')

# Remove any rows that are completely empty (though unlikely)
df = df.dropna(how='all')

# Remove duplicates if any
df = df.drop_duplicates()

# Perhaps standardize some text, like lowercase for consistency
for col in df.select_dtypes(include=['object']):
    df[col] = df[col].str.lower()

# But keep original casing for readability, or adjust as needed
# Actually, for ML, casing doesn't matter, but for output, perhaps keep.

# Save cleaned data
df.to_csv('/home/atsuomi/Documents/projects/glen/cleaned_survey_data.csv', index=False)

print(f"Cleaned data saved. Shape: {df.shape}")
print("Missing values after cleaning:")
print(df.isnull().sum())