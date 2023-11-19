import unittest
from unittest.mock import patch
from io import StringIO

class TestGeometryDashGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = GeometryDashGame()

    def setUp(self):
        self.game.screen.fill((0, 0, 0))  # Clear the screen before each test

    @patch('builtins.input', side_effect=['\r'])  # Simulate pressing Enter
    def test_startup_menu(self, mock_input):
        with self.assertRaises(SystemExit):
            self.game.startup_menu()

    @patch('builtins.input', side_effect=['\r'])  # Simulate pressing Enter
    def test_final_score_menu_quit(self, mock_input):
        result = self.game.final_score_menu(10)
        self.assertEqual(result, "quit")

    @patch('builtins.input', side_effect=['\r'])  # Simulate pressing Enter
    def test_final_score_menu_play_again(self, mock_input):
        result = self.game.final_score_menu(10)
        self.assertEqual(result, "play again")

    def test_draw_text(self):
        # Redirect stdout to capture print statements
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.game.draw_text("Test Text", self.game.font, (255, 255, 255), 100, 100)

        # Check if the text is drawn to the screen
        self.assertIn("Test Text", mock_stdout.getvalue())

    def test_collision_detection_no_collision(self):
        obstacle_list = [{'x': 200, 'y': 200, 'width': 50, 'height': 50}]
        result = self.game.collision_detection(obstacle_list, 100, 100, 50, 50)
        self.assertFalse(result)

    def test_collision_detection_with_collision(self):
        obstacle_list = [{'x': 100, 'y': 100, 'width': 50, 'height': 50}]
        result = self.game.collision_detection(obstacle_list, 120, 120, 30, 30)
        self.assertTrue(result)

class TestCollisionDetection(unittest.TestCase):
    def setUp(self):
        self.game = GeometryDashGame()
        self.obstacle_list = []

    def test_collision_no_collision(self):
        result = collision_detection(self.obstacle_list, self.game.player_x, self.game.player_y, self.game.player_width, self.game.player_height)
        self.assertFalse(result)

    def test_collision_left_collision(self):
        # Assuming an obstacle at the left of the player
        obstacle = {'x': self.game.player_x - self.game.obstacle_width, 'y': self.game.player_y, 'width': self.game.obstacle_width, 'height': self.game.obstacle_height}
        self.obstacle_list.append(obstacle)

        result = collision_detection(self.obstacle_list, self.game.player_x, self.game.player_y, self.game.player_width, self.game.player_height)
        self.assertTrue(result)

    def test_collision_right_collision(self):
        # Assuming an obstacle at the right of the player
        obstacle = {'x': self.game.player_x + self.game.player_width, 'y': self.game.player_y, 'width': self.game.obstacle_width, 'height': self.game.obstacle_height}
        self.obstacle_list.append(obstacle)

        result = collision_detection(self.obstacle_list, self.game.player_x, self.game.player_y, self.game.player_width, self.game.player_height)
        self.assertTrue(result)

    def test_collision_top_collision(self):
        # Assuming an obstacle at the top of the player
        obstacle = {'x': self.game.player_x, 'y': self.game.player_y - self.game.obstacle_height, 'width': self.game.obstacle_width, 'height': self.game.obstacle_height}
        self.obstacle_list.append(obstacle)

        result = collision_detection(self.obstacle_list, self.game.player_x, self.game.player_y, self.game.player_width, self.game.player_height)
        self.assertTrue(result)

    def test_collision_bottom_collision(self):
        # Assuming an obstacle at the bottom of the player
        obstacle = {'x': self.game.player_x, 'y': self.game.player_y + self.game.player_height, 'width': self.game.obstacle_width, 'height': self.game.obstacle_height}
        self.obstacle_list.append(obstacle)

        result = collision_detection(self.obstacle_list, self.game.player_x, self.game.player_y, self.game.player_width, self.game.player_height)
        self.assertTrue(result)

class TestPlayerMovement(unittest.TestCase):
    def setUp(self):
        self.game = GeometryDashGame()

    def test_player_jump(self):
        # Mock the Pygame event for the jump key (e.g., spacebar)
        pygame_event = MagicMock()
        pygame_event.type = pygame.KEYDOWN
        pygame_event.key = pygame.K_SPACE

        # Simulate the player pressing the jump key
        self.game.player_jump = False
        self.game.player_y_change = 0
        self.game.player_y = self.game.screen_height - self.game.ground_height - self.game.player_height
        self.game.collision_detection = MagicMock(return_value=False)

        self.game.run_game()
        self.game.handle_events([pygame_event])

        self.assertTrue(self.game.player_jump)
        self.assertEqual(self.game.player_y_change, -self.game.player_jump_speed)

    def test_player_jump_collision(self):
        # Mock the Pygame event for the jump key (e.g., spacebar)
        pygame_event = MagicMock()
        pygame_event.type = pygame.KEYDOWN
        pygame_event.key = pygame.K_SPACE

        # Simulate the player pressing the jump key with collision
        self.game.player_jump = False
        self.game.player_y_change = 0
        self.game.player_y = self.game.screen_height - self.game.ground_height - self.game.player_height
        self.game.collision_detection = MagicMock(return_value=True)

        self.game.run_game()
        self.game.handle_events([pygame_event])

        self.assertFalse(self.game.player_jump)
        self.assertEqual(self.game.player_y_change, 0)

    def test_player_gravity(self):
        # Simulate the player in mid-air after jumping
        self.game.player_jump = True
        self.game.player_y_change = -self.game.player_jump_speed

        # Run the game to apply gravity
        self.game.run_game()

        self.assertTrue(self.game.player_jump)
        self.assertGreater(self.game.player_y_change, 0)  # Player should be falling due to gravity

class TestGameOver(unittest.TestCase):
    def setUp(self):
        self.game = GeometryDashGame()

    def test_collision_game_over(self):
        # Mock the Pygame event for the jump key (e.g., spacebar)
        pygame_event = MagicMock()
        pygame_event.type = pygame.KEYDOWN
        pygame_event.key = pygame.K_SPACE

        # Simulate a collision with an obstacle
        self.game.player_jump = False
        self.game.player_y_change = 0
        self.game.player_y = self.game.screen_height - self.game.ground_height - self.game.player_height
        self.game.collision_detection = MagicMock(return_value=True)

        self.game.run_game()
        self.game.handle_events([pygame_event])

        self.assertTrue(self.game.is_game_over)

    def test_no_collision_continue_game(self):
        # Mock the Pygame event for the jump key (e.g., spacebar)
        pygame_event = MagicMock()
        pygame_event.type = pygame.KEYDOWN
        pygame_event.key = pygame.K_SPACE

        # Simulate no collision with obstacles
        self.game.player_jump = False
        self.game.player_y_change = 0
        self.game.player_y = self.game.screen_height - self.game.ground_height - self.game.player_height
        self.game.collision_detection = MagicMock(return_value=False)

        self.game.run_game()
        self.game.handle_events([pygame_event])

        self.assertFalse(self.game.is_game_over)

if __name__ == '__main__':
    unittest.main()
