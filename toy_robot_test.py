from toy_robot import Direction, MarsRover
import unittest

class TestMarsRoverMethods(unittest.TestCase):

    def _check_rover_fields(self, rover, x_pos, y_pos, x_max, y_max, facing, placed):
        self.assertEqual(rover.x_pos, x_pos)
        self.assertEqual(rover.y_pos, y_pos)
        self.assertEqual(rover.x_max, x_max)
        self.assertEqual(rover.y_max, y_max)
        self.assertEqual(rover.facing, facing)
        self.assertEqual(rover.placed, placed)

    def test_rover_initialisation(self):
        rover = MarsRover()
        self._check_rover_fields(rover, None, None, 4, 4, None, False)

    def test_rover_invalid_initialisations(self):
        try:
            rover = MarsRover(x_pos=10, y_pos=1, x_max=5, y_max=5, placed=True) # X is out of bounds
        except:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            rover = MarsRover(x_pos=1, y_pos=-1, x_max=5, y_max=5, placed=True) # Y is out of bounds
        except:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            rover = MarsRover(x_pos=1, y_pos=1, x_max=5, y_max=5, facing="SOUTHEAST", placed=True) # The facing direction is invalid
        except:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_rover_intialisation_non_default(self):
        rover = MarsRover(x_pos=4, y_pos=5, x_max=5, y_max=5, facing="EAST", placed = True)
        self._check_rover_fields(rover, 4, 5, 5, 5, Direction["EAST"].value, True)
        self.assertEqual(rover._report(), "4,5,EAST")

    def test_rover_intialisation_non_default_not_placed(self):

        # Initialisation with invalid combinations of arguments is successful if the rover is not placed on init
        rover = MarsRover(x_pos=10, y_pos=10, x_max=5, y_max=5, facing="SOUTHEAST")
        self._check_rover_fields(rover, None, None, 5, 5, None, False)

    def test_rover_place_parser(self):
        rover = MarsRover()
        self.assertEqual(rover._parse_place_command("PLACE 1,2,NORTH"), (1,2,"NORTH"))
        self.assertEqual(rover._parse_place_command("PLACE 14,-1,BANANAS"), (14,-1,"BANANAS")) # Valid command to parse, validy of arguments is checked in other methods
        self.assertEqual(rover._parse_place_command("PLACE 1,2 InvlaidArgument"), None) # Command includes extra parameters
        self.assertEqual(rover._parse_place_command("PLACE 1,2,NORTH,InvlaidArgument"), None) # command includes too many arguments
        self.assertEqual(rover._parse_place_command("PLACE"), None) # Command does not include placement arguments
        self.assertEqual(rover._parse_place_command("PLACE 1, 2, NORTH"), None) # Arguments formatted incorrectly
        self.assertEqual(rover._parse_place_command("PLACE string1,string2,NORTH"), None) # Position arguments are not integers
        self.assertEqual(rover._parse_place_command("place 1,2,NORTH"), None) # Incorrectly formatted command name

    def test_rover_place(self):
        rover = MarsRover()
        self.assertTrue(rover._place_rover(3, 4, "SOUTH"))
        self._check_rover_fields(rover, 3, 4, 4, 4, Direction["SOUTH"].value, True)
        self.assertTrue(rover._place_rover(1, 2, "NORTH"))
        self._check_rover_fields(rover, 1, 2, 4, 4, Direction["NORTH"].value, True)
        self.assertTrue(rover._place_rover(4, 3, "EAST"))
        self._check_rover_fields(rover, 4, 3, 4, 4, Direction["EAST"].value, True)
        self.assertTrue(rover._place_rover(2, 1, "WEST"))
        self._check_rover_fields(rover, 2, 1, 4, 4, Direction["WEST"].value, True)

    def test_rover_place_invalid(self):
        rover = MarsRover()
        self.assertFalse(rover._place_rover(5, 4, "WEST")) # X is out of bounds
        self._check_rover_fields(rover, None, None, 4, 4, None, False)
        self.assertFalse(rover._place_rover(4, 5, "WEST")) # Y is out of bounds
        self._check_rover_fields(rover, None, None, 4, 4, None, False)
        self.assertFalse(rover._place_rover(4, 4, "SOUTHWEST")) # The direction is invalid
        self._check_rover_fields(rover, None, None, 4, 4, None, False)
        self.assertFalse(rover._place_rover(-1, 1, "NORTH")) # X is out of bounds
        self._check_rover_fields(rover, None, None, 4, 4, None, False)
        self.assertFalse(rover._place_rover(1, -1, "NORTH")) # Y is out of bounds
        self._check_rover_fields(rover, None, None, 4, 4, None, False)

    def test_rover_turn_not_placed(self):

        # Initialise a rover that not placed. Calling turn should succeed with no effect
        rover = MarsRover()
        self._check_rover_fields(rover, None, None, 4, 4, None, False)
        self.assertTrue(rover._turn_rover("LEFT"))
        self._check_rover_fields(rover, None, None, 4, 4, None, False)

    def test_rover_right_turn_placed(self):

        # Initialise a rover facing EAST and turn right 4 times to go through each of the
        # directions and back to EAST
        rover = MarsRover(x_pos=4, y_pos=4, facing="EAST", placed = True)
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["EAST"].value, True)
        self.assertTrue(rover._turn_rover("RIGHT")) # EAST -> SOUTH
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["SOUTH"].value, True)
        self.assertTrue(rover._turn_rover("RIGHT")) # SOUTH -> WEST
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["WEST"].value, True)
        self.assertTrue(rover._turn_rover("RIGHT")) # WEST -> NORTH
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["NORTH"].value, True)
        self.assertTrue(rover._turn_rover("RIGHT")) # NORTH -> EAST
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["EAST"].value, True)

    def test_rover_left_turn_placed(self):

        # Initialise a rover facing EAST and turn left 4 times to go through each of the
        # directions and back to EAST
        rover = MarsRover(x_pos=4, y_pos=4, facing="EAST", placed = True)
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["EAST"].value, True)
        self.assertTrue(rover._turn_rover("LEFT")) # EAST -> NORTH
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["NORTH"].value, True)
        self.assertTrue(rover._turn_rover("LEFT")) # NORTH -> WEST
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["WEST"].value, True)
        self.assertTrue(rover._turn_rover("LEFT")) # WEST -> SOUTH
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["SOUTH"].value, True)
        self.assertTrue(rover._turn_rover("LEFT")) # SOUTH -> EAST
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["EAST"].value, True)

    def test_rover_invalid_turn_placed(self):
        rover = MarsRover(x_pos=4, y_pos=4, facing="EAST", placed = True)
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["EAST"].value, True)
        self.assertFalse(rover._turn_rover("UP")) # Invlaid turn direction
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["EAST"].value, True)

    def test_rover_move_not_placed(self):

        # Initialise a rover that not placed. Calling move should succeed with no effect
        rover = MarsRover()
        self._check_rover_fields(rover, None, None, 4, 4, None, False)
        self.assertTrue(rover._move_rover())
        self._check_rover_fields(rover, None, None, 4, 4, None, False)

    def test_rover_move_north(self):

        # Initialise a rover that is 1 step away from the NORTH side of the board
        rover = MarsRover(x_pos=4, y_pos=3, facing="NORTH", placed = True)
        self._check_rover_fields(rover, 4, 3, 4, 4, Direction["NORTH"].value, True)

        # Move 1 step NORTH, this should succeed
        self.assertTrue(rover._move_rover())
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["NORTH"].value, True)

        # Attempt another move NORTH which would take the rover out of bounds
        self.assertFalse(rover._move_rover())
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["NORTH"].value, True)

    def test_rover_move_east(self):

        # Initialise a rover that is 1 step away from the EAST side of the board
        rover = MarsRover(x_pos=3, y_pos=4, facing="EAST", placed = True)
        self._check_rover_fields(rover, 3, 4, 4, 4, Direction["EAST"].value, True)

        # Move 1 step EAST, this should succeed
        self.assertTrue(rover._move_rover())
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["EAST"].value, True)

        # Attempt another move EAST which would take the rover out of bounds
        self.assertFalse(rover._move_rover())
        self._check_rover_fields(rover, 4, 4, 4, 4, Direction["EAST"].value, True)

    def test_rover_move_south(self):

        # Initialise a rover that is 1 step away from the SOUTH side of the board
        rover = MarsRover(x_pos=0, y_pos=1, facing="SOUTH", placed = True)
        self._check_rover_fields(rover, 0, 1, 4, 4, Direction["SOUTH"].value, True)

        # Move 1 step SOUTH, this should succeed
        self.assertTrue(rover._move_rover())
        self._check_rover_fields(rover, 0, 0, 4, 4, Direction["SOUTH"].value, True)

        # Attempt another move SOUTH which would take the rover out of bounds
        self.assertFalse(rover._move_rover())
        self._check_rover_fields(rover, 0, 0, 4, 4, Direction["SOUTH"].value, True)

    def test_rover_move_west(self):

        # Initialise a rover that is 1 step away from the WEST side of the board
        rover = MarsRover(x_pos=1, y_pos=0, facing="WEST", placed = True)
        self._check_rover_fields(rover, 1, 0, 4, 4, Direction["WEST"].value, True)

        # Move 1 step WEST, this should succeed
        self.assertTrue(rover._move_rover())
        self._check_rover_fields(rover, 0, 0, 4, 4, Direction["WEST"].value, True)

        # Attempt another move WEST which would take the rover out of bounds
        self.assertFalse(rover._move_rover())
        self._check_rover_fields(rover, 0, 0, 4, 4, Direction["WEST"].value, True)

    def test_rover_report(self):

        # Initialise the rover. Until it is placed, reporting should have no effect
        rover = MarsRover()
        self.assertEqual(rover._report(), None)

        # Now place the rover and report the new position
        rover._place_rover(1, 2, "NORTH")
        self.assertEqual(rover._report(), "1,2,NORTH")

        # Turn the rover to ensure we can report each direction correctly
        rover._turn_rover("RIGHT")
        self.assertEqual(rover._report(), "1,2,EAST")
        rover._turn_rover("RIGHT")
        self.assertEqual(rover._report(), "1,2,SOUTH")
        rover._turn_rover("RIGHT")
        self.assertEqual(rover._report(), "1,2,WEST")
        rover._turn_rover("RIGHT")
        self.assertEqual(rover._report(), "1,2,NORTH")

    def _test_end_to_end_scenario(self, command_list):
        return_values = []
        rover = MarsRover()
        for command in command_list:
            if command == "REPORT":
                return_values.append(rover.recieve_command(command))
            else:
                self.assertEqual(rover.recieve_command(command), None)

        return return_values

    def test_end_to_end_scenario_1(self):
        command_list = [
            "PLACE 0,0,NORTH",
            "MOVE",
            "REPORT"
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), ["0,1,NORTH"])

    def test_end_to_end_scenario_2(self):
        command_list = [
            "PLACE 0,0,NORTH",
            "LEFT",
            "REPORT"
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), ["0,0,WEST"])

    def test_end_to_end_scenario_3(self):
        command_list = [
            "PLACE 1,2,EAST",
            "MOVE",
            "MOVE",
            "LEFT",
            "MOVE",
            "REPORT"
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), ["3,3,NORTH"])

    def test_end_to_end_scenario_4(self):

        # Test that commands issued before a rover is placed are ignored
        command_list = [
            "MOVE",
            "MOVE",
            "LEFT",
            "MOVE",
            "REPORT",
            "PLACE 1,2,EAST",
            "REPORT"
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), [None, "1,2,EAST"])

    def test_end_to_end_scenario_5(self):

        # Test that attempting to walk the rover off the board is ignored
        command_list = [
            "PLACE 0,0,NORTH",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "REPORT",
            "RIGHT",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "MOVE",
            "REPORT",
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), ["0,4,NORTH", "4,4,EAST"])

    def test_end_to_end_scenario_6(self):

        # Test invalid PLACE command does not allow subsequent commands to work
        command_list = [
            "PLACE 1,2,DOWN",
            "PLACE -1,2,EAST",
            "PLACE 1,22,EAST",
            "PLACE 1,22",
            "MOVE",
            "MOVE",
            "LEFT",
            "MOVE",
            "REPORT"
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), [None])

    def test_end_to_end_scenario_7(self):

        # Test unrecognised commands have no effect
        command_list = [
            "PLACE 1,2,EAST",
            "MOVE",
            "STOP",
            "MOVE",
            "LEFT",
            "ROTATE",
            "MOVE",
            "MAUVE",
            "REPORT"
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), ["3,3,NORTH"])

    def test_end_to_end_scenario_8(self):

        # Calling place replaces the rover if the command is valid
        command_list = [
            "PLACE 1,2,EAST",
            "MOVE",
            "MOVE",
            "LEFT",
            "MOVE",
            "PLACE 2,1,SOUTH",
            "REPORT"
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), ["2,1,SOUTH"])

    def test_end_to_end_scenario_9(self):

        # Tests all possible commands in a long list
        command_list = [
            "PLACE 0,0,NORTH", # 0,0,NORTH
            "MOVE", # 0,1,NORTH
            "RIGHT", # 0,1,EAST
            "MOVE", # 1,1,EAST
            "MOVE", # 2,1,EAST
            "LEFT", # 2,1,NORTH
            "LEFT", # 2,1,WEST
            "LEFT", # 2,1,SOUTH
            "MOVE", # 2,0,SOUTH
            "LEFT", # 2,0,EAST
            "MOVE", # 3,0,EAST
            "LEFT", # 3,0,NORTH
            "MOVE", # 3,1,NORTH
            "MOVE", # 3,2,NORTH
            "MOVE", # 3,3,NORTH
            "MOVE", # 3,4,NORTH
            "MOVE", # 3,4,NORTH - invalid move
            "RIGHT", # 3,4,EAST
            "RIGHT", # 3,4,SOUTH
            "RIGHT", # 3,4,WEST
            "MOVE", # 2,4,WEST
            "MOVE", # 1,4,WEST
            "REPORT"
        ]

        self.assertEqual(self._test_end_to_end_scenario(command_list), ["1,4,WEST"])


if __name__ == '__main__':
    unittest.main()
