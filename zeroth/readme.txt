
20190823 검색 알고리즘 새로 정리, 검색 결과 표시 형식 변경
20190801 (Litmus Project v0.4 시작) 
    - Login 기능 제거, ColorPicker 제거, 3D Plot 제거
    - DB 1600 json 파일 업데이트 및 Cell Group json 파일 추가
    - Group 및 Cell 연산 함수 구현 및 표시
    - Color Coordinate 표시 내용 축약

20190405 Supernova 컨셉 수립, proximity 계산 및 plot 과 geo map 표시
20190404 Deploy 버전 정돈 (최초)
20190328 Geo Map 기능 구현
20190326 MSlogin 기능 구현, 컬러 버튼 리스트 방법 변경
20190322 Litmus Project v0.2 시작
    - ver 0.1 (Litmus 20190312) 기반 upgrade
    - DB 변경:  SQL(Model:ColorDB, sqlite) -> Memory(Model: Litmus, read from json)
    - Work directory : (Office Gram) C:\Users\COYOON\Web\LitmusProject>
                       (Home Mac) C:\Users\Hexanomy\Web\LitmusProject>

(Litmus Project v0.1 이전 log)
20190312 Color Info에 Plotly 3D scatter 플롯 추가
20190306 Color Info에 neighbor 정보 표시 및 Bootstrap CDN 추가
20190305 Color Search (Name & Hexa) 기능 구현
20190228 RGB Sphere 계산 기능 구현
20190208 Library Backup 기능 (Json 파일로 저장)
20190124 color_index 에 각종 color index 변환 기능 구현 (HSLV CMYK XYZ Labuv)  
20190115 Json 파일에서 DB 초기화 기능 구현  
20190109 Home 디자인 변경 및 List Collapse 기능 구현 
20190108 color_index 에 color depth 기능 추가 및 ColorDB field 추가 
20190104 color_index 에 rgbhsl 변환 color grouping 기능 추가
20181216 color 리스트에 컬러 버튼 디스플레이 및 colorDB에 group 추가
20181214 color.py 작성, 컬러를 등록하면 컬러 정보를 웹에 출력
20191121 Crispy를 이용하여 부트스트랩 모달에서 모델 폼을 디스플레이
    - work Directory : Office Local C:\Users\COYOON\Web\Litmus>
        pip install : 
        python 3.7.1 64
        env
        django-2.1.3
        django-crispy
    - Model : ColorDB