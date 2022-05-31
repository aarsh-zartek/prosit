from lib.choices import GENDER


def has_fasting_blood_sugar(fasting_blood_sugar) -> bool:
    if 70 < fasting_blood_sugar < 95:
        return False
    return True

def has_cholesterol(cholesterol) -> bool:
    if 70 < cholesterol < 95:
        return False
    return True

def has_hemoglobin(hemoglobin) -> bool:
    if 11 < hemoglobin < 15:
        return False
    return True

def category_a(data) -> bool:
    # a = normal_diet, cholesterol
    normal_diet = data.get('normal_diet')
    cholestrol = data.get('cholestrol')
    if normal_diet and has_cholesterol(cholestrol):
        return True
    return False

def category_b(data) -> bool:
    # b = sugar, uric_acid, cholesterol
    sugar = data.get('sugar')
    uric_acid = data.get('uric_acid')
    cholesterol = data.get('cholesterol')
    if all(has_fasting_blood_sugar(sugar), uric_acid, has_cholesterol(cholesterol)):
        return True
    return False

def category_c(data) -> bool:
    # c = thyroid, pcod, cholesterol
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        pass
    return True

def category_d(data) -> bool:
    # d = sugar, thyroid, cholesterol
    return True

def category_e(data) -> bool:
    # e = thyroid, pcod, cholesterol, sugar
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        pass
    return True

def category_f(data) -> bool:
    # f = vitamin_b12, hemoglobin, cholesterol
    return True

def category_g(data) -> bool:
    # g = sugar, creatine, cholesterol
    return True

def category_h(data) -> bool:
    # h = vitamin_d, thyroid, pcod, cholesterol
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        pass
    return True

def category_i(data) -> bool:
    # i = vitamin_d, sugar, cholesterol
    return True

def category_j(data) -> bool:
    # j = vitamin_d, cholesterol, uric_acid
    return True

def category_k(data) -> bool:
    # k = vitamin_b12, sugar, creatine, cholesterol
    return True

def category_l(data) -> bool:
    # l = vitamin_b12, thyroid, pcod, cholesterol
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        pass
    return True

def get_category(category_data: dict) -> str:

    if category_l(category_data):
        return "L"
    elif category_k(category_data):
        return "K"
    elif category_j(category_data):
        return "J"
    elif category_i(category_data):
        return "I"
    elif category_h(category_data):
        return "H"
    elif category_g(category_data):
        return "G"
    elif category_f(category_data):
        return "F"
    elif category_e(category_data):
        return "E"
    elif category_d(category_data):
        return "D"
    elif category_c(category_data):
        return "C"
    elif category_b(category_data):
        return "B"
    elif category_a(category_data):
        return "A"
    else:
        return "0"