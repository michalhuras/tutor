"""Module contain unit tests for the question strategy. """
import unittest

from PySide6.QtGui import QColorConstants, QColor

from src.gui.strategy.question import blend_colors


class QuestionStrategyTests(unittest.TestCase):
    """Class contain unit tests for the question strategy. """
    def test_blend_colors(self):
        """Check if blending colors produces correct result. """
        expected_result = [QColor(255, 0, 0),
                           QColor(191, 63, 0),
                           QColor(127, 127, 0),
                           QColor(63, 191, 0),
                           QColor(0, 255, 0)
                           ]

        result = list(blend_colors(QColorConstants.Red, QColorConstants.Green, 5))
        self.assertEqual(expected_result, result)
