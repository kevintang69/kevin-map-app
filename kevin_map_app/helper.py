import os
from kevin_map_app.pygmaps import pygmaps
import datetime

#local: C:\Users\Kevin  CWD
#c:\Users\Kevin\Desktop\web dev\new app\kevin_map_app  DIR_PATH

#web: /app CWD
# /app/kevin_map_app DIR_PATH

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
STATIC_DIRECTORY = DIR_PATH + '/static/'


def return_file_path(name):
    return DIR_PATH + '/' + name


def check_input(s):
    if len(s)<3:
        return False
    
    if s[-1] == '|':
        s = s[:len(s)-1]
    if s[0] == '|':
        s = s[1:]
    


    no_spaces = ''
    for char in s:
        if char != ' ' and char != '':
            no_spaces += char

    if '|' not in no_spaces:
        try:
            lat,lng = no_spaces.split(',')
        except:
            return False
        return [( float( lat),  float(lng))]
    else:

        try:
            latlng_list =  no_spaces.split('|')
        except:
            return False
        try:
            path = []
            for pair in latlng_list:
                lat, lng = pair.split(',')

                
                path.append(  (float(lat),float(lng) )   )
            return path
        except:
            return False


def clean_string(s):
    new_string = ''
    new_list = check_input(s)
    for item in new_list:
        new_string+= f'{item[0]},{item[1]}|'
    return new_string[:-1]



def find_center_location(l):
    total_lat =0
    total_lng = 0
    for tup in l:
        total_lat += tup[0] /len(l)
        total_lng += tup[1] / len(l)
    return total_lat, total_lng






def zeropad(n):
    if int(n)  <10:
        return f"0{n}"
    else:
        return f"{n}"

def get_time_string(tob):
    return f'{zeropad(tob.month)}-{zeropad(tob.day)}-{zeropad(tob.year)}-{zeropad(tob.hour)}-{zeropad(tob.minute)}-{zeropad(tob.second)}'

def create_time_object(s):
    month = int(s[0:2])
    day =int( s[3:5])
    year = int( s[6:10])
    hour = int(s[11:13] )
    minute = int(s[14:16])
    second = int(s[17:19])
    return datetime.datetime(year,month,day,hour,minute,second)




def remove_file(location):
    if os.path.exists(STATIC_DIRECTORY+location):
        os.remove(STATIC_DIRECTORY+location)




def create_map(username, time_ob, coord_string ):
    path = check_input(coord_string)

    time_string = get_time_string(time_ob)
    name_of_run = username+ '_'+   time_string   + '_' +  coord_string +".html"
    avg_lat , avg_lng = find_center_location(path)
    mymap = pygmaps(avg_lat, avg_lng, 5)
    for pair in path:
        mymap.addpoint( pair[0],pair[1]  )
    
    if len(path) >=2 :
        mymap.addpath(path)

    remove_file(STATIC_DIRECTORY + name_of_run)
    mymap.draw(STATIC_DIRECTORY+name_of_run)
    return name_of_run


def find_median(l):
    if len(l)%2==0:
        return 0.5*l[len(l)//2-1] + 0.5*l[len(l)//2]
    else:
        return l[len(l)//2]

def IQR(l):
    l = l.copy().sorted()
    ori = l.copy()
    dic = {'middle75':[] , 'outliers':[]}
    median = find_median(l)
    size = len(l)
    if size%2==1:
        l = l.copy()
        del l[size//2]
    first_half = l[:size//2]
    second_half = l[size//2:]
    first_quartile = find_median(first_half)
    third_quartile = find_median(second_half)
    IQR = third_quartile-first_quartile
    lower_limit = first_quartile - 1.5* IQR
    upper_limit = third_quartile + 1.5* IQR
    
    for point in ori:
        if point >= first_quartile and point <= third_quartile:
            dic['middle75'].append( point)
        elif point < lower_limit or point > upper_limit:
            dic['outliers'].append(point)
    dic['median'] = median
    dic['IQR'] = IQR
    dic['first_quartile'] = first_quartile
    dic['third_quartile'] = third_quartile
    return dic
    
    

    