from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import cv2

test = [
    # ["Chapter 72", 1, 94, "https://mangadex.org/chapter/938553ff-dab3-4ced-902e-2c1f01e68a09/"],
    # ["Chapter 73", 1, 99, "https://mangadex.org/chapter/dc776360-5884-462a-a6e2-ffdc494205df/"],
    # ["Chapter 80", 1, 115, "https://mangadex.org/chapter/7a66c703-e08e-4620-9745-52f94f4eb908/"],
    # ["Chapter 81", 1, 94, "https://mangadex.org/chapter/564a575d-1ef3-4a2d-b94b-5ceb1cf0827f/"],
    # ["Chapter 82", 1, 104, "https://mangadex.org/chapter/006c6b33-4065-4415-aedf-cdf8d124f8e1/"],
    # ["Chapter 83", 1, 95, "https://mangadex.org/chapter/0680a53e-b124-4266-8e4d-acfc4ac2bf2d/"],
    # ["Chapter 84", 1, 99, "https://mangadex.org/chapter/3a4dcf72-ba6e-4b65-a2c0-e087adb1a758/"],
    # ["Chapter 85", 1, 94, "https://mangadex.org/chapter/f107e823-8e9c-443b-b78d-f7f4b4a8f90e/"],
    # ["Chapter 86", 1, 98, "https://mangadex.org/chapter/111456aa-5720-4851-ac3b-5432544a17cd/"],
    # ["Chapter 87", 1, 100, "https://mangadex.org/chapter/451e0c37-1682-4b09-afab-cdceb5cfe34d/"],
    # ["Chapter 88", 1, 102, "https://mangadex.org/chapter/2a1aa06c-2783-491c-a462-96109426fcc7/"],
    # ["Chapter 89", 1, 98, "https://mangadex.org/chapter/a5e1e306-e6b7-4ffb-9884-0c9d39331e1e/"],
    # ["Chapter 90", 1, 101, "https://mangadex.org/chapter/586e989a-1444-49d4-bf08-3abae2664323/"],
    # ["Chapter 91", 1, 99, "https://mangadex.org/chapter/ba36b141-e5da-4ae1-b1c3-305ede926f8f/"],
    # ["Chapter 92", 1, 102, "https://mangadex.org/chapter/51307e3b-5759-45b7-8ed0-786e9e230bd4/"],
    # ["Chapter 93", 1, 95, "https://mangadex.org/chapter/278701bd-f0a7-4fb4-a022-aa458009dfd6/"],
    # ["Chapter 94", 1, 99, "https://mangadex.org/chapter/44114acb-795f-4bf5-8b52-d047d7fa54d3/"],
    # ["Chapter 95", 1, 103, "https://mangadex.org/chapter/36164e71-edba-42e7-afbe-4f820a73db97/"],
    # ["Chapter 96", 1, 95, "https://mangadex.org/chapter/b154e1c8-8726-4e05-a7bc-ede5d7da3813/"],
    # ["Chapter 97", 1, 93, "https://mangadex.org/chapter/a82c472e-47b5-4a2f-894b-ff4119c06ba6/"],
    # ["Chapter 98", 1, 94, "https://mangadex.org/chapter/84cb68dd-496a-4fad-afbc-db1ace87588f/"],
    ["Chapter 99", 1, 96, "https://mangadex.org/chapter/ce722422-f043-4895-a2e8-cc7bfc75d275/"],
]


driver = webdriver.Firefox(executable_path=r'./geckodriver.exe')
for chap in test:
    if not os.path.exists(chap[0]):
        os.mkdir(chap[0])

    for i in range(chap[1], chap[2]+1):

        if i == 1:
            driver.get(chap[3]+str(i))
            time.sleep(5)
            driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_RIGHT)
            time.sleep(1)
            driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_LEFT)
        else:
            driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_RIGHT)
            time.sleep(2)
        driver.save_screenshot('test.png')

        img = cv2.imread('test.png')

        crop_img = img[0:956, 661: 661+598]

        cv2.imwrite(chap[0]+"/"+str(i)+".png", crop_img)

driver.close()
