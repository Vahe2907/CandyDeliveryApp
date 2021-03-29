import re
import iso8601


def parse_interval(interval):
    answer = {"status": 0}

    if not re.match(r"[0-9]?[0-9]:[0-9]?[0-9]-[0-9]?[0-9]:[0-9]?[0-9]", interval):
        answer["status"] = 1
        return answer

    parts = interval.split("-")

    start = int(parts[0].split(":")[0]) * 3600 + int(parts[0].split(":")[1]) * 60
    end = int(parts[1].split(":")[0]) * 3600 + int(parts[1].split(":")[1]) * 60

    if end - start < 0:
        answer["status"] = 1
        return answer

    answer["start"] = start
    answer["end"] = end

    return answer


def get_interval_values(interval):
    res = parse_interval(interval)

    return res["start"], res["end"]


def compatible(weight, courier_type):
    max_weights = {
        "foot": 10,
        "bike": 15,
        "car": 50
    }

    if weight > max_weights[courier_type]:
        return False

    return True


def withdraw(courier_type):
    coefficients = {
        "foot": 2,
        "bike": 5,
        "car": 9
    }

    return 500 * coefficients[courier_type]


def hours_intersection_check(left_hours, right_hours):
    intervals1 = [get_interval_values(tmp) for tmp in left_hours]
    intervals2 = [get_interval_values(tmp) for tmp in right_hours]

    for a in intervals1:
        for b in intervals2:
            if max(0, min(a[1], b[1]) - max(a[0], b[0])):
                return True

    return False


def get_date_object(date_string):
    return iso8601.parse_date(date_string)


def get_date_string(date_object):
    return ('%04d-%02d-%02dT%02d:%02d:%02d.%02d%s' %
            (date_object.year, date_object.month,
             date_object.day, date_object.hour, date_object.minute,
             date_object.second, date_object.microsecond / 1000, "Z"))
