import ast


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
    print(current_data)
    print(past_data)
    for key, value in current_data.items():
        past_data[key][value] = number_of_tour
    overwrite_file("choices_for_each.txt", past_data)


def get_new_data():
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
    for key in data_dict.keys():
        data_dict[key] = (input(key))
    data_dict["number"] = number_of_tour
    append_dict_to_file_data_list("past_data.txt", data_dict)
    update_choices(data_dict)


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


user_input = input("Choice. \n 1 = add new data. \n 2 = get prediction \n 3 = delete all data")

if user_input == "1":
    get_new_data()
if user_input == "2":
    print("working on it")
if user_input == "3":
    reset_data()
