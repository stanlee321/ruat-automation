import os

configs = {
    "BUCKET_NAME" : os.environ['BUCKET_NAME'],
    "OCR_API_URL" : os.environ['OCR_API_URL'],
    "NEWTON_PAGE_NAME" : "./data/page_3.html",
    "NEWTON_FORMS_PAGE_NAME" : "./data/page_4.html",
    "NEWTON_FORMS_TABLES_PAGE_NAME" : "./data/page_5.html",
    "CAPTCHA_IMAGE_PATH" : "./data/captcha.png",
    "DONE" : False,
    "MANUAL" : False
}
