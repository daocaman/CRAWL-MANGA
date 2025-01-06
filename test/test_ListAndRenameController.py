import unittest
from unittest.mock import patch, MagicMock
import json
from controllers.ListAndRenameController import get_list_of_files, rename_file
from common.Messages import MSG_ERR_CONTROLLER_LIST_AND_RENAME

class TestListAndRenameController(unittest.TestCase):
    def setUp(self):
        self.test_path = "test/test_data"
        self.test_list_file = [
            "test_file_1.txt",
            "test_file_2.txt",
            "test_file_3.txt"
        ]
        
        self.test_list_file_obj = [
            {
                "root_path": self.test_path,
                "current_file_name": "test_file_1.txt",
                "new_file_name": "test_file_1_new.txt"
            }
        ]
       
    def test_get_list_of_files_success(self):
        """Test get_list_of_files with success"""
        with patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
            patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('os.path.exists') as mock_path_exists, \
            patch('builtins.open') as mock_open, \
            patch("json.dump") as mock_json_dump, \
            patch('os.listdir') as mock_listdir:
                
            mock_json_dump.return_value = None
            
            mock_open_obj = MagicMock()
            mock_open_obj.write.return_value = None
            mock_open.return_value.__enter__.return_value = mock_open_obj
            
            mock_check_and_create_folder.return_value = True
            mock_check_file_exist.return_value = True
            mock_path_exists.return_value = True
            mock_listdir.return_value = self.test_list_file

            get_list_of_files(self.test_path)
            
    def test_get_list_of_files_failure(self):
        """Test get_list_of_files with failure"""
        with patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
            patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('os.path.exists') as mock_path_exists:
            
            mock_check_and_create_folder.return_value = False
            mock_check_file_exist.return_value = False
            mock_path_exists.return_value = False

            with self.assertRaises(Exception) as exc_info:
                get_list_of_files(self.test_path)
                
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_LIST_AND_RENAME.format("get_list_of_files"))

    def test_rename_file_success(self):
        """Test rename_file with success"""
        with patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('os.path.exists') as mock_path_exists, \
            patch('os.rename') as mock_rename, \
            patch('builtins.open') as mock_open:
            
            mock_check_file_exist.return_value = True
            mock_path_exists.return_value = True
            
            mock_open_obj = MagicMock()
            mock_open_obj.read.return_value = json.dumps(self.test_list_file_obj)
            mock_open.return_value.__enter__.return_value = mock_open_obj
            
            mock_rename.return_value = None
            
            rename_file()

    def test_rename_file_failure(self):
        """Test rename_file with failure"""
        with patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('builtins.open') as mock_open:
            
            mock_check_file_exist.return_value = False
            mock_open.return_value.__enter__.return_value = MagicMock()

            with self.assertRaises(Exception) as exc_info:
                rename_file()
                
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_LIST_AND_RENAME.format("rename_file"))

