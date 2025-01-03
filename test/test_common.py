import unittest
from common.Commons import *
from unittest.mock import patch, Mock, MagicMock
from common.Constants import *

class TestCommonIsImageFile(unittest.TestCase):
    def test_is_image_file_right_extension(self):
        """Test is_image_file with right extension"""
        self.assertTrue(is_image_file('test.jpg'))
        self.assertTrue(is_image_file('image.jpeg'))
        self.assertTrue(is_image_file('photo.png'))
    
    def test_is_image_file_wrong_extension(self):
        """Test is_image_file with wrong extension"""
        self.assertFalse(is_image_file('graphic.gif'))
        
    def test_is_image_file_no_extension(self):
        """Test is_image_file with no extension"""
        self.assertFalse(is_image_file('noextension'))
    
    def test_is_image_file_empty(self):
        """Test is_image_file with empty string"""
        self.assertFalse(is_image_file(''))

class TestGenerateFilename(unittest.TestCase):
    def test_basic_filename_generation(self):
        """Test basic filename generation with default length"""
        result = generate_filename(prefix="img_", idx=1, ext=".jpg")
        self.assertEqual(result, "img_0001.jpg")

    def test_custom_length(self):
        """Test filename generation with custom length"""
        result = generate_filename(prefix="img_", idx=1, ext=".jpg", str_len=3)
        self.assertEqual(result, "img_001.jpg")

    def test_large_index(self):
        """Test with index larger than padding"""
        result = generate_filename(prefix="img_", idx=12345, ext=".jpg", str_len=4)
        self.assertEqual(result, "img_2345.jpg")

    def test_empty_prefix(self):
        """Test with empty prefix"""
        result = generate_filename(idx=1, ext=".jpg")
        self.assertEqual(result, "0001.jpg")

    def test_empty_extension(self):
        """Test with empty extension"""
        result = generate_filename(prefix="img_", idx=1)
        self.assertEqual(result, "img_0001")

    def test_zero_index(self):
        """Test with zero index"""
        result = generate_filename(prefix="img_", idx=0, ext=".jpg")
        self.assertEqual(result, "img_0000.jpg")
        
class TestCommonExtractNumber(unittest.TestCase):
    def test_extract_first_integer(self):
        """Test extract_number with first integer"""
        assert extract_number("abc123def456") == 123
        assert extract_number("no numbers") == 0
        assert extract_number("42") == 42
        assert extract_number("abc42.5def") == 42

    def test_extract_last_integer(self):
        """Test extract_number with last integer"""
        assert extract_number("abc123def456", last=True) == 456
        assert extract_number("no numbers", last=True) == 0
        assert extract_number("42", last=True) == 42
        assert extract_number("abc42.5def", last=True) == 5

    def test_extract_first_float(self):
        """Test extract_number with first float"""
        assert extract_number("abc123.45def456", is_float=True) == 123.45
        assert extract_number("no numbers", is_float=True) == 0
        assert extract_number("42.5", is_float=True) == 42.5

    def test_extract_last_float(self):
        """Test extract_number with last float"""
        assert extract_number("abc123.45def456.78", last=True, is_float=True) == 456.78
        assert extract_number("no numbers", last=True, is_float=True) == 0
        assert extract_number("42.5", last=True, is_float=True) == 42.5

    def test_edge_cases(self):
        """Test extract_number with empty string"""
        assert extract_number("") == 0
        assert extract_number("", last=True) == 0
        assert extract_number("", is_float=True) == 0
        assert extract_number("", last=True, is_float=True) == 0

class TestCommonDownloadImage(unittest.TestCase):
   
    def test_download_image_success(self):
        """Test download_image with success"""
        with patch('requests.get') as mock_requests_get, \
             patch('os.path.exists') as mock_os_path_exists, \
             patch('common.Commons.is_image_error') as mock_is_image_error, \
            patch('builtins.open') as mock_open:
            
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = b'fake_image_content'
            mock_requests_get.return_value = mock_response
            
            mock_os_path_exists.return_value = False
            mock_is_image_error.return_value = False
            
            mock_open_obj = MagicMock()
            mock_open_obj.write.return_value = None
            mock_open.return_value = mock_open_obj
            
            result = download_image("https://example.com/image.jpg", "https://example.com", "local_image.jpg")
            
            self.assertEqual(result, 200)
            
    def test_download_image_failed(self):
        """Test download_image with failed"""
        with patch('requests.get') as mock_requests_get, \
             patch('os.path.exists') as mock_os_path_exists, \
             patch('common.Commons.is_image_error') as mock_is_image_error:
            
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.content = b'fake_image_content'
            mock_requests_get.return_value = mock_response
            
            mock_os_path_exists.return_value = False
            mock_is_image_error.return_value = False
            
            result = download_image("https://example.com/image.jpg", "https://example.com", "local_image.jpg")
            
            self.assertEqual(result, 400)      
            self.assertEqual(mock_requests_get.call_count, max_download_trial)
            
    def test_download_image_skip_download(self):
        """Test download_image with skip download"""
        with patch('os.path.exists') as mock_os_path_exists, \
             patch('common.Commons.is_image_error') as mock_is_image_error:
            mock_os_path_exists.return_value = True
            mock_is_image_error.return_value = False
            result = download_image("https://example.com/image.jpg", "https://example.com", "local_image.jpg")
            self.assertEqual(result, 200)
    
class TestCommonIsImageError(unittest.TestCase):
    @patch('common.Commons.Image.open')
    @patch('common.Commons.io.imread')
    def test_is_image_error_success(self, mock_imread, mock_image_open):
        """Test is_image_error with success"""
        # Setup
        mock_img = Mock()
        mock_img.verify.return_value = None  # verify() returns None on success
        mock_image_open.return_value = mock_img
        mock_imread.return_value = Mock()  # Simulate successful imread

        # Execute
        result = is_image_error("test.jpg")

        # Assert
        self.assertFalse(result)
        mock_image_open.assert_called_once_with("test.jpg")
        mock_img.verify.assert_called_once()
        mock_imread.assert_called_once_with("test.jpg")
        
    @patch('common.Commons.Image.open')
    def test_is_image_error_failed1(self, mock_image_open):
        """Test is_image_error with failed 1"""
        mock_img = Mock()
        mock_img.verify.side_effect = Exception("Mock verify error")
        mock_image_open.return_value = mock_img
        
        result = is_image_error("test.jpg")
        
        self.assertTrue(result)
        
    @patch('common.Commons.Image.open')
    @patch('common.Commons.io.imread')
    def test_is_image_error_failed2(self, mock_imread, mock_image_open):
        """Test is_image_error with failed 2"""
        mock_img = Mock()
        mock_img.verify.return_value = None
        mock_image_open.return_value = mock_img
        mock_imread.side_effect = Exception("Mock imread error")

        result = is_image_error("test.jpg")
        
        self.assertTrue(result)
        
class TestCommonExecuteProcess(unittest.TestCase):
    def test_execute_process_without_threading(self):
        """Test execute_process without threading"""
        
        def mock_function(x):
            print(x)
        
        test_list = [1, 2, 3]
        
        # Execute with threading disabled
        with patch('common.Commons.using_thread', False):
            execute_process(mock_function, test_list, use_thread=False)

    def test_execute_process_with_threading(self):
        """Test execute_process with threading"""
        # Test setup
        def mock_function(x):
            print(x)
        
        test_list = [1, 2, 3]
        
        # Execute with threading enabled
        with patch('common.Commons.using_thread', True):
            execute_process(mock_function, test_list, use_thread=True)
        
class TestCommonInitApp(unittest.TestCase):
    @patch('common.Commons.check_and_create_folder')
    @patch('common.Commons.check_file_exist')
    @patch('shutil.copy')
    @patch('os.path.exists')
    @patch('os.path.join')
    def test_init_app(self, mock_os_path_join, mock_os_path_exists, mock_shutil_copy, mock_check_file_exist, mock_check_and_create_folder):
        """Test init_app"""
        mock_check_and_create_folder.return_value = None
        mock_check_file_exist.return_value = True
        mock_shutil_copy.return_value = None
        mock_os_path_exists.return_value = False
        mock_os_path_join.return_value = "test"
        init_app()
        assert mock_check_and_create_folder.called_with(folder_running_resource, create=True)
        assert mock_check_file_exist.call_count == len(resource_cp_files)
        assert mock_shutil_copy.call_count == len(resource_cp_files)

    @patch('common.Commons.check_and_create_folder')
    def test_init_app_exception(self, mock_check_and_create_folder):
        """Test init_app with exception"""
        mock_check_and_create_folder.side_effect = Exception("Mock error")
        with self.assertRaises(Exception):
            init_app()

