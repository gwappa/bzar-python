#
# MIT License
#
# Copyright (c) 2019 Keisuke Sehara
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""unittest-based test case."""

import unittest
from pathlib import Path as _Path
import numpy as _np
import bzar

class TestBzarIO(unittest.TestCase):
    FILENAME_FULL = 'test_bzar_io.bzar'
    FILENAME_BASE = 'test_bzar_io'

    def setUp(self):
        self.data_orig     = _np.arange(10, dtype=int).reshape((2,-1))
        self.metadata_base = { "description": "test case for bzar I/O" }
        self.metadata_orig = bzar.generate_metadata_dict(data=self.data_orig, metadata=self.metadata_base)
        self.metadata_size = bzar.calc_metadata_size(self.metadata_orig)
        bzar.save(self.FILENAME_BASE, data=self.data_orig, metadata=self.metadata_base)

    def test_read_data_sizes(self):
        datasiz, metasiz = bzar.read_data_sizes(self.FILENAME_FULL)
        self.assertEqual(self.metadata_size, metasiz)
        self.assertEqual(len(self.data_orig.tobytes()), datasiz)

    def test_read_metadata(self):
        metadata = bzar.read_metadata(self.FILENAME_FULL, complete=False)
        self.assertEqual(self.metadata_base, metadata)
        metadata = bzar.read_metadata(self.FILENAME_FULL, complete=True)
        self.assertEqual(self.metadata_orig, metadata)

    def test_read_path(self):
        data, metadata = bzar.load(self.FILENAME_FULL, with_metadata=True)
        self.assertTrue(_np.allclose(self.data_orig, data))
        self.assertEqual(self.metadata_base, metadata)

    def tearDown(self):
        tested = _Path(self.FILENAME_FULL)
        if tested.exists():
            tested.unlink()
