############################################################################################################################################
# Author: Patrick Cemper
# Date: June 18th, 2018
############################################################################################################################################


def init():
    """This is the init method for global constants. Please feel free to modify these in case your machine doesn't work as fast or
    as slow as mine. PROCESSING_DIFFICULTY must be increased when the workers find the result too fast, otherwise it must be
    decreased. PRINTING_TIME should stay rather high so we see the wanted effect of after-work when all is found for the transaction
    but message printing and tracking is still ongoing."""

    global PROCESSING_DIFFICULTY
    PROCESSING_DIFFICULTY = 1500000000
    global PRINTING_TIME
    PRINTING_TIME = 12
