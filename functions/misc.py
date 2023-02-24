"""From an integer value, convert to minutes and seconds format"""
def beautify_time(time):
    minutes = int(int(time)/60) # Get int value for minutes
    seconds = int(int(time)%60) # Get int value for seconds
    # Prettify the values
    if (minutes == 0) :
        minutes = '00'
    elif (minutes < 10) :
        minutes = '0'+str(minutes)
    if (seconds == 0) :
        seconds = '00'
    elif (seconds < 10) :
        seconds = '0'+str(seconds)
    total_time = str(minutes)+":"+str(seconds) # Set song total time into one string from calculated minutes and seconds
    return str(total_time)