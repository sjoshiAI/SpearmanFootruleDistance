import pandas as pd

def scoresToRanks(scores):
    """returns a set of ranks based on the given scores for each measurement.
    :param score: dictionary of tuple where key is itemId and tuple contains scores by different metrics.

    :return: A pandas dataframe with ranks generated from each metric in a column.

    e.g scores = {'A' : (100,0.1),
          'B' : (90,0.3),
          'C' : (20, 0.2)}

        returns dataframe      Index     metric_0    metric_1
                               A            1           3
                               B            2           1
                               C            3           2

    """
    n_items = len(scores)
    if n_items:     # Check if scores is non-empty
        df = pd.DataFrame.from_dict(scores,orient='index')   # Using pandas to handle cases with huge number of entries
        df.columns = ['metric_'+ str(col) for col in df.columns]
        ranks = []
        for col in df.columns:
            df.sort_values(by=col,ascending=False,inplace=True) # Sort the index by the selected column
            df['rank'] = range(1,df.shape[0]+1) # Assign the ranks in descending order

            if df[col].nunique() != df.shape[0]: # check if all the scores are different i.e no collisions
                df[col] = df.groupby(col)['rank'].transform('min')
            else:
                df[col] = range(1,df.shape[0]+1)

            df.drop('rank',axis=1,inplace=True)
    else:
        raise Exception("Sorry, no scores are provided.")
    return df


def sumSpearmanDistances(scores, proposedRank):
    """Calculates spearman footrule distance between the
        proposed rank and the multiset of ranks generated by scores.

        :param scores:
        :param proposedRank:

        :return: sum of spearman distance i.e an integer

        e.g scores = {'A' : (100,0.1),
              'B' : (90,0.3),
              'C' : (20, 0.2)}
        proposedRank = {'A':1, 'B':2, 'C':3}  --> returns 4
        proposedRank = {'A':2, 'B':3, 'C':1}  --> returns 8
        proposedRank = {'A':3, 'B':1, 'C':2}  --> returns 4
        proposedRank = {'A':1, 'B':3, 'C':2}  --> returns 6
        proposedRank = {'A':2, 'B':1, 'C':3}  --> returns 4
        proposedRank = {'A':3, 'B':2, 'C':1}  --> returns 6
        """

    # ToDo : Add checks for partial rank cases and partial metric values being present.
    n_items = len(proposedRank)
    if n_items:
        ranks = scoresToRanks(scores) # Convert scores to ranks
        if not ranks.empty:
            ranks = ranks.reindex(proposedRank) # Reshuffle the dataset according to the proposed rank
            ranks['proposed_rank'] = range(1,ranks.shape[0]+1) # Assign proposed ranks

            distances = 0
            for col in ranks.columns:
                if col != 'proposed_rank':
                    distances+=(ranks[col]-ranks['proposed_rank']).abs().sum() # calculate spearman footrule distance
            return distances

    raise Exception("Sorry, proposed rank is not provided")
