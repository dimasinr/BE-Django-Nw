# def calculate_total_duration(data):
#         result = {}
#         for item in data:
#             employee_id = item["employee"]
#             working_minutes = item["working_hour"]
#             if employee_id in result:
#                 result[employee_id]["total_duration"] += working_minutes
#             else:
#                 result[employee_id] = {
#                     "total_duration": working_minutes,
#                 }
#             if result[employee_id]["total_duration"] % 100 >= 60:
#                 result[employee_id]["total_duration"] += 40
#                 result[employee_id]["total_duration"] += 100

#         return result

def calculate_total_duration(data):
    result = {}
    for item in data:
        employeeId = item["employee"]["pk"]
        working_minutes = item["working_hour"]
        if employeeId in result:
            result[employeeId]["total_duration"] += working_minutes
        else:
            result[employeeId] = {
                "total_duration": working_minutes,
            }
        if result[employeeId]["total_duration"] % 100 >= 60:
            result[employeeId]["total_duration"] += 40
            result[employeeId]["total_duration"] += 100

    return result

def parseHour(hour):
    va_hour = 0
    if hour and hour != 0:
        h_str = str(hour)
        if len(h_str) <= 2:
            return '0'
        va_hour = int(h_str[:-2])
    return va_hour

def parseMinute(hour):
    minutes = '0'
    if hour:
        h_str = str(hour)
        minutes = int(h_str[-2:])
        if minutes == 0:
            minutes = '0'
    return minutes

def parseToHour(hour):
    dig_awal = hour // 100
    dig_akhir = hour % 100

    if dig_akhir > 59:
        dig_awal += 1
        dig_akhir -= 60

    humanize_hour = dig_awal * 100 + dig_akhir

    return int(humanize_hour)

def median(lst):
    sorted_lst = sorted(lst)
    middle_index = len(sorted_lst) // 2
    if len(sorted_lst) % 2 == 1:
        median = sorted_lst[middle_index]
    else:
        median = (sorted_lst[middle_index - 1] + sorted_lst[middle_index]) / 2.0
    
    return median

def formula_sum_actual(x, y):
    var_d = x - y
    var_x = str(var_d)
    length = len(var_x)
    data1 = length - 2
    slics = var_x[data1:]
    slics_int = int(slics)
    print(slics)
    print(length)
    var4 = var_d + 40
    print(str(var4)[-2:])
    pars = int(str(var4)[-2:])
    
    if slics_int > 59:
        if var_d < 40:
            print("if 1.1")
            return var4
        else:
            print("else 1")
            return var_d - 40
    else:
        if pars > 59:
            if pars > 60:
                print("if 1")
                return var_d
            elif pars > 40:
                return var_d - 40
            else:
                print("if 1.2")
                return x - y
        else:
            if pars < 59:
                if var_d < 40:
                    print("if 2")
                    return var_d + 40
                else:
                    print("if 2.2")
                    return var_d
            else:
                print("else 3")
                return var_d + 40

def fix_hour(hour):
    hour_actual = str(hour)
    two_digit = hour_actual[-2:] 
    two = int(hour_actual[-2:])
    if two_digit == '00':
        two_digit = '00'
    else:
        if int(two_digit) > 59:
            two += 40
            two_digit = two 

    return int(f"{hour_actual[:-2] }{two_digit}")
    # h = int(hour)
    # if hour > 59:
    #     h = hour + 40

    # return h