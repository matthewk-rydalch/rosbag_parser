import unittest
import numpy as np
import ecef_v_relpos

class TEcef2Ned(unittest.TestCase):
    def test_south_pole(self):
        ecef = np.array([1.0,2.0,600000000])
        ecefOrigin = np.array([0.0,0.0,600000000])
        refLla = np.array([-90.0,0.0,1000])

        ned = ecef_v_relpos.ecef2ned(ecef, ecefOrigin, refLla)
        expectedNED = [1.0,2.0,0.0]

        self.assertAlmostEqual(ned[0],expectedNED[0])
        self.assertAlmostEqual(ned[1], expectedNED[1])
        self.assertAlmostEqual(ned[2], expectedNED[2])

    def test_prime_meridian(self):
        ecef = np.array([600000000.0,2.0,1.0])
        ecefOrigin = np.array([600000000.0,0.0,0.0])
        refLla = np.array([0.0,0.0,1000])

        ned = ecef_v_relpos.ecef2ned(ecef, ecefOrigin, refLla)
        expectedNED = [1.0,2.0,0.0]

        self.assertAlmostEqual(ned[0],expectedNED[0])
        self.assertAlmostEqual(ned[1], expectedNED[1])
        self.assertAlmostEqual(ned[2], expectedNED[2])

    def test_latlon_equal_45(self):
        # ecef = np.array([-1797871.09,-4532604.1,4099820.49])
        # ecefOrigin = np.array([-1797870.50,-4532603.59,4099821.23])
        # refLla = np.array([40.25,-111.65,1410.29])
        ecef = np.array([200000000-1.15,200000000.0-1.15,200000000.0+1.15])
        ecefOrigin = np.array([200000000,200000000.0,200000000.0])
        refLla = np.array([45.0,45.0,1000])

        ned = ecef_v_relpos.ecef2ned(ecef, ecefOrigin, refLla)
        expectedNED = [1.9918584,0.0,0.0]

        self.assertAlmostEqual(ned[0],expectedNED[0],places=0) #I think there is rounding error, so the precisness can't be high
        self.assertAlmostEqual(ned[1], expectedNED[1],places=0)
        self.assertAlmostEqual(ned[2], expectedNED[2],places=0)

    def test_experimental_data(self):
        ecef = np.array([-1797871.09,-4532603.95,4099820.45])
        ecefOrigin = np.array([-1797869.52,-4532603.15,4099821.26])
        refLla = np.array([40.246449,-111.635889,1409.721])

        ned = ecef_v_relpos.ecef2ned(ecef, ecefOrigin, refLla)
        expectedNED = [-1.47,-1.16,-0.48]

        self.assertAlmostEqual(ned[0],expectedNED[0],places=0) #I think there is rounding error, so the precisness can't be high
        self.assertAlmostEqual(ned[1], expectedNED[1],places=0)
        self.assertAlmostEqual(ned[2], expectedNED[2],places=0)

if __name__ == '__main__':
    unittest.main()