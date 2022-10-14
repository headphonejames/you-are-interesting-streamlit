fun_str = "fun!"
pretty_fun_str = "pretty fun"
ok_str = "ok"
not_fun_str = "not fun"
ineffective_str = "ineffective"
unrated_str = "unrated"

value = "value"
index = "index"

values_map = {
    unrated_str: {value: 0, index: 0},
    fun_str: {value: 5, index: 1},
    pretty_fun_str: {value: 4, index: 2},
    ok_str: {value: 3, index: 3},
    not_fun_str: {value: 2, index: 4},
    ineffective_str: {value: 1, index: 5}
}

values = []
for values_obj_key in values_map:
    values.append(values_obj_key)

def get_index_from_value(radio_value):
    for value_key in values_map:
        if values_map[value_key][value] == radio_value:
            return values_map[value_key][index]
    return 0