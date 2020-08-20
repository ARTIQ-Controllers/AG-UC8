## @package agPort
# This module contain classes that implements custom versions of python built-in serial port class
# for the agilis controllers 
#

import serial as s
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)


class AGPort():
    """Class that extends the functionality of :class:`Serial` for use with the Agilis controller commands.
    Creates an instance of :class:`Serial`
    
    :param portName: <host>:<port> (See pySerial's serial_for_url documentation. Uses the socket:// URL.)
    :portName type: str
    """
    
    ## Class constructor
    # @param portName The name of the virtual serial port of the chosen controller
    def __init__(self,portName = None):
        """Constructor method
        """
        
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
        """Returns whether port has been successfully opened.

        :return: True if port is open. False if not.
        :rtype: bool
        """
        return self.soul is None
    
    
    def isAquery(self,command):
        """Returns whether command is a query, as defined by Agilis command reference.

        :param command: Command to check
        :command type: str
        :return: True if command is a query. False if not.
        :rtype: bool
        """
        
        if self.amInull():
            return False
        
        queryOnly=["?","PH","TE","TP","TS","VE"]
        command = command.upper()
        for q in queryOnly:
            if command.find(q) != -1:
                return True
        return False
    
    
    def sendString(self, command):
        """Sends a serial command to the device.
        Returns a response if command is a query. Else returns 0.

        :param command: Command to send
        :command type: str
        :return: Return reponse if command is a query. Else returns 0.
        :rtype: str or int
        """
        
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
        """Close serial connection.
        """
        logger.debug('Closing serial communication..')
        self.ser.close()
        logger.info('Serial communication with ' + self.url + ' is closed.')
    
 
