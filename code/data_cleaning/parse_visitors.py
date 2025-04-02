import pandas as pd
import json

def parse_visitor_data(visitors_df, answers_df, questions_df):
    """
    - takes raw visitors dataframe with packed JSON data column. need to explode this
    - use visitor answers and questions to join with visitor data
    - returns one row per (visitor_id, question, answer)
    """
    # parse the data column as a json
    visitors_df['parsed_data'] = visitors_df['data'].apply(lambda x : json.loads(x))

    # explode each answer row into multiple rows
    exploded_visitors = visitors_df.explode('parsed_data').drop("data", axis=1).copy()

    # extract all the key-value pairs from parsed_data
    exploded_visitors['stepId'] = exploded_visitors['parsed_data'].apply(lambda x: x.get('stepId'))
    exploded_visitors['questionId'] = exploded_visitors['parsed_data'].apply(lambda x: x.get('questionId'))
    exploded_visitors['answerValue'] = exploded_visitors['parsed_data'].apply(lambda x: x.get('answerValue'))
    exploded_visitors['answerId'] = exploded_visitors['parsed_data'].apply(lambda x: x.get('answerId'))
    exploded_visitors['answerTypeId'] = exploded_visitors['parsed_data'].apply(lambda x: x.get('answerTypeId'))

    # removing the parsed_data column as we have already extracted each field now.
    exploded_visitors.drop("parsed_data", axis=1, inplace=True)

    # join with answers + questions
    final_df = exploded_visitors.merge(answers_df, on=['answerId', 'questionId'], how='left').merge(questions_df, on=['questionId', 'stepId'], how='left')

    # cleaning the exploded join, with only valid questions from our question bank
    final_df = final_df[~final_df['question'].isnull()]

    return final_df
