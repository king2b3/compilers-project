''' Simple timer data structure
'''

class Timer():
    def __init__(
        self
    ):
    '''
        Timer class to track and report time usage to print
    '''
        import time
        self.start_time = 0
        self.end_time = 0

    def start_timer(
        self
    ) -> None:
        ''' Records the start of a timer and resest both the start / end
        '''
        self.start_timer = time.time()

    def end_timer(
        self
    ) -> None:
        ''' Records the end value of a timer
        '''
        self.end_timer = time.time()

    def __str__(
        self
    ) -> float:
        ''' Returns the End - Start.
        '''
        return self.end-time - self.start_time