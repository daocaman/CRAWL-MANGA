import unittest
from unittest.mock import patch, MagicMock
from controllers.DownloadCoverController import download_cover_process
from common.Messages import MSG_ERR_CONTROLLER_DOWNLOAD_COVER

class TestDownloadCoverController(unittest.TestCase):
    
    def setUp(self):
        self.response_json = {
            "data": [
                {
                    "attributes": {
                        "volume": "1",
                        "fileName": "test1.jpg",
                        "locale": "en"
                    },
                    "relationships": [{"id": "123"}]
                },
                {
                    "attributes": {
                        "volume": "1",
                        "fileName": "test2.jpg",
                        "locale": "ja"
                    },
                    "relationships": [{"id": "456"}]
                },
                {
                    "attributes": {
                        "volume": "2",
                        "fileName": "test3.jpg",
                        "locale": "en"
                    },
                    "relationships": [{"id": "789"}]
                }
            ],
            "total": 3
        }
        
        self.link = "https://mangadex.org/title/123/manga-name"
        
        self.mock_response = MagicMock()
        
        
    def test_download_cover_process_success(self):
        with patch('requests.get') as mock_get, \
            patch('os.path.exists') as mock_os_path_exists, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder:
            
            mock_os_path_exists.return_value = True
            mock_check_and_create_folder.return_value = True
            self.mock_response.json.return_value = self.response_json
            mock_get.return_value = self.mock_response
            download_cover_process(self.link)

    def test_download_cover_process_failure(self):
        with patch('os.path.exists') as mock_os_path_exists, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder:
            mock_os_path_exists.return_value = False
            mock_check_and_create_folder.return_value = False
            with self.assertRaises(Exception) as exc_info:
                download_cover_process(self.link)
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_DOWNLOAD_COVER.format("download_cover_process"))
