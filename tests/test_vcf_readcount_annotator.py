import unittest
import sys
import os
import py_compile
from vcf_annotation_tools import vcf_readcount_annotator
import tempfile
from filecmp import cmp

class VcfExpressionEncoderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir          = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
        cls.executable    = os.path.join(base_dir, 'vcf_annotation_tools', 'vcf_readcount_annotator.py')
        cls.test_data_dir = os.path.join(base_dir, 'tests', 'test_data')

    def test_source_compiles(self):
        self.assertTrue(py_compile.compile(self.executable))

    def test_error_more_than_one_sample_without_sample_name(self):
        with self.assertRaises(Exception) as context:
            command = [
                os.path.join(self.test_data_dir, 'multiple_samples.vcf'),
                os.path.join(self.test_data_dir, 'snvs.bam_readcount'),
                'DNA',
            ]
            vcf_readcount_annotator.main(command)
        self.assertTrue('contains more than one sample. Please use the -s option to specify which sample to annotate.' in str(context.exception))

    def test_error_more_than_one_sample_with_wrong_sample_name(self):
        with self.assertRaises(Exception) as context:
            command = [
                os.path.join(self.test_data_dir, 'multiple_samples.vcf'),
                os.path.join(self.test_data_dir, 'snvs.bam_readcount'),
                'DNA',
                '-s', 'nonexistent_sample',
            ]
            vcf_readcount_annotator.main(command)
        self.assertTrue('does not contain a sample column for sample nonexistent_sample.' in str(context.exception))