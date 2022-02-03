
# tbgc - Time Box Graph Creator
# Written by Ian Adams

# Must import matplotlib library to run this file

import sys

# String that represents the indentation amount for subsections on help page
HELP_MESSAGE_INDENT = "         "

# A constant that sets the color that the ideal timebox data will be graphed with.
# It corresponds to the color arguments used by matplotlib
IDEAL_COLOR = "g"
# A constant that sets the color that the actual timebox data will be graphed with.
# It corresponds to the color arguments used by matplotlib
ACTUAL_COLOR = "b"

# Prints a help message for the user, that may or may not include an error
# message, and exits the program
#
# Params:
# - error_message: A string error message to print out with the help message.
# Is None by default
# - exit_code: The code to exit with. Is 0 (success) by default
def print_help_and_exit(error_message=None, exit_code=0):
    if error_message != None:
        print(f"Error: {error_message}\n")
    print("---Help and Program Info---\n")
    print("tbgc - Time Box Graph Creator\nUsage: python tbgc.py [OPTION] [ARGS]")
    print("Options:")
    print("  -h     print help (This message)")
    print("  -e     enter in graph data through console prompts")
    print("  -f     read in graph data from a file; takes an argument of the filename")
    print(f'{HELP_MESSAGE_INDENT}Example Usage of -f: python tbgc.py -f mydatafile.txt')
    print(f"{HELP_MESSAGE_INDENT}Example file layout for use with tbgc (Numbers on the left are line numbers\n{HELP_MESSAGE_INDENT}and do not need to be written)\n")
    print(f"{HELP_MESSAGE_INDENT}1 Name for Graph\n{HELP_MESSAGE_INDENT}2 [ideal val 1] [ideal val 2] [ideal val 3] ... [ideal val n]\n{HELP_MESSAGE_INDENT}3 [actual val 1] [actual val 2] [actual val 3] ... [actual val n]")

    sys.exit(exit_code)

try:
    from matplotlib import rcParams
    from matplotlib.ticker import MaxNLocator
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print_help_and_exit("matplotlib is not installed\nConsult matplotlib documentation for install instructions", 1)

# Parses the command line arguments into a tuple containing the option in index 0 and
# an list of arguments to tbgc in index 1. Options that require no additional
# arguments cause a value of 'None' to be returned in index 1 of the tuple
#
# Returns: A tuple containing the option in index 0 and an list of arguments to tbgc in 
# index 1. (index 1 is 'None' if the option requires no additional arguments)
def parse_args():
    if len(sys.argv) == 1:
        print_help_and_exit()
    
    option = sys.argv[1]

    if option == "-h":
        print_help_and_exit()
    elif option == "-e":
        return ("-e", None)
    elif option == "-f":
        if len(sys.argv) < 3:
            print_help_and_exit("filename arg missing", 1)
        return ("-f", [sys.argv[2]])
    else:
        print_help_and_exit(f"{option} is not a valid option for tbgc", 1)

# Creates and shows the graph
# Params:
# - title: String title of the the graph
# - ideal: list of ideal values
# - actual: list of actual values
# - time: the sprint (x coord) pertaining to the ideal and actual value at each indice
def create_graph(title, ideal, actual, time):
    
    plt.title(title)

    plt.xlabel("Sprints")
    plt.ylabel("Story Points in Backlog")

    # Overlay line plot and scatter plot to get desired effect
    plt.scatter(time, actual, c=ACTUAL_COLOR)
    plt.plot(time, actual, ACTUAL_COLOR, label="Actual")
    
    plt.scatter(time, ideal, c=IDEAL_COLOR)
    plt.plot(time, ideal, IDEAL_COLOR, label="Ideal")

    # Force Axis to have only integer values
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    # Based off of stackoverflow post:
    # https://stackoverflow.com/questions/30914462/matplotlib-how-to-force-integer-tick-labels
    
    rcParams["legend.loc"] = 'upper right'
    plt.legend()

    plt.show()

# Creates a graph based off of data the user enters through prompts in the 
# console
def create_graph_from_prompt():
    graph_title = input("Enter title: ")
    ideal_data = []
    actual_data = []

    while(True):
        try:
            input_len = int(input("How many data points: "))
        except ValueError:
            print("Invalid Input")
            continue
        break
    
    print(f"\n---Ideal Data Point Entry---")
    print(f"Enter the {input_len} ideal amounts of Story Points on the Backlog in order of their corresponding\nsprint. (Starting with the ideal value for sprint 1)")
    i = 0
    while(i < input_len):
        print(f"{len(ideal_data)} ideal data points entered")
        try:
            data_point = int(input("Input ideal data point: "))
        except ValueError:
            print("Invalid Input")
            continue
        i += 1
        ideal_data.append(data_point)
    
    print(f"\n---Actual Data Point Entry---")
    print(f"Enter the {input_len} actual amounts of Story Points on the Backlog in order of their corresponding\nsprint. (Starting with the actual value for sprint 1)")
    i = 0
    while(i < input_len):
        print(f"{len(actual_data)} actual data points entered")
        try:
            data_point = int(input("Input actual data point: "))
        except ValueError:
            print("Invalid Input")
            continue
        i += 1
        actual_data.append(data_point)

    sprints = []
    for i in range(input_len):
        sprints.append(int(i + 1))

    create_graph(graph_title, ideal_data, actual_data, sprints)
    
# Creates a graph from data from a file
def create_graph_from_file(name_of_file_to_read):
    try:
        data_file = open(name_of_file_to_read)
    except OSError:
        print_help_and_exit("Filename invalid or incorrect path", 1)
    lines_list = []
    for line in data_file:
        lines_list.append(line.strip("\n"))
    data_file.close()
    if len(lines_list) != 3:
        print_help_and_exit("File is not exactly 3 lines long", 1)
    
    title = lines_list[0]
    ideal = lines_list[1].split(" ")
    actual = lines_list[2].split(" ")

    if len(ideal) != len(actual):
        print_help_and_exit("Unequal amount of ideal and actual values", 1)

    for i in range(len(ideal)):
        try:
            ideal[i] = int(ideal[i])
        except ValueError:
            print_help_and_exit("One or more ideal values is not a valid integer", 1)
    
    for i in range(len(actual)):
        try:
            actual[i] = int(actual[i])
        except ValueError:
            print_help_and_exit("One or more actual values is not a valid integer", 1)
            
    sprints = []
    for i in range(len(ideal)):
        sprints.append(int(i + 1))

    create_graph(title, ideal, actual, sprints)

# Runs the option chosen by the user
# Params:
# - option: the string option to run
# - args: a list of additional arguments; this can be 'None'
def run_option(option, args):
    if option == "-e":
        create_graph_from_prompt()
    if option == "-f":
        create_graph_from_file(args[0])

# The main function. Delegates tasks to other parts of the program
def main():
    parsed = parse_args()
    run_option(parsed[0], parsed[1])


if __name__ == "__main__":
    main()