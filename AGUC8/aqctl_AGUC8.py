#!/usr/bin/env python3

import argparse
import logging

from sipyco.pc_rpc import simple_server_loop
from sipyco import common_args

from AGUC8 import driver

logger = logging.getLogger(__name__)

class Motor():
    """Class for providing functionality of piezo mount remotely.

    A Motor instance can be initialised using the desired port.
    If no serial number is specified, it connects to the port specified by the "self.port" variable.
    """

    def __init__(self, port=None):
        if port is None:
            self.port = "192.168.1.220:10001"
        else:
            self.port = port
        self._connect()

    def _connect(self):
        self.drv = driver.AGUC8(self.port)

    def move(self, d1, d2):
        """
        Moves to the relative location specified by coordinates (d1,d2).
        
        :param int d1: Number of steps in the x-direction.
        :param int d2: Number of steps in the y-direction.
        """
        self.drv.move(d1, d2)

    def moveUpUp(self):
        """
        Moves to the upper limit in both the x-direction and y-direction.
        """
        self.drv.moveUpUp()

    def moveDownDown(self):
        """
        Moves to the lower limit in both the x-direction and y-direction.
        """
        self.drv.moveDownDown()

    def moveDownUp(self):
        """
        Moves to the lower limit in the x-direction and the upper limit in the y-direction.
        """
        self.drv.moveDownUp()

    def moveUpDown(self):
        """
        Moves to the upper limit in the x-direction and the lower limit in the y-direction.
        """
        self.drv.moveUpDown()

    def goToZero(self):
        """
        Moves to the the "zero" point. If this point has not been specified since the device was powered on,
        it will move to the initial point when powered on.
        """
        self.drv.goToZero()

    def setZero(self):
        """
        Set the "zero" point.
        """
        self.drv.setZero()

    def stop(self):
        """
        Stops any ongoing motion.
        """
        self.drv.stop()

    def followApath(self, path):
        """
        Sequentially moves to each relative location specified in path.
        
        :param list path: List of tuples specifying the coordinates of each relative move.
        """
        self.drv.followApath(self, path)

    def close(self):
        self.drv.close()


def get_argparser():
    parser = argparse.ArgumentParser(description="""Agilis AG-UC8 controller.

    Use this controller to drive the AG-UC8 piezo motor controller.""")
    common_args.simple_network_args(parser, 3251)
    parser.add_argument("-s", "--serialPort", default=None,
                        help="Serial port. Defaults to None if not used. See documentation.")
    common_args.verbosity_args(parser)
    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)

    motor = Motor(args.serialPort)
    
    try:
        logger.info("AG-UC8 open. Serving...")
        simple_server_loop({"motor": motor}, common_args.bind_address_from_args(args), args.port)
    finally:
        motor.close()

if __name__ == "__main__":
    main()
