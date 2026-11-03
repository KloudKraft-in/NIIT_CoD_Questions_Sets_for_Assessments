import numpy as np

def create_vote_array(vote_list):
    # Converts a list of vote IDs to a NumPy integer array
    return np.array(vote_list, dtype=int)

def count_votes_per_candidate(vote_array):
    """
    Counts only the votes that exist in the vote array.
    For input [1, 2, 2, 3], returns [1, 2, 1] — not fixed size.
    """
    unique, counts = np.unique(vote_array, return_counts=True)
    return counts


def determine_winner(vote_array):
    """
    Uses count_votes_per_candidate to find the candidate with the most votes.
    If tie, returns the candidate with the smallest number.
    """
    counts = count_votes_per_candidate(vote_array)
    return int(np.argmax(counts) + 1)  # +1 to convert index to candidate number

def validate_vote_array(vote_array):
    """
    Returns True if vote_array:
    - Is a NumPy ndarray
    - Contains only integers
    - All values between 1 and 5 (inclusive)
    """
    if not isinstance(vote_array, np.ndarray):
        return False
    if not np.issubdtype(vote_array.dtype, np.integer):
        return False
    if not np.all((vote_array >= 1) & (vote_array <= 5)):
        return False
    return True