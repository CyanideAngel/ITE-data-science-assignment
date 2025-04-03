import pandas as pd

def parse_exhibitor_data(exhibitors_df, categories_df):
    """
    - takes raw exhibitors dataframe with concatenated categories using '|' symbol. need to explode this
    - map categories based on categoryId
    """
    # fixing the id column first
    exhibitors_df.rename({'exhibitorid': 'exhibitorId'}, axis=1, inplace=True) # To standardize column names

    # For the join on categoryId later on, need to typecast this to string as well
    categories_df['categoryId'] = categories_df['categoryId'].astype(str)
    
    # split pipe-separated string into list
    exhibitors_df['category_list'] = exhibitors_df['MainCategories'].apply(lambda x: x.split('|'))

    # explode the category list to each row
    exploded_exhibitors = exhibitors_df.explode('category_list').drop('MainCategories', axis=1)
    exploded_exhibitors.rename({"category_list": 'categoryId'}, axis=1, inplace=True)

    # mapping categories using categoryId
    exhibitor_data = exploded_exhibitors.merge(categories_df, on='categoryId', how='inner')

    return exhibitor_data
