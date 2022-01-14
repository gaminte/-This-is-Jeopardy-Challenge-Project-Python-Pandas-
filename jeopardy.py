import random
import pandas as pd
from random import randint
pd.set_option('display.max_colwidth', None)
pd.set_option('max_columns', None)
pd.set_option('max_rows', None)
jeopardy = pd.read_csv('jeopardy.csv')
jeopardy.rename(columns = {'Show Number': 'show_number',
                                                        ' Air Date': 'air_date',
                                                        ' Round': 'round',
                                                        ' Category': 'category',
                                                        ' Value': 'value',
                                                        ' Question': 'question',
                                                        ' Answer': 'answer'}, inplace = True)
# print(jeopardy.head(5))

jeopardy['question'] = jeopardy['question'].apply(lambda name: f"{name}?")
# print(jeopardy.head(5))

# Values to float--
jeopardy['value_float'] = jeopardy['value'].apply(lambda num: 0 if num == 'None' else float(num[1:].replace(",", "")))
# print(jeopardy['value_float'])

# Filtering Question column--
def filter_question(df, words,column):
    return df[df[column].apply(lambda row: all(word.lower() in row.lower() for word in words))].reset_index()
question_filter = filter_question(jeopardy,['King', 'England'], 'question')
# print(question_filter)

# king question filter--
king_filter = filter_question(jeopardy,['King'],'question')
# print(king_filter)

# Mean of values_king--
king_mean = king_filter['value_float'].mean()
# print(f"king mean: {king_mean}")

# Count of unique answers--
count_answers = jeopardy['answer'].value_counts()
# print(f"Count answers: {count_answers}")

# Count of unique King answers--
count_king_answers = king_filter['answer'].value_counts()
# print(f"Count King answers: {count_king_answers}")

# User Quiz--
print("********************")
print(f"     'Jeopardy'    ")
print("********************")
print("** You have 3 attempts to find the answer **")
def user_quiz():
    i = random.randint(0, len(jeopardy['question']))
    user_question = f"You are playing {jeopardy['round'][i]} in {jeopardy['category'][i]} for {jeopardy['value'][i]} and your question is {jeopardy['question'][i]}"
    count = 1
    while count == 1:
        user_answer = input(f"{user_question}: ")
        if user_answer.lower() == jeopardy['answer'][i].lower():
            return f"Your got the answer right and You won {jeopardy['value'][i]}!!!"
            break
        else:
            count+=1
    while count ==2:
        user_answer = input("2nd try: ")
        if user_answer.lower() == jeopardy['answer'][i].lower():
            return f"Your got the answer right and You won {jeopardy['value'][i]}!!!"
            break
        else:
            count+=1
    while count ==3:
        user_answer = input("last try: ")
        if user_answer.lower() == jeopardy['answer'][i].lower():
            return f"Your got the answer right and You won {jeopardy['value'][i]}!!!"
        else:
            count+=1
            return "You got the answer wrong!!, GAME OVER!!!"
quiz_user = user_quiz()
print(quiz_user)

# relation between category and round--
def category_round_rel():
    return  jeopardy.groupby(["category", "round"])["show_number"].count().reset_index().pivot(columns="round",
                                                                                                                                                   index="category",
                                                                                                                                                    values="show_number")
category_round_relation = category_round_rel()
# print(category_round_relation.head(10))

# relation between category and round with "LITERATURE"--
c_r_r_lit = category_round_relation.loc["LITERATURE"]
# print(f"Relation between category and round with 'LITERATURE': {c_r_r_lit}")

# How questions change over time--
computer_df = filter_question(jeopardy, ['Computer'], 'question')
computer_df['air_date'] = pd.to_datetime(computer_df['air_date'])
computer_90s_df = computer_df[(computer_df['air_date'] > '31-12-1989') & (computer_df['air_date'] < '01-01-2000')]
computer_2000s_df = computer_df[(computer_df['air_date'] > '31-12-1999') & (computer_df['air_date'] < '01-01-2010')]
# print(f"Number of questions based on computer in 90s: {computer_90s_df.air_date.count()}")
# print(f"Number of questions based on computer in 2000s: {computer_2000s_df.air_date.count()}")

