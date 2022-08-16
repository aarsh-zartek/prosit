from lib.choices import GENDER


def has_fasting_blood_sugar(fasting_blood_sugar) -> bool:
    """Returns True if `fasting_blood_sugar` is more than 95"""
    if fasting_blood_sugar < 95:
        return False
    return True

def has_hemoglobin(hemoglobin) -> bool:
    """Returns True if `hemoglobin` is less than or equal to 11"""
    if 11 < hemoglobin:
        return False
    return True

def category_a(data: dict) -> bool:
    # a = normal_diet
    return True

def category_b(data: dict) -> bool:
    # b = fasting_blood_sugar, uric_acid
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    uric_acid = data.get('uric_acid')
    return all([
        has_fasting_blood_sugar(fasting_blood_sugar),
        uric_acid
    ])

def category_c(data: dict) -> bool:
    # c = thyroid, pcod
    thyroid = data.get('thyroid')
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        return all([thyroid, pcod_pcos])
    else:
        return thyroid

def category_d(data: dict) -> bool:
    # d = fasting_blood_sugar, thyroid
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    thyroid = data.get('thyroid')
    return all([
        has_fasting_blood_sugar(fasting_blood_sugar),
        thyroid
    ])

def category_e(data: dict) -> bool:
    # e = thyroid, pcod, fasting_blood_sugar
    thyroid = data.get('thyroid')
    pcod_pcos = data.get('pcod_pcos')
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    gender = data.get('gender')
    if gender == GENDER.female:
        return all([category_d(data), pcod_pcos])
    else:
        return category_d(data)

def category_f(data: dict) -> bool:
    # f = vitamin_b12, hemoglobin
    vitamin_b12 = data.get('vitamin_b12')
    hemoglobin = data.get('hemoglobin')
    return all([
        vitamin_b12,
        hemoglobin
    ])

def category_g(data: dict) -> bool:
    # g = fasting_blood_sugar, creatine
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    creatine = data.get('creatine')
    return all([
        has_fasting_blood_sugar(fasting_blood_sugar),
        creatine,
    ])

def category_h(data: dict) -> bool:
    # h = vitamin_d, thyroid, pcod 
    vitamin_d = data.get('vitamin_d')
    thyroid = data.get('thyroid')
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        return all([
            vitamin_d,
            thyroid,
            pcod_pcos,
        ])
    else:
        return all([
            vitamin_d,
            thyroid,
        ])

def category_i(data: dict) -> bool:
    # i = vitamin_d, fasting_blood_sugar, 
    vitamin_d = data.get('vitamin_d')
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    return all([
        vitamin_d,
        has_fasting_blood_sugar(fasting_blood_sugar)
    ])

def category_j(data: dict) -> bool:
    # j = vitamin_d, uric_acid
    vitamin_d = data.get('vitamin_d')
    uric_acid = data.get('uric_acid')
    return all([vitamin_d, uric_acid])

def category_k(data: dict) -> bool:
    # k = vitamin_b12, fasting_blood_sugar, creatine, 
    vitamin_b12 = data.get('vitamin_b12')
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    creatine = data.get('creatine')
    return all([
        vitamin_b12,
        has_fasting_blood_sugar(fasting_blood_sugar),
        creatine
    ])

def category_l(data: dict) -> bool:
    # l = vitamin_b12, thyroid, pcod, 
    vitamin_b12 = data.get('vitamin_b12')
    thyroid = data.get('thyroid')
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        return all([
            vitamin_b12,
            thyroid,
            pcod_pcos
        ])
    else:
        return all([
            vitamin_b12,
            thyroid
        ])

def get_category(category_data: dict) -> str:
    """Returns a category from the provided `category_data`"""

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
