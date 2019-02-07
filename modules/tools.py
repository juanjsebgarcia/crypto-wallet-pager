
def pretty_output(input):
    '''
    Prune input to two decimal places and add thousand comma seperators
    '''
    output = format(input, '.2f')
    output = '{:,}'.format(float(output))
    return output
