#
# Copyright (C) 2015-2016 Ettore Landini
#
# This code is translated from another project of mines written in C#
#
# This is a python library for the NewPort Agilis controlle agUC2 and agUC8
#
# You can find another approach to this problem here: http://nullege.com/codes/show/src@t@e@terapy-2.00b6
#
#
#

from AGUC8.channel import Axis,RATE
from AGUC8.mothreading import MotorThread

from AGUC8.agPort import AGPort

import logging

logger = logging.getLogger(__name__)

class AGUC8(object):
    """Class that builds support for Agilis AGUC8 piezo motor controller. Creates an instance of a serial
    object using :class:`AGPort`
    
    :param portName: <host>:<port> (See pySerial's serial_for_url documentation. Uses the socket:// URL.)
    :portName type: str
    :param activeChannels: List of active channels on the AGUC8 controller. Defaults to ['1'].
    :activeChannels type: list, optional
    :param axis1alias: Alias for Axis 1. Defualts to 'X'.
    :axis1alias type: str
    :param axis2alias: Alias for Axis 2. Defualts to 'Y'.
    :axis2alias type: str
    :param stepAmp1: Axis 1 step amplitude. See AGUC8 docs. Defaults to 50.
    :stepAmp1 type: int
    :param stepAmp2: Axis 2 step amplitude. See AGUC8 docs. Defaults to 50.
    :stepAmp2 type: int
    """
    
    def __init__(self,portName,activeChannels = ['1'], axis1alias = 'X', axis2alias = 'Y', stepAmp1 = 50, stepAmp2 = 50):
        """Constructor method
        """
        
        self.port = AGPort(portName)
        self.channels = {'1':{axis1alias:None,axis2alias:None},
                         '2':{axis1alias:None,axis2alias:None},
                         '3':{axis1alias:None,axis2alias:None},
                         '4':{axis1alias:None,axis2alias:None}}
        
        self.aliases = [axis1alias,axis2alias]
        
        self.defChannel = activeChannels[0]
        
        if not self.port.amInull():
            deviceName = self.port.sendString('VE\r\n')
            logger.info('Device name: ' + deviceName)
            logger.debug('Setting device to remote mode')
            self.port.sendString('MR\r\n')
            for c in activeChannels:
                logger.debug('Configuring channel ' + str(c))
                self.port.sendString('CC'+str(c)+'\r\n')
                self.addAxis(c,'1',axis1alias,stepAmp1)
                logger.info('Channel ' + c + ': ' + axis1alias + ' axis given step amplitude ' + str(stepAmp1))
                self.addAxis(c,'2',axis2alias,stepAmp2)
                logger.info('Channel ' + c + ': ' + axis2alias + ' axis given step amplitude ' + str(stepAmp2))
            logger.info('Changing to channel ' + str(activeChannels[0]))
            self.port.sendString('CC'+str(activeChannels[0])+'\r\n')

            # Does a device have a limit switch?
            self._limit_status = self.port.sendString('PH\r\n')[2]

            logger.debug('Starting motor thread')
            self.mThread = MotorThread()
        
    def close(self):
        """Close serial connection."""
        self.port.close()
        
    def chchch(self,ch):
        """CHeck and CHange CHannel.
        Changes to channel ch if it isn't already active.

        :param ch: Desired channel number
        :type ch: str
        """
        
        channel = int(self.port.sendString('CC?\r\n')[2:])
        if channel != ch:
            logger.info('Changing to channel ' + str(ch))
            self.port.sendString('CC'+str(ch)+'\r\n')
        
        
    def addAxis(self,channel,name,alias,stepAmp):
        """Assigns an axis to a channel.

        :param channel: Channel number
        :channel type: str
        :param name: Axis number
        :name type: str
        :param alias: Axis alias
        :alias type: str
        :param stepAmp: Axis step amplitude
        :stepAmp type: int
        """
        
        if alias not in self.aliases:
            raise KeyError('You used an invalid axis name')
        self.channels[channel][alias] = Axis(name,stepAmp,controller = self)
    
    
    def move(self,d1,d2,ch='def'):
        """Relative move.

        :param d1: Axis 1 relative position
        :d1 type: int
        :param d2: Axis 2 relative position
        :d2 type: int
        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        logger.info('Moving to relative position: (' + str(d1) + ', ' + str(d2) + ')')
        self.channels[ch][self.aliases[0]].jog(d1)
        self.channels[ch][self.aliases[0]].amIstill(100)
        self.channels[ch][self.aliases[1]].jog(d2)
        self.channels[ch][self.aliases[1]].amIstill(100)
        
    
    def moveUpUp(self,ch='def'):
        """Move to Axis 1 maximum, Axis 2 maximum.

        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
  
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)

        if self._limit_status == ch:        
            logger.info('Moving to: ' + self.aliases[0] + ' axis max, ' + self.aliases[1] + ' axis max')
            self.channels[ch][self.aliases[0]].goMax()
            self.channels[ch][self.aliases[0]].amIstill(RATE)
            self.channels[ch][self.aliases[1]].goMax()
            self.channels[ch][self.aliases[1]].amIstill(RATE)
        else:
            logger.warning('The device on the specified channel has no active limit switch.')
            return
        
        
    def moveDownDown(self,ch='def'):
        """Move to Axis 1 minimum, Axis 2 minimum.

        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)

        if self._limit_status == ch:        
            logger.info('Moving to: ' + self.aliases[0] + ' axis min, ' + self.aliases[1] + ' axis min')
            self.channels[ch][self.aliases[0]].goMin()
            self.channels[ch][self.aliases[0]].amIstill(RATE)
            self.channels[ch][self.aliases[1]].goMin()
            self.channels[ch][self.aliases[1]].amIstill(RATE)
        else:
            logger.warning('The device on the specified channel has no active limit switch.')
            return
        
        
    def moveDownUp(self,ch='def'):
        """Move to Axis 1 minimum, Axis 2 maximum.

        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)

        if self._limit_status == ch:
            logger.info('Moving to: ' + self.aliases[0] + ' axis min, ' + self.aliases[1] + ' axis max')
            self.channels[ch][self.aliases[0]].goMin()
            self.channels[ch][self.aliases[0]].amIstill(RATE)
            self.channels[ch][self.aliases[1]].goMax()
            self.channels[ch][self.aliases[1]].amIstill(RATE)
        else:
            logger.warning('The device on the specified channel has no active limit switch.')
            return
        
        
    def moveUpDown(self,ch='def'):
        """Move to Axis 1 maximum, Axis 2 minimum.

        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        if self._limit_status == ch:
            logger.info('Moving to: ' + self.aliases[0] + ' axis max, ' + self.aliases[1] + ' axis min')
            self.channels[ch][self.aliases[0]].goMax()
            self.channels[ch][self.aliases[0]].amIstill(RATE)
            self.channels[ch][self.aliases[1]].goMin()
            self.channels[ch][self.aliases[1]].amIstill(RATE)
        else:
            logger.warning('The device on the specified channel has no active limit switch.')
            return
        

    def goToZero(self,ch='def'):
        """Move to the zero position. If zero position hasn't been defined,
        it will move to the initial position of the device when powered on.

        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)
        
        steps1 = self.channels[ch][self.aliases[0]].queryCounter()
        steps2 = self.channels[ch][self.aliases[1]].queryCounter()

        logger.info('Moving to zero position: relative position (' + str(steps1) + ', ' + str(steps2) + ')')
        
        self.channels[ch][self.aliases[0]].jog(-1*steps1)
        self.channels[ch][self.aliases[0]].amIstill(150)
        self.channels[ch][self.aliases[1]].jog(-1*steps2)
        self.channels[ch][self.aliases[1]].amIstill(150)
        
    
    def setZero(self,ch='def'):
        """Set the zero position to the current position.

        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)

        logger.info('Setting zero position to current position')
        
        self.channels[ch][self.aliases[0]].resetCounter()
        self.channels[ch][self.aliases[1]].resetCounter()
        
        
    def stop(self,ch='def'):
        """Stop ongoing motion.

        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)

        logger.info('Stopping ongoing motion')
        
        if self.mThread.isAlive():
            self.mThread.stop_at_next_check = True
            while self.mThread.isAlive():
                continue
            self.mThread = MotorThread()
        self.channels[ch][self.aliases[0]].stop()
        self.channels[ch][self.aliases[1]].stop()
        
    
    def followApath(self,path,ch='def'):
        """Follow a path.

        :param path: Path to be followed. List of tuples defining relative moves.
        :path type: list
        :param ch: Channel number. Defaults to 'def' and uses self.defChannel.
        :ch type: str, optional
        """
        
        if ch == 'def':
            ch = ch=self.defChannel
        self.chchch(ch)

        logger.info('Following a path')
        
        steps = []
        for p in path:
            step = lambda: self.move(ch,p[0], p[1])
            steps.append(step)
        self.mThread.steps = steps
        self.mThread.start()
