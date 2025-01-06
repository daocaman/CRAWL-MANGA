import unittest
from unittest.mock import patch
from common.Validations import *

class TestValidationCheckAndCreateFolder(unittest.TestCase):
    def test_check_existing_folder(self):
        """Test when folder already exists"""
        with patch('os.path.exists') as mock_os_path_exists:
            mock_os_path_exists.return_value = True
            self.assertEqual(check_and_create_folder("test_folder"), True)
            
    def test_check_non_existing_folder(self):
        """Test when folder doesn't exist and no action is taken"""
        with patch('os.path.exists') as mock_os_path_exists:
            mock_os_path_exists.return_value = False
            self.assertEqual(check_and_create_folder("test_folder"), False)
            
    def test_create_non_existing_folder(self):
        """Test folder creation when it doesn't exist"""
        with patch('os.path.exists') as mock_os_path_exists, \
             patch('os.makedirs') as mock_os_makedirs:
            mock_os_path_exists.return_value = False
            mock_os_makedirs.return_value = None
            self.assertEqual(check_and_create_folder("test_folder", create=True), True)
            mock_os_makedirs.assert_called_once_with("test_folder")

    def test_alert_non_existing_folder(self):
        """Test alert when folder doesn't exist"""
        with patch('os.path.exists') as mock_os_path_exists:
            mock_os_path_exists.return_value = False
            with self.assertRaises(Exception) as exc_info:
                check_and_create_folder("test_folder", alert=True)
            self.assertEqual(str(exc_info.exception), MSG_ERR_FOLDER_NOT_EXIST.format("test_folder"))

class TestValidationCheckFileExist(unittest.TestCase):
    def test_check_existing_file(self):
        """Test when file exists"""
        with patch('os.path.exists') as mock_os_path_exists:
            mock_os_path_exists.return_value = True
            self.assertEqual(check_file_exist("test_file"), True)

    def test_check_non_existing_file_alert(self):
        """Test when file doesn't exist and alert is True"""
        with patch('os.path.exists') as mock_os_path_exists:
            mock_os_path_exists.return_value = False
            with self.assertRaises(Exception) as exc_info:
                check_file_exist("test_file", alert=True)
            self.assertEqual(str(exc_info.exception), MSG_ERR_FILE_NOT_EXIST.format("test_file"))

    def test_check_non_existing_file_no_alert(self):
        """Test when file doesn't exist and alert is False"""
        with patch('os.path.exists') as mock_os_path_exists:
            mock_os_path_exists.return_value = False
            self.assertEqual(check_file_exist("test_file", alert=False), False)

class TestValidationCheckAndGetListOfFolders(unittest.TestCase):
    def test_check_and_get_list_of_folders(self):
        """Test when folders exist"""
        with patch('os.listdir') as mock_os_listdir, \
             patch('os.path.isdir') as mock_os_path_isdir:
            mock_os_listdir.return_value = ["test_folder1", "test_folder2"]
            mock_os_path_isdir.return_value = True
            self.assertEqual(check_and_get_list_of_folders("test"), ["test_folder1", "test_folder2"])

    def test_check_and_get_list_of_folders_no_folders(self):
        """Test when no folders exist"""
        with patch('os.listdir') as mock_os_listdir, \
             patch('os.path.isdir') as mock_os_path_isdir:
            mock_os_listdir.return_value = []
            mock_os_path_isdir.return_value = True
            with self.assertRaises(Exception) as exc_info:
                check_and_get_list_of_folders("test", alert=True)
            self.assertEqual(str(exc_info.exception), MSG_ERR_NO_FOLDERS_WITH_NAME.format("test"))

    def test_check_and_get_list_of_folders_no_alert(self):
        """Test when no folders exist and alert is False"""
        with patch('os.listdir') as mock_os_listdir, \
             patch('os.path.isdir') as mock_os_path_isdir:
            mock_os_listdir.return_value = []
            mock_os_path_isdir.return_value = True
            self.assertEqual(check_and_get_list_of_folders("test", alert=False), [])

class TestValidationCheckValidVideoUrl(unittest.TestCase):
    def test_check_valid_video_url(self):
        """Test when URL is a valid YouTube video URL"""
        
        self.assertEqual(check_valid_video_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ"), True)

    def test_check_invalid_video_url(self):
        """Test when URL is not a valid YouTube video URL"""
        with self.assertRaises(Exception) as exc_info:
            check_valid_video_url("https://google.com", alert=True)
        self.assertEqual(str(exc_info.exception), MSG_ERR_URL_NOT_VALID_VIDEO)
        
    def test_check_invalid_video_url_no_alert(self):
        """Test when URL is not a valid YouTube video URL and alert is False"""
        self.assertEqual(check_valid_video_url("https://google.com", alert=False), False)

class TestValidationCheckValidPlaylistUrl(unittest.TestCase):
    def test_check_valid_playlist_url(self):
        """Test when URL is a valid YouTube playlist URL"""
        self.assertEqual(check_valid_playlist_url("https://www.youtube.com/playlist?list=PL1234567890"), True)

    def test_check_invalid_playlist_url(self):
        """Test when URL is not a valid YouTube playlist URL"""
        with self.assertRaises(Exception) as exc_info:
            check_valid_playlist_url("https://google.com", alert=True)
        self.assertEqual(str(exc_info.exception), MSG_ERR_URL_NOT_VALID_PLAYLIST)

    def test_check_invalid_playlist_url_no_alert(self):
        """Test when URL is not a valid YouTube playlist URL and alert is False"""
        self.assertEqual(check_valid_playlist_url("https://google.com", alert=False), False)

