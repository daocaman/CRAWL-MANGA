import unittest
from unittest.mock import patch, Mock
from controllers.ConvertTSController import convert_ts_to_mp4
from common.Messages import MSG_ERR_CONTROLLER_CONVERT_TS

class TestConvertTSController(unittest.TestCase):
    
    def setUp(self):
        self.test_folder = "/test/folder"
        self.test_files = ["video1.ts", "video2.ts", "other.txt"]
        self.function_name = "convert_ts_to_mp4"
    
    def test_convert_ts_to_mp4_success(self):
        
        with patch('os.path.join') as mock_os_path_join, \
             patch('os.listdir') as mock_os_listdir, \
             patch('os.cpu_count') as mock_os_cpu_count, \
             patch('os.path.exists') as mock_os_path_exists, \
             patch('ffmpeg.input') as mock_ffmpeg_input, \
             patch('ffmpeg.output') as mock_ffmpeg_output, \
             patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder:
                 
            # Mock OS operations
            mock_os_path_join.return_value = self.test_folder
            mock_os_listdir.return_value = self.test_files
            mock_os_cpu_count.return_value = 4
            mock_os_path_exists.return_value = True
            
            # Mock ffmpeg operations
            mock_input_ffmpeg_obj = Mock()
            mock_output_ffmpeg_obj = Mock()
            mock_ffmpeg_input.return_value = mock_input_ffmpeg_obj
            mock_ffmpeg_output.return_value = mock_output_ffmpeg_obj
            mock_ffmpeg_output.global_args.return_value = True
            
            # Mock check_and_create_folder
            mock_check_and_create_folder.return_value = True
            
            # Test convert_ts_to_mp4
            convert_ts_to_mp4(self.test_folder)
            
            # Assertions
            self.assertEqual(mock_ffmpeg_input.call_count, 2)
            self.assertEqual(mock_ffmpeg_output.call_count, 2)
  
    def test_convert_ts_to_mp4_failure(self):
        with patch('os.path.exists') as mock_os_path_exists, \
             patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder:
            mock_os_path_exists.return_value = False
            mock_check_and_create_folder.return_value = False
            with self.assertRaises(Exception) as exc_info:
                convert_ts_to_mp4(self.test_folder)
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_CONVERT_TS.format(self.function_name))
