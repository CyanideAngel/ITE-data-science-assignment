import pandas as pd

# Using the pre-calculated visitor interest map from the recommend_exhibitors_by_answers.ipynb
visitor_interest_map = {
    "Travel Agent": "Travel Agencies",
    "Event management": "MICE",
    "Tour Operator": "Tour Operators",
    "IT solutions for travel industry": "Travel Tech",
    "Accommodation Provider": "Hotels & Stays",
    "Media": "Media",
    #"Sales": "" 
    #"Formation of tourist products": "" 
    "Visa support": "Tour Operators", # inferred from above analysis
    "Guided tour services": "Travel Agencies", # inferred from above analysis
    "Marketing": "Travel Agencies" # inferred from above analysis
}

def fetch_unique_categories(x):
    category_list = x['interest_category'].tolist()
    category_set = set(category_list)
    category_set.discard("") # Discarding empty strings, if we didn't find any match in the interest mapping
    return category_set

def map_visitor_interests(visitor_data):
    """
    Given visitor_data, use their answers, mapped with the above dictionary to find unique categories of interest per visitor
    """
    # mapping interests
    visitor_data['interest_category'] = visitor_data['answer'].apply(lambda x: visitor_interest_map.get(x, ""))

    # refining unique categories based on visitor interest
    visitor_interested_categories = visitor_data.groupby(['visitorId', 'email']).apply(lambda x: fetch_unique_categories(x)).reset_index(name='interest_category_list')
    
    return visitor_interested_categories