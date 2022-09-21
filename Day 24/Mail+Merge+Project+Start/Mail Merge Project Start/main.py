with open('Input/Names/invited_names.txt') as names_file:
    names = names_file.readlines()

with open('Input/Letters/starting_letter.txt') as letter_file:
    blueprint = letter_file.read()

for name in names:
    stripped_name = name.strip()
    new_letter = blueprint.replace('[name]', stripped_name)
    with open(f'Output/ReadyToSend/letter_for_{stripped_name}.txt', "w") as completed_letter:
        completed_letter.write(new_letter)

