"""Integration tests to read test data."""

import outputfileparser as parser
import unittest


class TestOutputfile_Integration(unittest.TestCase):

    def test_parserReadsTotalCPUTestFile(self):
        myresults = parser.DstatResults()
        myresults.read_csv('testdata/dstat_example_result_totalcpu.csv')
        # Num of categories
        self.assertEqual(5, len(myresults.results))
        # Num of set_subcategories
        subcat_count = 0
        for cat in myresults.results:
            subcat_count += len(myresults.results[cat])
        self.assertEqual(13, subcat_count)
        # Num of rows per column
        for cat in myresults.results:
            for subcat in myresults.results[cat]:
                self.assertEqual(8, len(myresults.results[cat][subcat]))

    def test_parserReadsMultiCPUTestFile(self):
        myresults = parser.DstatResults()
        myresults.read_csv('testdata/dstat_example_result_multicpu.csv')

        # Num of categories should match expected
        self.assertEqual(41, len(myresults.results))
        # Num of set_subcategories
        subcat_count = 0
        for cat in myresults.results:
            subcat_count += len(myresults.results[cat])
        self.assertEqual(228, subcat_count)
        # Num of data rows per column
        for cat in myresults.results:
            for subcat in myresults.results[cat]:
                self.assertEqual(20, len(myresults.results[cat][subcat]))


if __name__ == '__main__':
    unittest.main()
