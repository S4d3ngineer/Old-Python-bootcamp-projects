# TODO 1. Create a dictionary in this format:
import pandas
with open('nato_phonetic_alphabet.csv') as nato_file:
    nato_df = pandas.read_csv(nato_file)
nato_dict = {row.letter: row.code for (index, row) in nato_df.iterrows()}

# TODO 2. Create a list of the phonetic code words from a word that the user inputs.


def check_input():
    try:
        user_input = input('Please enter the word that you want to spell in NATO alphabet: ').upper()
        output = [nato_dict[char] for char in user_input]
    except KeyError:
        print("You might type only letters from the alphabet!")
        check_input()
    else:
        print(output)
        check_input()


check_input()
