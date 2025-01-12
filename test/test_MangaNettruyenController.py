import unittest
from unittest.mock import patch, MagicMock
from controllers.MangaNettruyenController import get_link_chapter_nettruyen, get_list_image_nettruyen
from common.Messages import MSG_ERR_CONTROLLER_NETTRUYEN

class TestMangaNettruyenController (unittest.TestCase):
    def setUp(self):
        self.link = "https://nettruyenviet.com/truyen-tranh/van-co-chi-ton"
        self.mock_response = """
        <div id="nt_listchapter">
            <ul id="desc">
                <a href="https://nettruyen.com/chapter-4"></a>
                <a href="https://nettruyen.com/chapter-3"></a>
                <a href="https://nettruyen.com/chapter-2"></a>
                <a href="https://nettruyen.com/chapter-1"></a>
            </ul>
        </div>
        """
        self.mock_response_chapter_html = """
            <html>
                <title>Manga Name Chap 1 Next Chap 2</title>
                <div class="page-chapter">
                    <img data-src="image1.jpg" />
                </div>
                <div class="page-chapter">
                    <img data-sv1="image2.jpg" />
                </div>
            </html>
        """
        
        self.mock_response_chapter_html_2 = """
            <html>
                <title>Manga Name Chap 1.1 Next Chap 2</title>
                <div class="page-chapter">
                    <img data-src="image1.jpg" />
                </div>
                <div class="page-chapter">
                    <img data-sv1="image2.jpg" />
                </div>
            </html>
        """

    def tearDown(self):
        self.link = None
        self.num_chap = None
        self.start_idx = None

    def test_get_link_chapter_nettruyen_success_full(self):
        with patch('requests.get') as mock_get:
            
            mock_response = MagicMock()
            mock_response.content = self.mock_response
            mock_get.return_value = mock_response

            result = get_link_chapter_nettruyen(self.link, -1, -1)
            self.assertEqual(len(result[1]), 4)

    def test_get_link_chapter_nettruyen_success_num_chap(self):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.content = self.mock_response
            mock_get.return_value = mock_response

            server, list_chapters = get_link_chapter_nettruyen(self.link, 2, 0)
            self.assertEqual(server, "https://nettruyenviet.com")
            self.assertEqual(len(list_chapters), 2)
            self.assertEqual(list_chapters[0], "https://nettruyen.com/chapter-1")
            
    def test_get_link_chapter_nettruyen_success_start_idx(self):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.content = self.mock_response_chapter_html
            mock_get.return_value = mock_response

            server, list_chapters = get_link_chapter_nettruyen(self.link, -1, 1)
            self.assertEqual(server, "https://nettruyenviet.com")
            self.assertEqual(len(list_chapters), 3)
            self.assertEqual(list_chapters[0], "https://nettruyen.com/chapter-2")

    def test_get_link_chapter_nettruyen_error(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Error")
            with self.assertRaises(Exception) as exc_info:
                get_link_chapter_nettruyen(self.link, -1, -1)
            self.assertEqual(str(exc_info.exception), MSG_ERR_CONTROLLER_NETTRUYEN.format("get_link_chapter_nettruyen"))

    def test_get_list_image_nettruyen_success(self):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.content = self.mock_response_chapter_html_2
            mock_get.return_value = mock_response

            title, list_images = get_list_image_nettruyen(self.link)
            self.assertEqual(title, "Chapter 0001")
            self.assertEqual(len(list_images), 2)
            self.assertEqual(list_images[0], "https://image1.jpg")
            self.assertEqual(list_images[1], "https://image2.jpg")

    def test_get_list_image_nettruyen_success_2(self):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.content = self.mock_response_chapter_html_2
            mock_get.return_value = mock_response

            title, list_images = get_list_image_nettruyen(self.link)
            self.assertEqual(title, "Chapter 0001.1")
            self.assertEqual(len(list_images), 2)
            self.assertEqual(list_images[0], "https://image1.jpg")
            self.assertEqual(list_images[1], "https://image2.jpg")

