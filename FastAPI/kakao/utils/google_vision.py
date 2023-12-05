import os
import io
import time

#!pip install --upgrade google-cloud-vision   # Cloud Vision API 설치 => 프로젝트에서 Cloud Vision API 사용으로 설정해야함
from google.cloud import vision

class Google_Vision:
    
    def __init__(self, service_account_jsonfile_path:str):
        assert service_account_jsonfile_path, f'service_account_jsonfile_path is empty'
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_jsonfile_path
        client_options = {'api_endpoint': 'eu-vision.googleapis.com'}
        self.client = vision.ImageAnnotatorClient(client_options=client_options)
        
        return
    
    
    def __del__(self):
        return
    
    # URL 이미지 OCR 텍스트 추출
    def ocr_url(self, url:str):
        
        assert url, f"url is empty"  
        start_time = time.time()
        
        #client = vision.ImageAnnotatorClient()
        image = vision.Image()
        image.source.image_uri = url
    
        res:list = []
        #time.sleep(1)
        
        for idx in range(2):
            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            #print(f'texts:\n{texts}\n')
        
            if response.error.message:
                if idx == 0:
                    continue
                else:
                    res.append(f'{response.error.message}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors')
                    return res, 1001
            else:
                break
        
        for text in texts:
            res.append(text.description)
             
            #vertices = [f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices]
            #print("bounds: {}".format(",".join(vertices)))
          
        # 소요된 시간을 계산합니다.
        end_time = time.time()
        elapsed_time = "{:.2f}".format(end_time - start_time)
        print(f'time:{elapsed_time}\n')

        return res, 0
    
    # 로컬 이미지 OCR 텍스트 추출
    def ocr_file(self, filepath:str):
        
        assert filepath, f"filepath is empty"
        start_time = time.time()
        
        # 로컬이미지 열기
        with io.open(filepath, 'rb') as image_file:
            content = image_file.read()
            
        #Request to Google Cloud Vision API
        #API 호출 방식은 매우 간단합니다. 
        #만약 PermissionDenied: 403 This API method requires billing to be enabled. 
        #오류가 발생하였다면 결제 계정 설정이 안된 경우 입니다.  
        #Google Cloud Platform Console로 이동하여 결제 정보 설정을 하시면 됩니다.

        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        
        res:list = []
        if response.error.message:
            res.append(f'{response.error.message}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors')
            return res
        
        for text in texts:
            res.append(text.description)
             
            #vertices = [f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices]
            #print("bounds: {}".format(",".join(vertices)))
          
        # 소요된 시간을 계산합니다.
        end_time = time.time()
        elapsed_time = "{:.2f}".format(end_time - start_time)
        print(f'time:{elapsed_time}\n')

        return res
        
        