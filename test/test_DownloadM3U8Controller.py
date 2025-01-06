import unittest
from unittest.mock import patch, MagicMock
from controllers.DownloadM3U8Controller import download_m3u8
from common.Messages import MSG_ERR_CONTROLLER_DOWNLOAD_M3U8

class TestDownloadM3U8Controller(unittest.TestCase):
    def setUp(self):
        self.file_data = [
            {"url": "https://example.com/video.m3u8", "output_path": "video.mp4"},
            {"url": "https://example.com/video2.m3u8", "output_path": "video2.mp4"}
        ]
        self.file_path = ""
        self.mock_json_object = MagicMock()

    def test_download_m3u8_success(self):
        with patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('os.path.exists') as mock_os_path_exists, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
            patch('json.load') as mock_json_load, \
            patch('m3u8_To_MP4.multithread_file_download') as mock_multithread_file_download, \
            patch('builtins.open') as mock_open:
           
            mock_os_path_exists.return_value = True
            mock_check_file_exist.return_value = True
            mock_check_and_create_folder.return_value = True
            
            mock_open.return_value = MagicMock()
            mock_json_load.return_value = self.file_data
            
            mock_multithread_file_download.return_value = True
            
            download_m3u8(self.file_path)

    def test_download_m3u8_failure(self):
        with patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('os.path.exists') as mock_os_path_exists, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder:
            mock_check_file_exist.return_value = False
            mock_os_path_exists.return_value = False
            mock_check_and_create_folder.return_value = False
            with self.assertRaises(Exception) as exc_info:
                download_m3u8(self.file_path)
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_DOWNLOAD_M3U8.format("download_m3u8"))

