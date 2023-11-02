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
    if hour:
        h_str = str(hour)
        if len(h_str) <= 2:
            return '0'
        va_hour = int(h_str[:-2])
    return va_hour

def parseMinute(hour):
    minutes = 0
    if hour:
        h_str = str(hour)
        minutes = int(h_str[-2:])
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