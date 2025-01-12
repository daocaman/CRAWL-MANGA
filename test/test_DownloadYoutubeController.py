import unittest
from unittest.mock import patch, MagicMock
import yt_dlp
from controllers.DownloadYoutubeController import download_from_youtube, download_yt_process, get_playlist_videos
from common.Messages import MSG_ERR_CONTROLLER_DOWNLOAD_YOUTUBE

class TestDownloadYoutubeController(unittest.TestCase):
    
    def setUp(self):
        self.url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.url_playlist = "https://www.youtube.com/playlist?list=PLZlA0Gqn_vJfMf5I154mRBoaT5PqMl23L"
        self.type_download_video = "video"
        self.type_download_audio = "audio"
        self.quality_360 = "360"
        
        self.mock_response = {
            "entries": [
                {
                    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                },
                {
                    "url": "https://www.youtube.com/watch?v=xvFZjo5PgG0"
                }
            ]
        }
    
    def test_download_from_youtube_success(self):
        """Test download_from_youtube with success"""
        with patch('common.Validations.check_valid_video_url') as mock_check_valid_video_url, \
            patch('common.Validations.check_valid_playlist_url') as mock_check_valid_playlist_url, \
            patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
            patch('yt_dlp.YoutubeDL') as mock_ydl:

            mock_youtube_dl = MagicMock()
            mock_youtube_dl.download.return_value = True
            
            mock_check_valid_video_url.return_value = True
            mock_check_valid_playlist_url.return_value = True
            mock_check_file_exist.return_value = True
            mock_check_and_create_folder.return_value = True
            mock_ydl.return_value = mock_youtube_dl

            download_from_youtube(self.url, self.type_download_video, self.quality_360)

    def test_download_from_youtube_failure(self):
        """Test download_from_youtube with failure"""
        with patch('common.Validations.check_valid_video_url') as mock_check_valid_video_url, \
            patch('common.Validations.check_valid_playlist_url') as mock_check_valid_playlist_url, \
            patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
            patch('yt_dlp.YoutubeDL') as mock_ydl:
                
            mock_youtube_dl = MagicMock()
            mock_youtube_dl.download.side_effect = Exception("Error downloading video")
                
            mock_check_valid_video_url.return_value = True
            mock_check_valid_playlist_url.return_value = True
            mock_check_file_exist.return_value = True
            mock_check_and_create_folder.return_value = True
            mock_ydl.return_value.__enter__.return_value = mock_youtube_dl

            with self.assertRaises(Exception) as exc_info:
                download_yt_process({"link": self.url, "type": self.type_download_audio, "quality": self.quality_360})
                
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_DOWNLOAD_YOUTUBE.format("download_from_youtube"))
            
    def test_get_playlist_from_youtube_success(self):
        """Test get_playlist_from_youtube with success"""
        with patch('common.Validations.check_valid_playlist_url') as mock_check_valid_playlist_url, \
            patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
            patch('yt_dlp.YoutubeDL') as mock_ydl:

            mock_youtube_dl = MagicMock()
            mock_youtube_dl.extract_info.return_value = self.mock_response

            mock_check_valid_playlist_url.return_value = True
            mock_check_file_exist.return_value = True
            mock_check_and_create_folder.return_value = True
            mock_ydl.return_value.__enter__.return_value = mock_youtube_dl

            result = get_playlist_videos(self.url_playlist)
            self.assertEqual(len(result), 2)

    def test_get_playlist_from_youtube_failure(self):
        """Test get_playlist_from_youtube with failure"""
        with patch('common.Validations.check_valid_playlist_url') as mock_check_valid_playlist_url, \
            patch('common.Validations.check_file_exist') as mock_check_file_exist, \
            patch('common.Validations.check_and_create_folder') as mock_check_and_create_folder, \
            patch('yt_dlp.YoutubeDL') as mock_ydl:

            mock_youtube_dl = MagicMock()
            mock_youtube_dl.extract_info.side_effect = Exception("Error downloading video")

            mock_check_valid_playlist_url.return_value = True
            mock_check_file_exist.return_value = True
            mock_check_and_create_folder.return_value = True
            mock_ydl.return_value.__enter__.return_value = mock_youtube_dl

            with self.assertRaises(Exception) as exc_info:
                get_playlist_videos(self.url_playlist)
                
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_DOWNLOAD_YOUTUBE.format("get_playlist_videos"))

