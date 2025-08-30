def flagify_from_cli(ctx, param, value):
    return flagify(value)

def flagify(flag_list):
    if flag_list is None:
        return flag_list

    flags = 0;

    for flag in flag_list:
        flags = flags | flag

    return flags

