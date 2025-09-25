import pandas as pd
from collections import Counter
from difflib import SequenceMatcher

# Load cleaned data
df = pd.read_csv('cleaned_survey_data.csv')

# Define all possible features
all_features = ['age_group', 'what_type_of_event_are_you_going_for', 'what_kind_of_vibe_are_you_going', 'what_outfit_are_you_wearing', 'outfit_neckline_shape']

# Define targets
targets = [
    'what_makeup_look_do_you_usually_pick_for_this_situation_select_all_that_apply',
    'what_type_of_earrings_would_you_wear',
    'what_kind_of_necklace_would_you_wear',
    'what_kind_of_bracelets_hand_accessories',
    'other_accessories_optional_select_all_that_apply'
]

# Function to get recommendations
def get_recommendations(user_inputs, k=5):
    # user_inputs is a dict of feature: value, only provided ones
    
    # Filter out 'under 18' if age not specified (assume adult preferences)
    filtered_df = df if 'age_group' in user_inputs else df[df['age_group'] != 'under 18']
    
    # Weight features by importance (age and event are most important)
    weights = {'age_group': 2, 'what_type_of_event_are_you_going_for': 2, 
               'what_kind_of_vibe_are_you_going': 1, 'what_outfit_are_you_wearing': 1, 
               'outfit_neckline_shape': 1}

    def get_similarity_score(val, row_val, weight):
        if not isinstance(row_val, str) or not row_val.strip():
            return 0
        val_lower = val.lower()
        row_lower = row_val.lower()
        
        # Check for substring match first
        if val_lower in row_lower or row_lower in val_lower:
            return weight * 0.75  # Good match for substrings
        
        # Otherwise, use fuzzy similarity
        similarity = SequenceMatcher(None, val_lower, row_lower).ratio()
        if similarity >= 0.9:  # very close
            return weight
        elif similarity >= 0.7:  # reasonable fuzzy match
            return weight * 0.6
        elif similarity >= 0.5:  # partial fuzzy
            return weight * 0.4
        else:
            return 0

    # Compute similarity scores for each row
    scores = []
    for idx, row in filtered_df.iterrows():
        score = 0
        for feat, val in user_inputs.items():
            score += get_similarity_score(val, row[feat], weights.get(feat, 1))
        scores.append((idx, score))

    # Sort by score descending, take top k with score > 0
    scores = [(idx, score) for idx, score in scores if score > 0]
    scores.sort(key=lambda x: x[1], reverse=True)
    
    if not scores:
        return None  # No matches found
        
    top_indices = [idx for idx, score in scores[:k]]
    max_score = scores[0][1]
    confidence = min(100, (max_score / len(user_inputs)) * 50)  # Rough confidence measure

    recommendations = {'confidence': f"{confidence:.0f}%"}

    # Better labels for output
    labels = {
        'what_makeup_look_do_you_usually_pick_for_this_situation_select_all_that_apply': 'Makeup Look',
        'what_type_of_earrings_would_you_wear': 'Earrings',
        'what_kind_of_necklace_would_you_wear': 'Necklace',
        'what_kind_of_bracelets_hand_accessories': 'Bracelets',
        'other_accessories_optional_select_all_that_apply': 'Other Accessories'
    }

    for target in targets:
        # Get the target values of top neighbors
        neighbor_targets = filtered_df.loc[top_indices, target]

        # For multi-select, split by comma and find most common
        if target in ['what_makeup_look_do_you_usually_pick_for_this_situation_select_all_that_apply', 'other_accessories_optional_select_all_that_apply']:
            all_items = []
            for val in neighbor_targets:
                if val and isinstance(val, str):
                    all_items.extend([item.strip() for item in val.split(',') if item.strip()])
            if all_items:
                most_common = Counter(all_items).most_common(2)  # Top 2 for cleaner output
                recommendations[labels[target]] = [item.title() for item, count in most_common]
            else:
                recommendations[labels[target]] = ['No preference']
        else:
            # For single select, most common
            most_common = Counter(neighbor_targets).most_common(1)
            rec = most_common[0][0] if most_common and most_common[0][0] != 'none' else 'No preference'
            recommendations[labels[target]] = rec.title() if rec != 'No preference' else rec

    return recommendations

# Example usage
if __name__ == "__main__":
    print("=== Fashion & Makeup Recommendation System ===\n")
    
    # Better prompts
    prompts = {
        'age_group': 'Age group',
        'what_type_of_event_are_you_going_for': 'Event type',
        'what_kind_of_vibe_are_you_going': 'Vibe you\'re going for',
        'what_outfit_are_you_wearing': 'Outfit you\'re wearing',
        'outfit_neckline_shape': 'Neckline shape'
    }
    
    user_inputs = {}
    for feat in all_features:
        val = input(f"{prompts[feat]}: ").strip()
        if val:
            user_inputs[feat] = val.lower()

    if not user_inputs:
        print("\nNo inputs provided, cannot make recommendations.")
    else:
        recs = get_recommendations(user_inputs)
        
        if recs is None:
            print("\nNo similar users found. Try providing different inputs.")
        else:
            confidence = recs.pop('confidence')
            print(f"\n=== Your Recommendations (Confidence: {confidence}) ===")
            for key, value in recs.items():
                if isinstance(value, list):
                    print(f"• {key}: {', '.join(value)}")
                else:
                    print(f"• {key}: {value}")
            print("\nBased on similar users in our survey data! ✨")