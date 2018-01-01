"""Utility functions to parse dstat output csv format."""
import csv
import logging
from collections import defaultdict


class ParserConfig(object):
    """Configures parser"""
    def __init__(self):
        pass


class ResultsColumnMap(object):
    """Creates a mapping of category and subcategory headers to column indexes.

    This metadata is used for parsing columns within each data row and
    organizing them into arrays for analysis and plotting.

    TODO: Add filtering ability on categories and subcategories
    """
    def __init__(self):
        """Initialize storage data structures.

        Category column mapping uses each column category as a key associated
        with a list of two integers, representing start and end columns for
        that category.

        Mappings contains category-subcategory-column index mapping. E.g.:
            {'category1': { 'subcat_1a': 1,
                            'subcat_1b': 2 },
             'category2': { 'subcat_2a': 3,
                            'subcat_2b': 4}
            }
        """
        self._category_cols = defaultdict(list)
        self.mappings = defaultdict(dict)
        # We keep a pointer to the last category since we need to use the
        # subcat row to determine its final column index.
        self._last_cat = None

    def set_categories(self, categories_row):
        cur_cat = None
        for col_idx, col in enumerate(categories_row):
            if col:
                if cur_cat is not None:
                    # Mark that it's the end column of the previous category
                    self._category_cols[cur_cat].append(col_idx-1)
                cur_cat = str(col)
                self._category_cols[cur_cat].append(col_idx)
        self._initialize_mapping_categories()
        self._last_cat = cur_cat

    def _initialize_mapping_categories(self):
        for cat in self._category_cols:
            self.mappings[cat]

    def _get_end_col_for_final_cat(self, subcat_row_length):
        """Parsing the category row will not let us know where the final
        category's last column is. We need to use info from the next header
        to identify this.

        Args:
            subcat_row_length: integer representing column width of subcategory
                                row.
        """
        self._category_cols[self._last_cat].append(subcat_row_length-1)

    def set_subcategories(self, subcat_row):
        if not self.mappings:
            raise ValueError('You must initialize category mappings before you'
                             ' can initialize subcategory mappings')
        self._get_end_col_for_final_cat(len(subcat_row))
        for cat in self._category_cols:
            for col_idx in range(self._category_cols[cat][0],
                                 self._category_cols[cat][1]+1):
                subcat_name = subcat_row[col_idx]
                self.mappings[cat][subcat_name] = col_idx


class DstatResults(object):
    """An instance of a Dstat csv output results file."""
    def __init__(self):
        """
        Results contains category-subcategory dicts that map to a list of
        numerical data. E.g.:
            {'category1': { 'subcat_1a': [0.5 1 3 ...],
                            'subcat_1b': [0.1 9.7 1.5 ...] },
             'category2': { 'subcat_2a': [0.5 1 3 ...],
                            'subcat_2b': [0.1 9.7 1.5 ...]}
            }
        """
        self._startingstrs_to_ignore = ['Dstat ', 'Author:', 'Host:',
                                        'Cmdline:']
        self._results_column_map = ResultsColumnMap()
        self.results = defaultdict(dict)

    def read_csv(self, filepath):
        """Read CSV then pass reader object to parser method."""
        with open(filepath, 'rU') as resultsfp:
            csvreader = csv.reader(resultsfp, delimiter=',')
            self._parse_csv(csvreader)

    def _parse_csv(self, csvreader):
        """Parse csv lines.

        Args:
            csvreader: Reader object returned from csv reader.
        """
        # initialize variables to identify which section we're parsing:
        #   - metadata rows that should be ignored
        #   - header rows, of which there are two.
        cur_row_type = 'ignore'
        header_row_idx = 0

        for rownum, row in enumerate(csvreader, 1):
            # While within the metadata rows section, check to see if you've
            # reached a header row.
            if (cur_row_type == 'ignore'
                    and not self._starting_row_to_ignore(row)):
                logging.info('Found headers starting at row %i', rownum)
                cur_row_type = 'header'

            if cur_row_type == 'header':
                if header_row_idx == 0:
                    # first header row contains categories
                    self._results_column_map.set_categories(row)
                    header_row_idx += 1
                else:
                    # second (and final) header row contains subcategories
                    self._results_column_map.set_subcategories(row)
                    self._initialize_results()
                    cur_row_type = 'data'
                    logging.info('Finished parsing headers.')
            elif cur_row_type == 'data':
                self._append_data(row)

    def _initialize_results(self):
        """Initialize the results dict with categories and subcategories.

        Args:
            results_column_map: An instance of ResultsColumnMap which holds
                                column index mappings to categories and
                                subcategories.
        """
        for cat in self._results_column_map.mappings:
            for subcat in self._results_column_map.mappings[cat]:
                self.results[cat][subcat] = list()

    def _append_data(self, data_row):
        """For each row that contains numerical data, append data points.

        Uses column mappings to identify where to append each column.

        TODO: Will need to
        explicitly cast some subcat values as float, otherwise data values
        get read as strings.
        """
        for cat in self.results:
            for subcat in self.results[cat]:
                col_idx = self._results_column_map.mappings[cat][subcat]
                self.results[cat][subcat].append(data_row[col_idx])

    def _starting_row_to_ignore(self, row):
        """Determines if row contains data or contains headers metadata
        that should be ignored.

        Args:
            row: list representing a csv row.

        Returns:
            boolean: True if should be ignored.
        """
        try:
            col1 = str(row[0])
            for pattern in self._startingstrs_to_ignore:
                if col1.startswith(pattern):
                    return True
        except Exception as e:
            logging.info('No data in row, raises exception: %s', str(e))
            return True
        return False


def parse_directory():
    # TODO: Provide ability to parse multiple output files in dir based on
    #       filename patterns.
    pass
