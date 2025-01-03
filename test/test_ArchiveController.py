import unittest
from unittest.mock import patch
from controllers.ArchiveController import archive_folder, archive_folder_process
from common.Messages import MSG_ERR_CONTROLLER_ARCHIVE

class TestArchiveController(unittest.TestCase):
    def test_archive_folder_without_delete(self):
        """Test archiving without deletion"""
        
        with patch('os.path.exists') as mock_os_path_exists, \
             patch('shutil.make_archive') as mock_shutil_make_archive, \
             patch('shutil.rmtree') as mock_shutil_rmtree, \
             patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
             patch('os.remove') as mock_os_remove:
            mock_os_path_exists.return_value = True
            mock_shutil_make_archive.return_value = True
            mock_shutil_rmtree.return_value = True
            mock_check_and_create_folder.return_value = True
            mock_os_remove.return_value = True
            # Test archiving without deletion
            archive_folder("test_folder", is_delete=False)
            
    def test_archive_folder_with_delete(self):
        """Test archiving with deletion"""
        with patch('os.path.exists') as mock_os_path_exists, \
             patch('shutil.make_archive') as mock_shutil_make_archive, \
             patch('shutil.rmtree') as mock_shutil_rmtree, \
             patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
             patch('os.remove') as mock_os_remove:
            mock_os_path_exists.return_value = True
            mock_shutil_make_archive.return_value = True
            mock_shutil_rmtree.return_value = True
            mock_check_and_create_folder.return_value = True
            mock_os_remove.return_value = True
            # Test archiving with deletion
            archive_folder("test_folder", is_delete=True)
            
    def test_archive_folder_exception(self):
        """Test archiving with exception"""
        with patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder:
            mock_check_and_create_folder.side_effect = Exception("Test exception")
            # Test archiving with exception
            with self.assertRaises(Exception) as exc_info:
                archive_folder_process({"folder": "test_folder", "is_delete": False})
                
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_ARCHIVE.format("archive_folder"))
