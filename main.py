import ast
from copy import deepcopy

def get_data_from_file(filename):
    with open(filename, "r") as file:
        text = file.read()
        data = ast.literal_eval(text)
    return data


def append_dict_to_file_data_list(filename, data):
    read_data = get_data_from_file(filename)
    read_data.append(data)
    with open(filename, "w") as file:
        file.write(str(read_data))


def overwrite_file(filename, data):
    with open(filename, "w") as file:
        file.write(str(data))


def update_choices(current_data):
    past_data = get_data_from_file("choices_for_each.txt")
    number_of_tour = current_data["number"]
    for key, value in current_data.items():
        past_data[key][value].append(number_of_tour)
    overwrite_file("choices_for_each.txt", past_data)


def get_new_data():
    while True:
        data_from_file = get_data_from_file("past_data.txt")
        number_of_tour = len(data_from_file) + 1
        data_dict = {
            "location": None,
            "lover_bodysuit": None,
            "man_jacket": None,
            "lover_guitar": None,
            "fearless_dress": None,
            "red_shirt": None,
            "speak_dress": None,
            "rep_outfit": None,
            "folkmore_dress": None,
            "1989_top": None,
            "1989_skirt": None,
            "TTPD_dress": None,
            "TTPD_set": None,
            "TTPD_jacket": None,
            "surprise_dress": None,
            "midnights_shirtdress": None,
            "midnights_bodysuit": None,
            "karma_jacket": None,
        }
        choice = input("import from spreadsheet or input directly? 1 or 2")
        if choice == "1":
            print("enter spreadsheet column:\n")
            words = []
            while True:
                word = input().strip()
                if not word:
                    break
                words.append(word)

            keys_list = list(data_dict.keys())
            data_dict = {}

            for key, value in zip(keys_list, words):
                if value != "x":
                    data_dict[key] = value
                else:
                    data_dict[key] = None

        elif choice == "2":
            for key in data_dict.keys():
                user_input = (input(key))
                if user_input != " ":
                    data_dict[key] = user_input

        data_dict["number"] = number_of_tour
        if data_dict["karma_jacket"] is not None:
            append_dict_to_file_data_list("past_data.txt", data_dict)
            update_choices(data_dict)


def create_list_of_tours_worn():
    past_tour_data = get_data_from_file("past_data.txt")
    past_choices = get_data_from_file("choices_for_each.txt")
    for item in past_tour_data:
        tour_num = item["number"]
        for key, value in item.items():  # key is the type of clothing, value is the colour
            # recent_data_for_item = current_data[key]
            if value in past_choices[key]:
                past_choices[key][value].append(tour_num)
            else:
                past_choices[key][value] = [tour_num]
    overwrite_file("choices_for_each.txt", past_choices)


def get_tour_number():
    tour_number = len(get_data_from_file("past_data.txt"))
    return tour_number

def get_valid_options():
    tour_number = get_tour_number()
    past_choices = get_data_from_file("choices_for_each.txt")
    options = {
        "lover_bodysuit": [],
        "man_jacket": [],
        "lover_guitar": [],
        "fearless_dress": [],
        "red_shirt": [],
        "speak_dress": [],
        "rep_outfit": [],
        "folkmore_dress": [],
        "1989_top": [],
        "1989_skirt": [],
        "TTPD_dress": [],
        "TTPD_set": [],
        "TTPD_jacket": [],
        "surprise_dress": [],
        "midnights_shirtdress": [],
        "midnights_bodysuit": [],
        "karma_jacket": []
    }
    for item, style in past_choices.items():
        if item != "location" and item != "number":
            for style in style.keys():
                options[item].append(style)
    valid_options = deepcopy(options)
    for item in options.keys():
        for style in options[item]:
            if tour_number - past_choices[item][style][-1] > 15:
                valid_options[item].remove(style)

    return (valid_options)

def count_times_worn():
    dict_of_scores = {
        "location": {},
        "lover_bodysuit": {},
        "man_jacket": {},
        "lover_guitar": {},
        "fearless_dress": {},
        "red_shirt": {},
        "speak_dress": {},
        "rep_outfit": {},
        "folkmore_dress": {},
        "1989_top": {},
        "1989_skirt": {},
        "TTPD_dress": {},
        "TTPD_set": {},
        "TTPD_jacket": {},
        "surprise_dress": {},
        "midnights_shirtdress": {},
        "midnights_bodysuit": {},
        "karma_jacket": {},
        "number": {}
    }
    valid_options = get_valid_options()
    past_choices = get_data_from_file("choices_for_each.txt")
    for item in valid_options.keys():
        for style in valid_options[item]:
            list_of_appearances = past_choices[item][style]
            initial_appearance = list_of_appearances[0]
            total_score_for_appearance = 0
            for appearance in list_of_appearances: #iterates through every appearance the tour has had. this rewards
                total_score_for_appearance = total_score_for_appearance + give_weighting(appearance) #adds the score for each.
            print(style, total_score_for_appearance)
            final_score = total_score_for_appearance/(get_tour_number()-(initial_appearance-1)) # total score = sum of all weightings, divides by number of times it could have appeared
            dict_of_scores[item][style] = final_score
    return(dict_of_scores)


def give_weighting(tour_number):
    tour_being_checked = tour_number
    final_tour_number = get_tour_number()
    final_weighting = 0.5 + ((tour_being_checked-1)/(final_tour_number-1))*0.5
    return final_weighting

def reset_data():
    past_data_default = []
    choices_for_each_default = {
        "location": {},
        "lover_bodysuit": {},
        "man_jacket": {},
        "lover_guitar": {},
        "fearless_dress": {},
        "red_shirt": {},
        "speak_dress": {},
        "rep_outfit": {},
        "folkmore_dress": {},
        "1989_top": {},
        "1989_skirt": {},
        "TTPD_dress": {},
        "TTPD_set": {},
        "TTPD_jacket": {},
        "surprise_dress": {},
        "midnights_shirtdress": {},
        "midnights_bodysuit": {},
        "karma_jacket": {},
        "number": {}
    }
    overwrite_file("past_data.txt", past_data_default)
    overwrite_file("choices_for_each.txt", choices_for_each_default)

def get_predictions():
    count_times_worn()

user_input = input("Choice. \n 1 = add new data. \n 2 = get prediction \n 3 = delete all data")

if user_input == "1":
    get_new_data()
if user_input == "2":
    get_predictions()
if user_input == "3":
    reset_data()
