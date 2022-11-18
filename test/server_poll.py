import unittest
import requests
import time
from coverage import Coverage


def run_tests(proc, test_dir):
    timeout_threshold = 240
    start_time = time.time()
    while time.time()-start_time < timeout_threshold:
        try:
            requests.head("http://localhost:7860/")
            break
        except requests.exceptions.ConnectionError:
            if proc.poll() is not None:
                break
    if proc.poll() is None:
        if test_dir is None:
            test_dir = ""

        cov = Coverage()
        cov.start()

        suite = unittest.TestLoader().discover(test_dir, pattern="*_test.py", top_level_dir="test")
        result = unittest.TextTestRunner(verbosity=2).run(suite)

        cov.stop()
        with open('coverage_report.xml', 'w') as f:
            cov.xml_report(outfile=f)

        return len(result.failures) + len(result.errors)
    else:
        print("Launch unsuccessful")
        return 1
