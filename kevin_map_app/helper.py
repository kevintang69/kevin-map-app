import os
from kevin_map_app.pygmaps import pygmaps

#local: C:\Users\Kevin  CWD
#c:\Users\Kevin\Desktop\web dev\new app\kevin_map_app  DIR_PATH

#web: /app CWD
# /app/kevin_map_app DIR_PATH

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_DIRECTORY = DIR_PATH + '/static/'



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



def remove_file(location):
    if os.path.exists(STATIC_DIRECTORY+location):
        os.remove(STATIC_DIRECTORY+location)




def create_map(username, time_ob, coord_string ):
    path = parse_coordinates(coord_string)
    time_string = get_time_string(time_ob)
    name_of_run = username+ '_'+   time_string   +".html"
    avg_lat , avg_lng = find_center_location(path)
    mymap = pygmaps(avg_lat, avg_lng, 5)
    mymap.addpath(path,"#FF0000")
    remove_file(STATIC_DIRECTORY + name_of_run)
    mymap.draw(STATIC_DIRECTORY+name_of_run)
    return name_of_run