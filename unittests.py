import unittest
import os
from Data import Data

class TestProgram(unittest.TestCase):
    def test_search_path_files(self):
        folder_path = 'musics'
        result = Data.search_path_files(folder_path)
        self.assertIsNotNone(result)

    def test_get_data_for_file(self):
        file_path = 'musics/music2.mp3'
        result = Data.get_data_for_file(file_path)
        self.assertIsNone(result)

    def test_count_files(self):
        folder_path = 'musics'
        result = Data.search_path_files(folder_path)
        expected_files = [
            'musics/MACAN - ASPHALT 8.mp3',
            'musics/music.flac'
        ]
        self.assertCountEqual(result, expected_files)

if __name__ == '__main__':
    unittest.main()