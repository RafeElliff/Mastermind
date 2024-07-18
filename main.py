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
    dict_of_lists = get_data_from_file("ordered_list_of_items_worn.txt")
    number_of_tour = current_data["number"]
    for item, style in current_data.items():  # item and style are used throughout the program to reference different layers of dictionary: item is what she wears, style is the colour/feature e.g. lover_bodysuit would be an item, pink would be a style.
        past_data[item][style].append(number_of_tour)
        dict_of_lists[item].append(style)
    past_data.pop("location", None)
    past_data.pop("number", None)
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
        for key, value in item.items():
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
                total_score_for_appearance = total_score_for_appearance + give_weighting(appearance)  # adds the score for each.
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


def give_weighting(tour_number):
    tour_being_checked = tour_number
    final_tour_number = get_tour_number()
    final_weighting = 0.5 + ((tour_being_checked - 1) / (final_tour_number - 1)) * 0.5  # this is the formula that I went with, can be changed if you want to change the weighting in favour of/against when a tour happened
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
    chance_of_rewear = calculate_chance_of_rewear()

    # chance for item = scores_per_item[item][style]
    # for item, style in scores_per_item.items():
    #     print(item, style)
    for item in scores_per_item.keys():
        for style in scores_per_item[item].keys():
            initial_score_of_item = scores_per_item[item][style]
            final_score_of_item = initial_score_of_item
            if list_of_items_worn[item][-1] == style:
                final_score_of_item = initial_score_of_item * chance_of_rewear[item]
            # print(style, initial_score_of_item, final_score_of_item)
            final_scores[item][style] = final_score_of_item
    # print(final_scores)

    # highest_scorers

    for item in final_scores.keys():
        highest_chance = 0
        best_scorer = None
        total_score_for_item = 0
        for style in final_scores[item].keys():
            total_score_for_item = total_score_for_item + final_scores[item][style]
            if final_scores[item][style] > highest_chance:
                highest_chance = final_scores[item][style]
                best_scorer = style
        percentage_certainty = ((highest_chance/total_score_for_item)-(1/get_tour_number()))*100
        print(f"{item}: {best_scorer}, {round(percentage_certainty, 1)}% certainty")
    return




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

def prepare_output():
    get_final_scores()


user_input = input("Choice. \n 1 = add new data. \n 2 = get prediction \n 3 = delete most recent data \n 4 = delete all data" )

if user_input == "1":
    get_new_data()
if user_input == "2":
    prepare_output()
if user_input == "3":
    delete_most_recent_data()
if user_input == "4":
    reset_data()
