def add_slider(original, horizontal, vertical):
    original[0] += horizontal
    original[1] += vertical
    return original

def distance_cor(original, amount):
    return original + int(amount) * 5

def angle_cor(original, distance, amount):
    return original + (int(amount) * 5) / distance
