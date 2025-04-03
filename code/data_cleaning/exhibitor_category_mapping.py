import pandas as pd

# Using the pre-populated category name mapping from the exhibitors_profile_analysis.ipynb
category_class_names = {
    "1": "Hotels & Stays",
    "2": "Tour Operators",
    "3": "Travel Agencies",
    "4": "Online Travel",
    "5": "Transport",
    "6": "Cars & Motorhomes",
    "7": "Glamping",
    "8": "Healthcare",
    "9": "Hotel Supplies",
    "10": "Parks",
    "11": "MICE",
    "12": "Tourism Offices",
    "13": "Travel Tech",
    "14": "Special Interest Travel",
    "15": "Media",
    "16": "Real Estate",
    "17": "Finance"
}


# cleaning the category name, as it has index and sub-index as prefix
def clean_category_name(x):
    full_class = x.split(' ')[0] # getting the category and subcategory
    just_name = ' '.join(x.split(' ')[1:]) # getting the name
    main_class = full_class.split('.')[0] # getting just the category
    sub_class = full_class.split('.')[1] # getting just the sub category
    
    return main_class, sub_class, just_name


def map_exhibitor_category(exhibitor_data):
    """
    Given exhibitor_data, use their category names, mapped with the above dictionary to find borad categories offered by the exhibitor
    """
    # fetching categories
    exhibitor_data[['category_class', 'subcategory_class', 'category']] = exhibitor_data['categoryName'].apply(lambda x: pd.Series(clean_category_name(x)))

    # refining category name to category class
    exhibitor_data['category_class_name'] = exhibitor_data['category_class'].apply(lambda x: category_class_names[str(x)])

    exhibitor_data.drop(["categoryName", "category_class", "subcategory_class"], axis=1, inplace=True)
    
    return exhibitor_data