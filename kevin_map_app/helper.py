def find_center_location(l):
    total_lat =0
    total_lng = 0
    for tup in l:
        total_lat += tup[0] /len(l)
        total_lng += tup[1] / len(l)
    return total_lat, total_lng




def parse_coordinates(s):
    answer = []
    coordlist = s.split('|')
    for coord in coordlist:
        lat,lng = coord.split(',')
        answer.append( (float(lat), float(lng)) )
    return answer



def get_time_string(tob):
    return f'{tob.month}-{tob.day}-{tob.year}-{tob.hour}-{tob.minute}-{tob.second}'