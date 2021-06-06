########################################################################################################################
# Function: frange
# Description:
#   Creates a float range generator
# Arguments:
#   start:  Start of range
#   stop:   End of range
#   step:   Step size of range
########################################################################################################################
def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step