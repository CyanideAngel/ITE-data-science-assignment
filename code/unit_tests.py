import pytest

###################
# to run the unit tests, simply type pytest unit_tests.py, it will run each function with a 'test' substring in the function name
# other functions, apart from modularized functions are directly copied from notebooks, as I don't want to create additional modules for them (lack of time)
# modularized functions are just helper functions, to read data and transform data. I have already used them in my notebooks, guess, we can skip writing unit tests for them
###################

## testing scoring functions

def penalized_score(visitor_set, exhibitor_set):
    """
    Computes a penalized Jaccard similarity between two sets. Here, Jaccard similarity computes the similarity between two sets of strings.
    We want to penalize exhibitors who list too many categories, so we reduce their score separately. Lowest score is 0, if either of the sets are empty.
    """
    # reusing our category threshold from our exhibitor_profile_analysis.ipynb, where we declare the exhibitor_class to be spammy, if its higher than this number.
    category_threshold = 4

    # if either set is empty, nothing to score
    if not visitor_set or not exhibitor_set: 
        return 0.0

    intersection = visitor_set & exhibitor_set
    union = visitor_set | exhibitor_set
    jaccard = len(intersection) / len(union)

    # only penalize if exhibitor has more categories than category threshold
    if len(exhibitor_set) > category_threshold:
        penalty = 1/len(exhibitor_set)
    else:
        penalty = 1

    return jaccard * penalty

def matching_score(visitor_set, exhibitor_set):
    """
    Computes a Jaccard similarity between two sets. Here, Jaccard similarity computes the similarity between two sets of strings.
    Lowest score is 0, if either of the sets are empty.
    """
    # if either set is empty, nothing to score
    if not visitor_set or not exhibitor_set: 
        return 0.0

    intersection = visitor_set & exhibitor_set
    union = visitor_set | exhibitor_set
    jaccard = len(intersection) / len(union)

    return jaccard


#### unit tests for penalized_score() function

def test_penalized_score_standard():
    v = {"Travel", "Hotel"}
    e = {"Hotel", "Wellness"}
    score = penalized_score(v, e)
    expected_jaccard = 1 / 3  # overlap: 1, union: 3
    assert abs(score - expected_jaccard) < 1e-6

def test_penalized_score_with_penalty():
    v = {"A"}
    e = {"A", "B", "C", "D", "E", "F"}  # len > threshold (4) so apply penalty
    score = penalized_score(v, e)
    jaccard = 1 / 6
    penalty = 1 / 6
    assert abs(score - (jaccard * penalty)) < 1e-6

def test_penalized_score_empty_visitor():
    assert penalized_score(set(), {"X"}) == 0.0

def test_penalized_score_empty_exhibitor():
    assert penalized_score({"X"}, set()) == 0.0


#### unit tests for matching_score() function (slightly different tests than above, as its mostly same computation)

def test_matching_score_standard():
    v = {"A", "B"}
    e = {"B", "C"}
    expected = 1 / 3
    assert abs(matching_score(v, e) - expected) < 1e-6

def test_matching_score_no_overlap():
    s1 = {"A"}
    s2 = {"B"}
    assert matching_score(s1, s2) == 0.0

def test_matching_score_empty_sets():
    assert matching_score(set(), set()) == 0.0

## testing recommendation functions, by modifying them to take in the dictionaries as arguments, 
## instead of using them globally (as in the notebook)

def recommend_exhibitors(visitor_email, visitor_dict, exhibitor_dict, top_k=7):
    """
    Returns top_k matching exhibitors for a given visitor.
    Scores are based on category overlap with optional penalization.
    """
    # initializing empty exhibitor score dict    
    exhibitor_scores = dict()

    visitor_interest_set = set(visitor_dict.get(visitor_email, set()))

    for exhibitor_name, exhibitor_cats in exhibitor_dict.items():
        score = penalized_score(visitor_interest_set, exhibitor_cats)
        exhibitor_scores[exhibitor_name] = score

    # we want to rank exhibitors by their score (descending),
    ranked_exhibitors = sorted(exhibitor_scores.items(), key=lambda item: item[1], reverse=True) # sort by score in descending order

    return ranked_exhibitors[:top_k] # if the visitor has expressed no interest, they will receive random recommendations for exhibitors

def recommend_visitors(exhibitor_id, exhibitor_dict, visitor_dict, top_k=7):
    """
    Returns top_k matching visitors for a given exhibitor.
    Scores are based on category overlap.
    """
    # initializing empty visitor score dict    
    visitor_scores = dict()

    exhibitor_interest_set = set(exhibitor_dict.get(exhibitor_id, set()))

    for visitor_email, visitor_cats in visitor_dict.items():
        score = matching_score(visitor_cats, exhibitor_interest_set)
        visitor_scores[visitor_email] = score

    # we want to rank visitors by their score (descending),
    ranked_visitors = sorted(visitor_scores.items(), key=lambda item: item[1], reverse=True)  # sort by score in descending order

    return ranked_visitors[:top_k] 

#### preparing some mock dictionaries

mock_visitor_dict = {
    "a@xyz.com": {"Hotels & Stays", "Tour Operators"},
    "b@xyz.com": {"Finance", "Real Estate"},
    "c@xyz.com": set(),  # no interests
}

mock_exhibitor_dict = {
    101: {"Hotels & Stays", "Travel Agencies"},
    102: {"Finance", "Real Estate"},
    103: {"MICE", "Media"},
}


#### unit tests for both recommendation functions

def test_recommend_exhibitors_match_found():
    test_exhibitor_dict = {
        "E1": {"Hotels & Stays", "Travel Agencies"},
        "E2": {"Tour Operators"},
        "E2": {"Hotels & Stays", "Tour Operators", "Real Estate", "Media", "Finance"},
    }

    result = recommend_exhibitors("a@xyz.com", mock_visitor_dict, test_exhibitor_dict, top_k=2)

    assert isinstance(result, list) # testing result is a list
    assert len(result) == 2 # testing only top_k are returned
    assert result[0][1] >= result[1][1] # testing rank ordering
    assert all(isinstance(x[0], str) and isinstance(x[1], float) for x in result) # testing data types

def test_recommend_visitors_match_found():
    test_visitor_dict = {
        "V1": {"Finance", "MICE"},
        "V2": {"Real Estate"},
        "V3": {"Media"}
    }
    result = recommend_visitors(102, mock_exhibitor_dict, test_visitor_dict, top_k=2)

    assert isinstance(result, list) # testing result is a list
    assert len(result) == 2 # testing only top_k are returned
    assert result[0][1] >= result[1][1] # testing rank ordering
    assert result[0][0] in test_visitor_dict # testing if result is from test_visitor_dict


def test_recommend_exhibitors_no_interest():
    test_exhibitor_dict = {
        "E4": {"dummy"},
    }

    result = recommend_exhibitors("c@xyz.com", mock_visitor_dict, test_exhibitor_dict, top_k=1)

    assert result[0][1] == 0.0 # testing no interest

def test_recommend_visitors_empty_interest():
    test_visitor_dict = {
        "V4": {},
    }

    result = recommend_visitors(101, test_visitor_dict, mock_exhibitor_dict, top_k=1)

    assert result[0][1] == 0.0 # testing empty interest
