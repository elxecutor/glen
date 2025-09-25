
# Fashion & Makeup Recommendation System

A Python-based recommendation system that suggests makeup looks, jewelry, and accessories based on fashion survey data. Uses fuzzy matching to provide personalized recommendations for events and outfits.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Overview](#file-overview)
- [Data](#data)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Personalized Recommendations**: Get makeup and accessory suggestions based on your age, event type, vibe, outfit, and neckline
- **Fuzzy Matching**: Handles partial inputs and variations using intelligent string matching
- **Confidence Scoring**: Provides confidence levels for recommendations
- **Survey-Based**: Recommendations derived from real fashion survey data
- **Interactive CLI**: Easy-to-use command-line interface

## Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/elxecutor/glen.git
cd glen
pip install pandas
```

## Usage
Run the recommendation system:

```bash
python recommend.py
```

Follow the prompts to enter your:
- Age group
- Event type
- Desired vibe
- Outfit type
- Neckline shape

The system will provide recommendations with confidence scores.

Example output:
```
=== Your Recommendations (Confidence: 52%) ===
• Makeup Look: Clear Gloss, Lip Liner + Gloss
• Earrings: Small Studs
• Necklace: Pendant Necklace
• Bracelets: Beaded Bracelets
• Other Accessories: Rings, Hair Clips/Bands

Based on similar users in our survey data! ✨
```

## File Overview
- `recommend.py` - Main recommendation engine with fuzzy matching
- `clean_data.py` - Data cleaning and preprocessing script
- `cleaned_survey_data.csv` - Processed survey data
- `Fashion + Makeup Choices Survey 🎀 .csv` - Raw survey data

## Data
The system uses anonymized survey data from fashion and makeup preferences. The dataset includes responses about makeup choices, jewelry preferences, and accessory selections for various events and outfits.

## Contributing
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) for details.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For questions or support, please open an issue or contact the maintainer via [X](https://x.com/elxecutor/).
