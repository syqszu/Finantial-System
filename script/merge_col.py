import pandas as pd

def merge_col(goal_col, tool_col):
    goal_col = goal_col[tool_col.columns]
    match_col = pd.concat([goal_col, tool_col])

    return match_col