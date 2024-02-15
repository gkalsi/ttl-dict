import unittest
import ttldict

class TestClock:
    """TestClock implements a `time` method that allows us to simulated the passage of time
        without sleeping in the test.
    """
    def __init__(self, unix_ts=0.0):
        self.__unix_ts = unix_ts


    def time(self):
        return self.__unix_ts
    

    def advance(self, seconds):
        self.__unix_ts += seconds

    
    def set_time(self, unix_ts):
        self.__unix_ts = unix_ts


class TestTTLDict(unittest.TestCase):
    def setUp(self):
        self.clk = TestClock(0)
        self.dut = ttldict.TTLDict(self.clk.time)


    def test_trivial(self):
        """Insert a Key and make sure we can read it back using both `get` and `[]`"""
        self.dut["key"] = "value"
        self.assertEqual(self.dut["key"], "value")
        self.assertEqual(self.dut.get("key"), "value")


    def test_missing(self):
        """Make sure that missing keys work just like dicts for `get` and `[]`"""
        self.assertIsNone(self.dut.get("key"))

        with self.assertRaises(KeyError):
            _unused = self.dut["key"]
        

    def test_expired_key(self):
        """Make sure that expired keys are evicted"""
        self.dut.set("key", "value", 5)

        # Make sure the key made it in there.
        self.assertEqual(self.dut.get("key"), "value")

        # Make some time pass.
        self.clk.advance(10)

        # Make sure the key was evicted.
        self.assertIsNone(self.dut.get("key"))


    def test_expire_multikey(self):
        """If there are multiple keys, make sure only the expired ones are evicted"""
        self.dut.set("five", "five seconds", 5)
        self.dut.set("twenty", "twenty seconds", 20)
        self.dut.set("ten", "ten seconds", 10)
        self.dut.set("fifteen", "fifteen seconds", 15)

        self.clk.advance(12)

        self.assertEqual(len(self.dut), 2)
        self.assertEqual(self.dut.get("fifteen"), "fifteen seconds")
        self.assertEqual(self.dut.get("twenty"), "twenty seconds")


    def test_update_ttl(self):
        """Make sure we can update the TTL for a key"""
        self.dut.set("key", "value", 10)
        self.dut.set("key", "value", 20)

        self.clk.advance(15)

        # Key should still be in the dict because we updated its TTL to 20 seconds.
        self.assertEqual(self.dut.get("key"), "value")


if __name__ == "__main__":
    unittest.main()