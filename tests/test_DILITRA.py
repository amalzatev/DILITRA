import os
import sys
sys.path.append(os.getcwd())

import unittest

from plscadd_report import pls_summary
from DILITRA import create_structures

class Test_DILITRA(unittest.TestCase):

    def setUp(self):
        self.structures = create_structures(pls_summary)

    def test_create_structures(self):
        self.assertEqual(self.structures[0].name, 'ML Las Damas')
        self.assertEqual(self.structures[15].ahead_span, 218.73)
        self.assertEqual(self.structures[23].coordinates.get('y'), 6194334.67)
        self.assertEqual(self.structures[34].attachments[2].get('insulator_attach_point').get('x'), 259780.92)


if __name__ == '__main__':
    unittest.main()
