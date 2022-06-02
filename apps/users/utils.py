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

def category_a(data: dict) -> bool:
    # a = normal_diet, cholesterol
    normal_diet = data.get('normal_diet')
    cholestrol = data.get('cholestrol')
    return all([normal_diet, has_cholesterol(cholestrol)])

def category_b(data: dict) -> bool:
    # b = fasting_blood_sugar, uric_acid, cholesterol
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    uric_acid = data.get('uric_acid')
    cholesterol = data.get('cholesterol')
    return all([
        has_fasting_blood_sugar(fasting_blood_sugar),
        has_cholesterol(cholesterol),
        uric_acid,
    ])

def category_c(data: dict) -> bool:
    # c = thyroid, pcod, cholesterol
    thyroid = data.get('thyroid')
    cholesterol = data.get('cholesterol')
    pcod_pcos = data.get('pcod_pcos')
    thyroid_cholesterol = thyroid and has_cholesterol(cholesterol)
    gender = data.get('gender')
    if gender == GENDER.female:
        return all([thyroid_cholesterol, pcod_pcos])
    else:
        return all([thyroid_cholesterol])

def category_d(data: dict) -> bool:
    # d = fasting_blood_sugar, thyroid, cholesterol
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    thyroid = data.get('thyroid')
    cholesterol = data.get('cholesterol')
    return all([
        has_fasting_blood_sugar(fasting_blood_sugar),
        has_cholesterol(cholesterol),
        thyroid,
    ])

def category_e(data: dict) -> bool:
    # e = thyroid, pcod, cholesterol, fasting_blood_sugar
    thyroid = data.get('thyroid')
    pcod_pcos = data.get('pcod_pcos')
    cholesterol = data.get('cholesterol')
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    gender = data.get('gender')
    if gender == GENDER.female:
        return all([category_d(data), pcod_pcos])
    else:
        return category_d(data)

def category_f(data: dict) -> bool:
    # f = vitamin_b12, hemoglobin, cholesterol
    vitamin_b12 = data.get('vitamin_b12')
    hemoglobin = data.get('hemoglobin')
    cholesterol = data.get('cholesterol')
    return all([
        vitamin_b12,
        hemoglobin,
        has_cholesterol(cholesterol)
    ])

def category_g(data: dict) -> bool:
    # g = fasting_blood_sugar, creatine, cholesterol
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    creatine = data.get('creatine')
    cholesterol = data.get('cholesterol')
    return all([
        has_fasting_blood_sugar(fasting_blood_sugar),
        has_cholesterol(cholesterol),
        creatine,
    ])

def category_h(data: dict) -> bool:
    # h = vitamin_d, thyroid, pcod, cholesterol
    vitamin_d = data.get('vitamin_d')
    thyroid = data.get('thyroid')
    cholesterol = data.get('cholesterol')
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        return all([
            vitamin_d,
            thyroid,
            pcod_pcos,
            has_cholesterol(cholesterol)
        ])
    else:
        return all([
            vitamin_d,
            thyroid,
            has_cholesterol(cholesterol)
        ])

def category_i(data: dict) -> bool:
    # i = vitamin_d, fasting_blood_sugar, cholesterol
    vitamin_d = data.get('vitamin_d')
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    cholesterol = data.get('cholesterol')
    return all([
        vitamin_d,
        has_fasting_blood_sugar(fasting_blood_sugar),
        has_cholesterol(cholesterol)
    ])

def category_j(data: dict) -> bool:
    # j = vitamin_d, cholesterol, uric_acid
    vitamin_d = data.get('vitamin_d')
    uric_acid = data.get('uric_acid')
    cholesterol = data.get('cholesterol')
    return all([
        vitamin_d,
        uric_acid,
        has_cholesterol(cholesterol)
    ])

def category_k(data: dict) -> bool:
    # k = vitamin_b12, fasting_blood_sugar, creatine, cholesterol
    vitamin_b12 = data.get('vitamin_b12')
    fasting_blood_sugar = data.get('fasting_blood_sugar')
    creatine = data.get('creatine')
    cholesterol = data.get('cholesterol')
    return all([
        vitamin_b12,
        has_fasting_blood_sugar(fasting_blood_sugar),
        has_cholesterol(cholesterol),
        creatine,
    ])

def category_l(data: dict) -> bool:
    # l = vitamin_b12, thyroid, pcod, cholesterol
    vitamin_b12 = data.get('vitamin_b12')
    thyroid = data.get('thyroid')
    cholesterol = data.get('cholesterol')
    pcod_pcos = data.get('pcod_pcos')
    gender = data.get('gender')
    if gender == GENDER.female:
        return all([
            vitamin_b12,
            thyroid,
            has_cholesterol(cholesterol),
            pcod_pcos
        ])
    else:
        return all([
            vitamin_b12,
            thyroid,
            has_cholesterol(cholesterol)
        ])

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