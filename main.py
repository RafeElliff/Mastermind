import ast
import math
from copy import deepcopy


# File management related functions
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


# Functions related to adding data

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
        print(f"The most recent tour was {data_from_file[-1]['location']}, number {get_tour_number()}")
        choice = input("import from spreadsheet or input directly? 1 or 2? 3 to end the program and enter the data")
        if choice == "3":
            break
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


def update_choices(current_data):
    past_data = get_data_from_file("choices_for_each.txt")
    dict_of_lists = get_data_from_file("ordered_list_of_items_worn.txt")
    number_of_tour = current_data["number"]
    current_data.pop("location", None)
    current_data.pop("number", None)
    for item, style in current_data.items():  # item and style are used throughout the program to reference different layers of dictionary: item is what she wears, style is the colour/feature e.g. lover_bodysuit would be an item, pink would be a style.
        past_data[item][style].append(number_of_tour)
        dict_of_lists[item].append(style)
    past_data.pop("location", None)
    past_data.pop("number", None)
    overwrite_file("choices_for_each.txt", past_data)
    overwrite_file("ordered_list_of_items_worn.txt", dict_of_lists)


# functions that are related to deleting data

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
    }
    overwrite_file("past_data.txt", past_data_default)
    overwrite_file("choices_for_each.txt", choices_for_each_default)


def delete_most_recent_data():
    choices_for_each = get_data_from_file("choices_for_each.txt")
    for item in choices_for_each.keys():
        for style in choices_for_each[item].keys():
            if get_tour_number() in choices_for_each[item][style]:
                choices_for_each[item][style].remove(get_tour_number())
    ordered_list = get_data_from_file("ordered_list_of_items_worn.txt")
    for item in ordered_list.keys():
        ordered_list[item] = ordered_list[item][:-1]
    past_data = get_data_from_file("past_data.txt")
    past_data = past_data[:-1]

    overwrite_file("choices_for_each.txt", choices_for_each)
    overwrite_file("ordered_list_of_items_worn.txt", ordered_list)
    overwrite_file("past_data.txt", past_data)


# functions that are not accessed, but are remnants from bug-fixing


def temp_function():  # this function created the ordered lists in ordered_list_of_items_worn.txt, it is now done automatically and is not needed anymore
    baseline_dict = {
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
        "karma_jacket": [],
    }

    past_choices = get_data_from_file("past_data.txt")
    for item in baseline_dict.keys():
        for night in past_choices:
            if night[item] is not None:
                baseline_dict[item].append(night[item])
    overwrite_file("ordered_list_of_items_worn.txt", baseline_dict)
    return baseline_dict


def create_list_of_tours_worn():  # this is code that is not accessed directly in the project and is just left over from bugfixing
    past_tour_data = get_data_from_file("past_data.txt")
    past_choices = get_data_from_file("choices_for_each.txt")
    for item in past_tour_data:
        tour_num = item["number"]
        for key, value in item.items():
            if value in past_choices[key]:
                past_choices[key][value].append(tour_num)
            else:
                past_choices[key][value] = [tour_num]
    overwrite_file("choices_for_each.txt", past_choices)


# functions that are necessary for the algorithm

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
            if tour_number - past_choices[item][style][
                -1] > 15:  # 15 is a pretty arbitrary number. I figured, if she doesn't wear something for 15 tours in a row, she probably never will again. It can be changed
                valid_options[item].remove(style)

    return (valid_options)


def count_times_worn():
    dict_of_scores = {
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
    }
    valid_options = get_valid_options()
    past_choices = get_data_from_file("choices_for_each.txt")
    for item in valid_options.keys():
        for style in valid_options[item]:
            list_of_appearances = past_choices[item][style]
            initial_appearance = list_of_appearances[0]
            total_score_for_appearance = 0
            for appearance in list_of_appearances:  # iterates through every appearance the tour has had. this rewards
                total_score_for_appearance = total_score_for_appearance + give_weighting(
                    appearance)  # adds the score for each.
                # total_score_for_appearance = total_score_for_appearance + 1

            final_score = total_score_for_appearance / (get_tour_number() - (
                    initial_appearance - 1))  # total score = sum of all weightings, divides by number of times it could have appeared
            dict_of_scores[item][style] = final_score
    return (dict_of_scores)


def calculate_chance_of_rewear():
    baseline_dict = {
        "lover_bodysuit": 0,
        "man_jacket": 0,
        "lover_guitar": 0,
        "fearless_dress": 0,
        "red_shirt": 0,
        "speak_dress": 0,
        "rep_outfit": 0,
        "folkmore_dress": 0,
        "1989_top": 0,
        "1989_skirt": 0,
        "TTPD_dress": 0,
        "TTPD_set": 0,
        "TTPD_jacket": 0,
        "surprise_dress": 0,
        "midnights_shirtdress": 0,
        "midnights_bodysuit": 0,
        "karma_jacket": 0,
    }
    past_choices_lists = get_data_from_file("ordered_list_of_items_worn.txt")
    for item, list_of_items in past_choices_lists.items():
        total_count_of_rewear = 0
        for count in range(0, len(list_of_items) - 1):
            if list_of_items[count] == list_of_items[count + 1]:
                total_count_of_rewear = total_count_of_rewear + 1
            percentage_chance = total_count_of_rewear / (len(list_of_items) - 1)
            baseline_dict[item] = percentage_chance
    return baseline_dict


def give_weighting(tour_number):
    tour_being_checked = tour_number
    final_tour_number = get_tour_number()
    final_weighting = 0.5 + ((tour_being_checked - 1) / (final_tour_number - 1)) * 0.5  # this is the formula that I
    # went with, can be changed if you want to change the weighting in favour of/against when a tour happened
    return final_weighting


def calc_days_since_last_worn(item, style):
    past_data = get_data_from_file("choices_for_each.txt")
    tour_number = get_tour_number()
    days_since_last_worn = tour_number - past_data[item][style][-1]
    return days_since_last_worn


def calc_weighting_of_days_since_last_worn(item, style):
    days_since_last_worn = calc_days_since_last_worn(item, style)
    valid_options = get_valid_options()
    num_of_options = len(valid_options[item])
    weighting = min(math.sqrt(days_since_last_worn), num_of_options) + 1
    print(item, style, weighting)
    return weighting


# functions related to the algorithm itself

def get_final_scores():
    final_scores = {
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
    }

    list_of_items_worn = get_data_from_file("ordered_list_of_items_worn.txt")
    scores_per_item = count_times_worn()
    rewear_dict = calculate_chance_of_rewear()

    for item in scores_per_item.keys():
        for style in scores_per_item[item].keys():
            initial_score_of_item = scores_per_item[item][style]
            final_score_of_item = initial_score_of_item
            # if list_of_items_worn[item][-1] == style:
            #     final_score_of_item = initial_score_of_item * chance_of_rewear[item]
            days_weighting = calc_weighting_of_days_since_last_worn(item, style)
            final_score_of_item = days_weighting / rewear_dict[item]
            final_scores[item][style] = final_score_of_item

    return final_scores


def percentage_breakdown(item):
    final_scores = get_final_scores()
    dict_of_one_item = final_scores[item]
    total_of_all_scores = 0
    for style in dict_of_one_item.keys():
        total_of_all_scores = total_of_all_scores + dict_of_one_item[style]
    print("\n")
    for value in dict_of_one_item.keys():
        percentage_certainty = (final_scores[item][value] / total_of_all_scores) * 100
        print(f"{value} at {round(percentage_certainty, 1)}%")
    print("\n")


def prepare_output():
    print("\n")
    total_expected_points = 0
    point_values_for_questions = {
        "lover_bodysuit": 6,
        "man_jacket": 6,
        "lover_guitar": 4,
        "fearless_dress": 6,
        "red_shirt": 7,
        "speak_dress": 9,
        "rep_outfit": 2,
        "folkmore_dress": 9,
        "1989_top": 7,
        "1989_skirt": 7,
        "TTPD_dress": 3,
        "TTPD_set": 6,
        "TTPD_jacket": 5,
        "surprise_dress": 6,
        "midnights_shirtdress": 7,
        "midnights_bodysuit": 5,
        "karma_jacket": 5,
    }
    final_scores = get_final_scores()
    for item in final_scores.keys():
        highest_chance = 0
        best_scorer = None
        total_score_for_item = 0
        for style in final_scores[item].keys():
            total_score_for_item = total_score_for_item + final_scores[item][style]
            if final_scores[item][style] > highest_chance:
                highest_chance = final_scores[item][style]
                best_scorer = style
        percentage_certainty = round(((highest_chance / total_score_for_item) * 100), 1)
        point_value = point_values_for_questions[item]
        expected_points = round(point_value * (percentage_certainty / 100), 1)
        total_expected_points = total_expected_points + expected_points
        print(f"{item}: {best_scorer}, {percentage_certainty}% certainty. expected_points = {expected_points}")
        total_available_points = 0
        for item, point_value in point_values_for_questions.items():
            total_available_points = total_available_points + point_value
    total_expected_points = round(total_expected_points, 0)
    print(
        f"Total expected points: {total_expected_points}. As there were {total_available_points} points available, you should get {round((total_expected_points / total_available_points) * 100, 1)}%")

    print("\n")


# Functions related to data extraction
def return_data_for_tour():
    index = int(input("Which tour? Input '0' for the most recent tour, -1 for the second most recent etc"))
    choice = input("items and styles or just styles? Please input 1 or 2")
    past_data = get_data_from_file("past_data.txt")
    if index > 0:
        index = index - 1
    dict_of_data = past_data[index]
    for item, style in dict_of_data.items():
        if choice == "1":
            print(item, style)
        else:
            print(style)


user_input = input(
    "Choice. \n 1 = add new data \n 2 = get prediction \n 3 = delete most recent data \n 4 = delete all data\n 5 = testing features\n 6 = get data for a given tour")

if user_input == "1":
    get_new_data()
if user_input == "2":
    prepare_output()
    while True:
        choice = input(
            "If you would like to view a percentage breakdown for a certain item, enter the name now or enter 'END' to end\n")
        if choice == "END":
            break
        try:
            percentage_breakdown(choice)
        except KeyError:
            print("There may have been a typo, this is not a valid item")
        except:
            print("There was another error")
if user_input == "3":
    delete_most_recent_data()
if user_input == "4":
    reset_data()
if user_input == "5":
    print(calc_days_since_last_worn("lover_bodysuit", "pink"))
if user_input == "6":
    while True:
        return_data_for_tour()
else:
    pass
