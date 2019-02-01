CT_WHITE = (1.0, 1.0, 1.0, 1.0)
CT_RED = (1.0, 0.5, 0.5, 1.0)
CT_BROWN = (0.64100000000000001, 0.35499999999999998, 0.27000000000000002, 1.0)
CT_CANTELOPE = (
    0.83899999999999997,
    0.65100000000000002,
    0.54900000000000004,
    1.0)
CT_TAN = (0.996, 0.69499999999999995, 0.51200000000000001, 1.0)
CT_ORANGE = (
    0.99199999999999999,
    0.47999999999999998,
    0.16800000000000001,
    1.0)
CT_CORAL = (0.83199999999999996, 0.5, 0.29699999999999999, 1.0)
CT_PEACH = (1.0, 0.81999999999999995, 0.69999999999999996, 1.0)
CT_BEIGE = (1.0, 0.80000000000000004, 0.59999999999999998, 1.0)
CT_TAN2 = (0.80800000000000005, 0.67800000000000005, 0.51000000000000001, 1.0)
CT_SIENNA = (
    0.56999999999999995,
    0.44900000000000001,
    0.16400000000000001,
    1.0)
CT_YELLOW = (0.996, 0.89800000000000002, 0.32000000000000001, 1.0)
CT_CREAM = (0.996, 0.95699999999999996, 0.59799999999999998, 1.0)
CT_BEIGE2 = (1.0, 1.0, 0.59999999999999998, 1.0)
CT_YELLOW2 = (1.0, 1.0, 0.69999999999999996, 1.0)
CT_CITRINE = (
    0.85499999999999998,
    0.93400000000000005,
    0.49199999999999999,
    1.0)
CT_FOREST_GREEN = (0.5, 0.58599999999999997, 0.40000000000000002, 1.0)
CT_LINE = (0.55100000000000005, 0.82399999999999995, 0.32400000000000001, 1.0)
CT_PALE_GREEN = (0.78900000000000003, 1.0, 0.69999999999999996, 1.0)
CT_GREEN = (0.30499999999999999, 0.96899999999999997, 0.40200000000000002, 1.0)
CT_TEAL = (0.59999999999999998, 1.0, 0.80000000000000004, 1.0)
CT_SEA_GREEN = (
    0.24199999999999999,
    0.74199999999999999,
    0.51600000000000001,
    1.0)
CT_LIGHT_BLUE = (0.434, 0.90600000000000003, 0.83599999999999997, 1.0)
CT_AQUA = (0.34799999999999998, 0.81999999999999995, 0.95299999999999996, 1.0)
CT_BLUE = (0.191, 0.56299999999999994, 0.77300000000000002, 1.0)
CT_LIGHT_BLUE2 = (0.875, 0.93700000000000006, 1.0, 1.0)
CT_PERIWINKLE = (0.55900000000000005, 0.58999999999999997, 0.875, 1.0)
CT_ROYAL_BLUE = (
    0.28499999999999998,
    0.32800000000000001,
    0.72699999999999998,
    1.0)
CT_GREY = (0.69999999999999996, 0.69999999999999996, 0.80000000000000004, 1.0)
CT_BLUE2 = (0.59999999999999998, 0.59999999999999998, 1.0, 1.0)
CT_SLATE_BLUE = (0.46100000000000002, 0.379, 0.82399999999999995, 1.0)
CT_PURPLE = (0.54700000000000004, 0.28100000000000003, 0.75, 1.0)
CT_LAVENDER = (
    0.72699999999999998,
    0.47299999999999998,
    0.85899999999999999,
    1.0)
CT_PINK = (0.89800000000000002, 0.61699999999999999, 0.90600000000000003, 1.0)
CT_PINK2 = (1.0, 0.59999999999999998, 1.0, 1.0)
CT_MAROON = (0.71099999999999997, 0.23400000000000001, 0.438, 1.0)
CT_PEACH2 = (
    0.96899999999999997,
    0.69099999999999995,
    0.69899999999999995,
    1.0)
CT_RED2 = (0.86299999999999999, 0.40600000000000003, 0.41799999999999998, 1.0)
CT_BRIGHT_RED = (
    0.93400000000000005,
    0.26600000000000001,
    0.28100000000000003,
    1.0)
CT_DARK_WOOD = (
    0.68999999999999995,
    0.74099999999999999,
    0.70999999999999996,
    1.0)
CT_DARK_WALNUT = (
    0.54900000000000004,
    0.41199999999999998,
    0.25900000000000001,
    1.0)
CT_GENERIC_DARK = (0.443, 0.33300000000000002, 0.17599999999999999, 1.0)
CT_PINE = (1.0, 0.81200000000000006, 0.48999999999999999, 1.0)
CT_CHERRY = (
    0.70999999999999996,
    0.40799999999999997,
    0.26700000000000002,
    1.0)
CT_BEECH = (0.96099999999999997, 0.65900000000000003, 0.40000000000000002, 1.0)
CTFlatColor = [
    CT_BEIGE,
    CT_TEAL,
    CT_BLUE2,
    CT_PINK2,
    CT_BEIGE2,
    CT_RED]
CTValentinesColors = [
    CT_PINK2,
    CT_RED]
CTUnderwaterColors = [
    CT_WHITE,
    CT_TEAL,
    CT_SEA_GREEN,
    CT_LIGHT_BLUE,
    CT_PALE_GREEN,
    CT_AQUA,
    CT_CORAL,
    CT_PEACH]
CTFlatColorDark = []
tint = 0.75
for color in CTFlatColor:
    CTFlatColorDark.append(
        (color[0] * tint,
         color[1] * tint,
         color[2] * tint,
         1.0))

CTFlatColorAll = CTFlatColor + CTFlatColorDark
CTBasicWoodColorOnWhite = [
    CT_DARK_WALNUT,
    CT_GENERIC_DARK,
    CT_PINE,
    CT_CHERRY,
    CT_BEECH]
CTWhite = [
    CT_WHITE]
