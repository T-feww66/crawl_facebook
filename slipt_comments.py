import pandas as pd

def split_comments(df):
    comments = df.comment
    split_comments = []
    split_usernames = []
    for comment in comments:
        #tach usename bang \n dau tien
        split_usernames.append(comment.split('\n')[0].strip())
        # phan con lai la comment
        split_comments.append('\n'.join(comment.split('\n')[1:]).strip())

    #xoá cột comments ban đâu
    df.drop('comment', axis=1, inplace=True)
    #them cot username
    df['username'] = split_usernames
    #them cot comment
    df['comment'] = split_comments

    return df