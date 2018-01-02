import plotter
import numpy as np
import unittest
from mock import patch


class TestPlotter(unittest.TestCase):
    def setUp(self):
        t = np.arange(0., 5., 0.2)
        t2 = np.arange(0., 5.6, 0.2)
        self.mydata = [t, t, t2, t2**2, t, t**3]
        self.legend = ('No mask', 'Masked if > 0.5', 'Masked if < -0.5')
        self.title = 'Line graph demo'

    @patch('plotter.plt.show')
    @patch('plotter.plt.title')
    def test_plotterCallsMatplotLibFunctions(self, mock_plt_show,
                                             mock_plt_title):
        # Simply verifies that it calls some of the needed functions
        # TODO: Will need to improve this test in the future to not depend
        #       on actually starting matplotlib
        plotter.create_line_graph(self.mydata, self.legend, self.title)
        assert plotter.plt.title.called

    @patch('plotter.plt.show')
    @patch('plotter.plt.title')
    def test_plotterCallsMatplotLibFunctionsNoTitle(self, mock_plt,
                                                    mock_plt_title):
        # Simply verifies that it calls some of the needed functions
        # TODO: Will need to improve this test in the future to not depend
        #       on actually starting matplotlib
        plotter.create_line_graph(self.mydata, self.legend)
        assert not plotter.plt.title.called


if __name__ == '__main__':
    unittest.main()
