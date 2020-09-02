def less_count(element1, element2):
    if int(element1['vote_count']) < int(element2['vote_count']):
        return True
    return False

def less_average(element1, element2):
    if float(element1['vote_average']) < float(element2['vote_average']):
        return True
    return False


def greater_count(element1, element2):
    return not(less_count(element1, element2))

def greater_average(element1, element2):
    return not(less_average(element1, element2))