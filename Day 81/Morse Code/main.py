# Dictionary for translation purposes
morse_dict = {'A': '.-', 'B': '-...',
              'C': '-.-.', 'D': '-..', 'E': '.',
              'F': '..-.', 'G': '--.', 'H': '....',
              'I': '..', 'J': '.---', 'K': '-.-',
              'L': '.-..', 'M': '--', 'N': '-.',
              'O': '---', 'P': '.--.', 'Q': '--.-',
              'R': '.-.', 'S': '...', 'T': '-',
              'U': '..-', 'V': '...-', 'W': '.--',
              'X': '-..-', 'Y': '-.--', 'Z': '--..',
              '1': '.----', '2': '..---', '3': '...--',
              '4': '....-', '5': '.....', '6': '-....',
              '7': '--...', '8': '---..', '9': '----.',
              '0': '-----', ', ': '--..--', '.': '.-.-.-',
              '?': '..--..', '/': '-..-.', '-': '-....-',
              '(': '-.--.', ')': '-.--.-'}

# Getting to-be-translated message from user
user_input = input("Enter the message you want to translate to morse code:\n")
# Declaring output string
output = ""
# Boolean variable indicating that nothing went wrong during translating message
successful = True

# For every character in user input check if it's translatable
# If character is translatable add its translated counterpart to output string
for char in user_input:
    if char.upper() in morse_dict.keys():
        output += morse_dict.get(char.upper()) + " "
    elif char == " ":
        output += "  "
    # If input string contains non-translatable character stop executing script and print message informing about
    # unsupported character
    else:
        print(f"One or more characters you have entered is not supported.\n"
              f"List of available characters:{morse_dict.keys()}")
        successful = False
        break

# If translation was successful print output message
if successful:
    print(f"Your message translated to morse code:\n{output}")
