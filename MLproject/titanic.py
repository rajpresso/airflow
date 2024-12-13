from MLproject.preprocess import TitanicPreprocess  # TitanicPreprocess 클래스를 임포트
from MLproject.config import PathConfig  # PathConfig 클래스를 임포트
from MLproject.dataio import DataIOSteam  # DataIOSteam 클래스를 임포트
from MLproject.model import TitanicModeling  # TitanicModeling 클래스를 임포트

# 모든 스크립트들의 클래스를 상속 받음.
class TitanicMain(TitanicPreprocess, PathConfig, TitanicModeling, DataIOSteam):
    def __init__(self):  # 클래스 초기화 메서드
        TitanicPreprocess.__init__(self)  # TitanicPreprocess 초기화
        PathConfig.__init__(self)  # PathConfig 초기화
        TitanicModeling.__init__(self)  # TitanicModeling 초기화
        DataIOSteam.__init__(self)  # DataIOSteam 초기화

    # Airflow에서 PythonOperator를 사용할 때, kwargs를 통해 태스크 인스턴스(task_instance)와 같은 컨텍스트 정보를 전달. 
    def prepro_data(self, f_name, **kwargs):  # 데이터 전처리 메서드
        # fname = train.csv
        data = self.get_data(self.titanic_path, f_name)  # 데이터를 로드
        data = self.run_preprocessing(data)  # 데이터 전처리 수행
        data.to_csv(f"{self.titanic_path}/prepro_titanic.csv", index=False)  # 전처리된 데이터를 저장
        kwargs['task_instance'].xcom_push(key='prepro_csv', value=f"{self.titanic_path}/prepro_titanic")  # xcom에 전처리된 파일 경로를 푸시
        return "end prepro"  # 전처리 완료 메시지 반환

    # Airflow에서 PythonOperator를 사용할 때, kwargs를 통해 태스크 인스턴스(task_instance)와 같은 컨텍스트 정보를 전달. 
    def run_modeling(self, n_estimator, flag, **kwargs):  # 모델 실행 메서드
        # n_estimator = 100
        f_name = kwargs["task_instance"].xcom_pull(key='prepro_csv')  # xcom에서 전처리된 파일 경로를 가져옴
        data = self.get_data(self.titanic_path, f_name, flag)  # 데이터를 로드
        X, y = self.get_X_y(data)  # X와 y를 분리
        model_info = self.run_sklearn_modeling(X, y, n_estimator)  # 모델 실행
        kwargs['task_instance'].xcom_push(key='result_msg', value=model_info)  # xcom에 모델 결과를 푸시
        return "end modeling"  # 모델링 완료 메시지 반환
