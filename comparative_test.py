#!/bin/python

import time

def track_time(function_to_track):
        """
        To track running time of a function
        """
        start_time=time.time()
        function_to_track
        return time.time()-start_time

def p_value(rel_stats):
        """
        To format result from scipy.stats
        """
        return float(str(rel_stats).split(",")[1].split(")")[0].split("=")[1])