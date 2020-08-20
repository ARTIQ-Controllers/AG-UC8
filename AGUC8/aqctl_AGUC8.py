#!/usr/bin/env python3

import argparse
import logging
import sys

from sipyco.pc_rpc import simple_server_loop
from sipyco import common_args

from AGUC8 import driver

logger = logging.getLogger(__name__)

class Motor():
    """Class for providing remote functionality of AGUC8 controller.

    A Motor instance can be initialized using the desired port.
    If no serial number is specified, it connects to the port specified by the "self.port" variable.

    :param port: Serial port (Uses pySerial serial_for_url)
    Defaults to None if not specified. In that case, it will use self.port.
    :port type: str, optional
    """

    def __init__(self, port=None):
        """Constructor method
        """
        if port is None:
            self.port = "socket://192.168.1.220:10001"
        else:
            self.port = port
        self._connect()

    def _connect(self):
        self.drv = driver.AGUC8(self.port)

    def move(self, d1, d2):
        """Moves to the relative location specified by coordinates (d1,d2).
        
        :param d1: Axis 1 relative location
        :d1 type: int
        :param d2: Axis 2 relative location
        :d2 type: int
        """
        self.drv.move(d1, d2)

    def moveUpUp(self):
        """Moves to Axis 1 maximum, Axis 2 maximum.
        """
        self.drv.moveUpUp()

    def moveDownDown(self):
        """Moves to Axis 1 minimum, Axis 2 minimum.
        """
        self.drv.moveDownDown()

    def moveDownUp(self):
        """Moves to Axis 1 minimum, Axis 2 maximum.
        """
        self.drv.moveDownUp()

    def moveUpDown(self):
        """Moves to Axis 1 maximum, Axis 2 minimum.
        """
        self.drv.moveUpDown()

    def goToZero(self):
        """Moves to the the zero position. If this point has not been specified, it moves to
        the initial position of the device when powered on.
        """
        self.drv.goToZero()

    def setZero(self):
        """
        Set the zero position to the current position.
        """
        self.drv.setZero()

    def followApath(self, path):
        """Sequentially moves to each relative location specified in path.
        
        :param path: List of tuples specifying the coordinates of each relative move.
        :path type: list
        """
        self.drv.followApath(self, path)

    def close(self):
        """Close serial connection.
        """
        self.drv.close()


def get_argparser():
    parser = argparse.ArgumentParser(description="""Agilis AG-UC8 controller.

    Use this controller to drive the AG-UC8 piezo motor controller.""")
    common_args.simple_network_args(parser, 3251)
    parser.add_argument("-s", "--serialPort", default=None,
                        help="Serial port. See documentation for how to specify port.")
    common_args.verbosity_args(parser)
    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)

    if not args.serialPort:
        print("You need to specify -s")
        sys.exit(1)

    motor = Motor(args.serialPort)
    
    try:
        logger.info("AG-UC8 open. Serving...")
        simple_server_loop({"AGUC8": motor}, common_args.bind_address_from_args(args), args.port)
    finally:
        motor.close()

if __name__ == "__main__":
    main()
