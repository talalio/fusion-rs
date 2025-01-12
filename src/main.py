#!/usr/bin/python

from models.cf import CF


if __name__=='__main__':

    recsys = CF('./data/ratings.csv', './data/movies.csv')

    while True:
        # Prompt the user for input
        user_input = input("Enter the name of a movie you like: ")
        if user_input == "exit":
            print("bye!")
            break
        
        recommendations = recsys.recommend(user_input, top_n=5)

        # Display recommendations
        print("\nRecommendations based on your input:")
        for idx, title in enumerate(recommendations, start=1):
            print(f"\t{idx}. {title}")
