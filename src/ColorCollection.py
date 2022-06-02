color_collection = []

def in_collection(color) -> bool:
    answer = False
    for c in color_collection:
        if color == c:
            answer = True
            return answer
    color_collection.append(color)
    return answer