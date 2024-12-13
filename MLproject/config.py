import os  # 운영 체제 관련 기능을 제공하는 모듈을 임포트
import pathlib  # 파일 시스템 경로를 조작하기 위한 pathlib 모듈을 임포트

class PathConfig:
    def __init__(self):  # 클래스 초기화 메서드
        self.project_path = pathlib.Path(__file__).parent.resolve()  # 현재 파일의 디렉토리를 기준으로 프로젝트 경로를 설정
        self.titanic_path = f"{self.project_path}/data/titanic"  # 타이타닉 데이터 경로를 설정

class EnvConfig:
    def get_gender_mapping_code(self):  # 성별 매핑 정보를 반환하는 메서드
        gender_mapping_info = {
            'male' : 0,  # 남성 성별을 0으로 매핑
            'female' : 1,  # 여성 성별을 1로 매핑
        }

        return gender_mapping_info  # 성별 매핑 정보를 반환
    
    def get_column_list(self):  # 사용할 열 목록을 반환하는 메서드
        columns_list = ['Sex', 'Age_band', 'Pclass']  # 열 목록을 리스트로 정의
        return columns_list  # 열 목록을 반환
