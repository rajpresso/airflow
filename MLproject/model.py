import sys  # 시스템 관련 기능을 제공하는 모듈을 임포트

from sklearn.ensemble import RandomForestClassifier  # 랜덤 포레스트 분류기를 사용하기 위해 임포트

class TitanicModeling:
    def __init__(self):  # 클래스 초기화 메서드
        pass  # 초기화 메서드는 현재 아무 작업도 하지 않음

    def run_sklearn_modeling(self, X, y, n_estimator):  # 모델을 실행하는 메서드
        model = self._get_rf_model(n_estimator)  # 랜덤 포레스트 모델을 생성

        model.fit(X, y)  # 모델을 학습 데이터에 맞추어 훈련

        model_info = {
            'score' : {
                'model_score' :  model.score(X, y)  # 모델의 점수를 계산하여 저장
            },
            'params' : model.get_params()  # 모델의 파라미터를 저장
        }

        return model_info  # 모델 정보를 반환

    def _get_rf_model(self, n_estimator):  # 랜덤 포레스트 모델을 생성하는 메서드
        return RandomForestClassifier(n_estimators=n_estimator, max_depth=5)  # n_estimators와 max_depth를 설정하여 모델 생성
