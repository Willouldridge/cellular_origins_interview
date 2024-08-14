from enum import Enum
from typing import Tuple
import logging

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

class MarsRover(object):
    """A toy robot Mars Rover that can move around a grid of predetermined size.

    Attributes:
        x_pos - the position of the rover on the x axis - can be None if the rover has not been placed
        y_pos - the position of the rover on the y axis - can be None if the rover has not been placed
        facing - the direction the rover is facing in. This is a value from the Direction Enum. Can be None if the rover has not been placed
        placed - indicates whether the rover has been placed yet
        x_max - the maximum position possible on the x axis for this rover
        y_max - the maximum position possible on the y axis for this rover
    """

    def __init__ (self,
                  x_pos: int = 0,
                  y_pos: int = 0,
                  x_max: int = 4,
                  y_max: int = 4,
                  facing: str = 'NORTH',
                  placed: bool = False):
        """Initialise class attributes and place the rover if needed.
        """
        logging.basicConfig(filename='MarsRover.log', filemode='w', level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info('Initialising Mars Rover')
        self.x_pos = None
        self.y_pos = None
        self.facing = None
        self.x_max = x_max
        self.y_max = y_max
        self.placed = False

        if placed and not self._place_rover(x_pos, y_pos, facing):
            raise Exception("Invalid initial placement")

        self.logger.info('Initialised Mars Rover, board dimensions {} x {}'
                    .format(self.x_max, self.y_max))

    def _parse_place_command(self, command: str) -> Tuple[int, int, str]:
        """Parse a PLACE command. The command must take the format:
            'PLACE X,Y,F'
           where X,Y are integer coordinates and F is a direction (e.g. NORTH).
           This method will not enforce the direction is a valid direction.

        Returns a tuple (int(X), int(Y), F) for valid inputs. None otherwise.
        """
        self.logger.info("Parsing PLACE command {}".format(command))
        split_command = command.split(" ")
        if len(split_command) < 2:
            self.logger.error("PLACE command does not contain coordinates")
            return None
        elif len(split_command) > 2:
            self.logger.error("PLACE command includes unrecognised arguments")
            return None

        if split_command[0] != "PLACE":
            self.logger.error("Invalid command for PLACE operation")
            return None

        arguments = split_command[1].split(",")
        if len(arguments) != 3:
            self.logger.error("PLACE command includes invlaid arguments")
            return None

        try:
            return (int(arguments[0]), int(arguments[1]), arguments[2])
        except ValueError:
            self.logger.error("PLACE command includes non integer coordinates")
            return None


    def _place_rover(self, x_pos: int, y_pos: int, facing: str) -> bool:
        """Place the rover at the specified coordinates (if valid) facing the correct direction.

        Returns True if the placement is valid and the rover has been updated with this state,
        False otherwise.

        Arguments:
        x_pos - the position on the x axis to place the rover
        y_pos - the position on the y axis to place the rover
        facing - the direction the rover is facing once placed.
        """
        self.logger.info("Placing rover")

        # Verify that the arguments represent a valid placement. The robot cannot
        # be placed out of bounds or facing an unrecognised direction
        if x_pos > self.x_max or x_pos < 0 or y_pos > self.y_max or y_pos < 0:
            self.logger.error("Coordinates ({},{}) are out of bounds"
                              .format(x_pos, y_pos))
            return False

        if facing not in [d.name for d in Direction]:
            self.logger.error("Direction {} is not a valid direction".format(facing))
            return False

        # This command is a valid placement so update the position and facing of
        # the robot and indicate the robot has been placed (at least) once.
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.facing = Direction[facing].value
        self.placed = True
        self.logger.info("Successfully placed rover at ({},{}) facing {}"
                         .format(x_pos, y_pos, facing))
        return True

    def _turn_rover(self, command: str) -> bool:
        """Turn the rover left or right through 90 degrees to face a new direction.

        Returns True if the turn command is valid and the rover has been turned
        (or if the move was ignored because the rover has not been placed),
        False otherwise.

        Arguments:
        command - the turn command. This must be one of "LEFT" or "RIGHT"
        """
        self.logger.info("Turning rover")

        if not self.placed:
            self.logger.info("Rover has not yet been placed")
            return True

        if command not in ["LEFT", "RIGHT"]:
            self.logger.error("Invalid turn command {}".format(command))
            return False

        # Determine the direction we want to be turning in terms of incrementing or
        # decrementing in the Direction enum.
        direction = 1
        if command == "LEFT":
            direction = -1

        new_facing = self.facing + direction

        # If we have gone outside the bounds of the Direction enum, wrap to start from
        # the beginning again.
        if new_facing > 4:
            new_facing = 1
        elif new_facing < 1:
            new_facing = 4

        self.facing = new_facing
        self.logger.info("Successfully turned rover to face {}"
                        .format(Direction(self.facing).name))
        return True

    def _move_rover(self) -> bool:
        """Move the rover one unit in the direction it is facing if this does not result in the rover
        going out of bounds.

        Returns True if the move is successful (or if the move was ignored because the rover has not
        been placed), False otherwise
        """
        if not self.placed:
            self.logger.info("Rover has not yet been placed")
            return True

        self.logger.info("Moving rover {}".format(Direction(self.facing).name))

        # Calculate where the new position would be if the move occured and check
        # the new position is valid before comitting the move operation.
        match self.facing:
            case 1: # North - increase y
                new_x = self.x_pos
                new_y = self.y_pos + 1
            case 2: # East - increase x
                new_x = self.x_pos + 1
                new_y = self.y_pos
            case 3: # South - decrease y
                new_x = self.x_pos
                new_y = self.y_pos - 1
            case 4: # West - decrease x
                new_x = self.x_pos - 1
                new_y = self.y_pos

        if new_x < 0 or new_x > self.x_max or new_y < 0 or new_y > self.y_max:
            self.logger.error("Move would take rover out of bounds")
            return False

        self.x_pos = new_x
        self.y_pos = new_y

        self.logger.info("Successfully moved rover {} to ({},{})"
                         .format(Direction(self.facing).name, new_x, new_y))
        return True



    def _report(self) -> str:
        """Return 'X,Y,F' where X and Y are the position of the rover and F is the direction it is facing.
        """
        self.logger.info("Reporting rover position")
        if not self.placed:
            self.logger.info("Rover has not yet been placed")
            return None

        return "{},{},{}".format(self.x_pos,
                                 self.y_pos,
                                 Direction(self.facing).name)

    def recieve_command(self, command: str) -> str:
        """Process a command and perform the appropriate action.

        Returns the report if command is "REPORT". None otherwise

        Arguments:
        command - the command to follow. Must be one of:
                    PLACE X,Y,Z
                    MOVE
                    LEFT
                    RIGHT
                    REPORT

        Requests to MOVE, LEFT, RIGHT or REPORT before the rover has been placed
        with a PLACE command will be ignored.
        """
        self.logger.info('Received command {}'.format(command))
        command = command.upper()
        match command.split(" ")[0]:
            case "PLACE":
                args_tuple = self._parse_place_command(command)
                if args_tuple is None or not self._place_rover(args_tuple[0], args_tuple[1], args_tuple[2]):
                    self.logger.error("Invalid PLACE command will be ignored")
            case "MOVE":
                if not self._move_rover():
                    self.logger.error("Invalid MOVE command will be ignored")
            case "LEFT" | "RIGHT":
                if not self._turn_rover(command):
                    self.logger.error("Invalid turn command will be ignored")
            case "REPORT":
                return(self._report())
            case _:
                self.logger.error("Unrecognosed command {} will be ignored"
                                  .format(command))

        return None

