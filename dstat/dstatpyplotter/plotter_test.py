import plotter
import numpy as np
import unittest
from mock import MagicMock
from mock import patch


class TestPlotter(unittest.TestCase):
    def setUp(self):
        t = np.arange(0., 5., 0.2)
        t2 = np.arange(0., 5.6, 0.2)
        self.mydata = [t, t, t2, t2**2, t, t**3]
        self.legend = ('No mask', 'Masked if > 0.5', 'Masked if < -0.5')
        self.title = 'Line graph demo'

    @patch('plotter.plt')
    def test_plotterCallsMatplotLibFunctions(self, mock_plt):
        # Simply verifies that it calls the needed functions
        plotter.create_line_graph(self.mydata, self.legend, self.title)
        assert plotter.plt.plot.called
        assert plotter.plt.title.called
        assert plotter.plt.show.called

    @patch('plotter.plt')
    def test_plotterCallsMatplotLibFunctionsNoTitle(self, mock_plt):
        # Simply verifies that it calls the needed functions
        plotter.create_line_graph(self.mydata, self.legend)
        assert plotter.plt.plot.called
        assert not plotter.plt.title.called
        assert plotter.plt.show.called


if __name__ == '__main__':
    unittest.main()
