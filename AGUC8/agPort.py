## @package agPort
# This module contain classes that implements custom versions of python built-in serial port class
# for the agilis controllers 
#

import serial as s
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

## Documentation for the AGPort class
#
# This class uses the python Serial class to provide functionality for use with the agilis controller commands
class AGPort():
    
    ## Class constructor
    # @param portName The name of the virtual serial port of the chosen controller
    def __init__(self,portName = None):
        
        if portName == None:
            ## @var AGPort.soul
            self.soul = None
            return None
        try:
            logger.debug('Opening serial communication..')
            self.url = "socket://" + portName
            self.ser = s.serial_for_url(self.url,115200,s.EIGHTBITS,s.PARITY_NONE,s.STOPBITS_ONE, timeout=1)
            self.soul = 'p'
            logger.info('Serial communcation opened with ' + self.url)
        except Exception as e:
            print('I could not find or open the port you specified: {0}'.format(portName))
            self.soul = None
            return None
    
        
    def amInull(self):
        return self.soul is None
    
    
    def isAquery(self,command):
        
        if self.amInull():
            return False
        
        queryOnly=["?","PH","TE","TP","TS","VE"]
        command = command.upper()
        for q in queryOnly:
            if command.find(q) != -1:
                return True
        return False
    
    
    def sendString(self, command):
        
        response = ''
        logger.debug('sent: ' + repr(command))
        bCommand = command.encode('utf-8')
        self.ser.write(bCommand)
        if self.isAquery(command):
            try:
                response = self.ser.readline().decode('utf-8')
                logger.debug('received: ' + repr(response))
                return response[:-2]
            except:
                print('Serial Timeout')
                return 0

    def close(self):
        logger.debug('Closing serial communication..')
        self.ser.close()
        logger.info('Serial communication with ' + self.url + ' is closed.')
    
 
