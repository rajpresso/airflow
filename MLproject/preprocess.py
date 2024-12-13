import numpy as np  # 수치 계산을 위한 numpy 라이브러리를 임포트

class TitanicPreprocess:
    def __init__(self):  # 클래스 초기화 메서드
        pass  # 초기화 메서드는 현재 아무 작업도 하지 않음

    def run_preprocessing(self, data):  # 전처리 메서드
        data = self._set_initial(data)  # 이름에서 호칭을 추출하여 Initial 컬럼 생성
        data = self._set_fill_na(data)  # 결측값을 채움
        data = self._set_feature(data)  # 새로운 피처를 생성
        data = self._set_replace(data)  # 값을 숫자로 변환 및 불필요한 컬럼 삭제

        return data  # 전처리된 데이터를 반환

    def _set_fill_na(self, data):  # 결측값을 채우는 메서드
        data.loc[(data['Age'].isnull()) & (data['Initial'] == 'Mr'), 'Age'] = 33  # 'Mr'의 결측값을 33으로 채움
        data.loc[(data['Age'].isnull()) & (data['Initial'] == 'Master'), 'Age'] = 5  # 'Master'의 결측값을 5로 채움
        data.loc[(data['Age'].isnull()) & (data['Initial'] == 'Mrs'), 'Age'] = 36  # 'Mrs'의 결측값을 36으로 채움
        data.loc[(data['Age'].isnull()) & (data['Initial'] == 'Miss'), 'Age'] = 22  # 'Miss'의 결측값을 22로 채움
        data.loc[(data['Age'].isnull()) & (data['Initial'] == 'Other'), 'Age'] = 46  # 'Other'의 결측값을 46으로 채움
        data['Embarked'].fillna('S', inplace=True)  # 'Embarked' 결측값을 'S'로 채움

        return data  # 결측값을 채운 데이터를 반환

    def _set_initial(self, data):  # 이름에서 호칭을 추출하는 메서드
        data['Initial'] = 0  # 초기값 설정
        data['Initial'] = data['Name'].str.extract('([A-Za-z]+)\.')  # 이름에서 호칭 추출
        data['Initial'].replace(
            ['Mlle', 'Mme', 'Ms', 'Dr', 'Major', 'Lady', 'Countess', 'Jonkheer', 'Col', 'Rev', 'Capt', 'Sir', 'Don', 'Dona'],
            ['Miss', 'Miss', 'Miss', 'Mr', 'Mr', 'Mrs', 'Mrs', 'Other', 'Other', 'Other', 'Mr', 'Mr', 'Mr', 'Other'],
            inplace=True)  # 호칭을 표준화된 값으로 대체

        return data  # 호칭이 추가된 데이터를 반환

    def _set_feature(self, data):  # 새로운 피처를 생성하는 메서드
        data['Fare'] = data["Fare"].map(lambda i: np.log(i) if i > 0 else 0)  # 요금을 로그 변환
        data['Age_band'] = 0  # 나이대 초기값 설정
        data['Alone'] = 0  # 혼자인지 여부 초기값 설정
        data['Family_Size'] = 0  # 가족 크기 초기값 설정

        data.loc[data['Age'] <= 16, 'Age_band'] = 0  # 나이대 설정
        data.loc[(data['Age'] > 16) & (data['Age'] <= 32), 'Age_band'] = 1
        data.loc[(data['Age'] > 32) & (data['Age'] <= 48), 'Age_band'] = 2
        data.loc[(data['Age'] > 48) & (data['Age'] <= 64), 'Age_band'] = 3
        data.loc[data['Age'] > 64, 'Age_band'] = 4

        data['Family_Size'] = data['Parch'] + data['SibSp']  # 가족 크기 계산

        data.loc[data.Family_Size == 0, 'Alone'] = 1  # 혼자인 경우 Alone 컬럼을 1로 설정

        return data  # 새로운 피처가 추가된 데이터를 반환

    def _set_replace(self, data):  # 값을 숫자로 변환하고 불필요한 컬럼을 삭제하는 메서드
        data['Sex'].replace(['male', 'female'], [0, 1], inplace=True)  # 성별을 숫자로 변환
        data['Embarked'].replace(['S', 'C', 'Q'], [0, 1, 2], inplace=True)  # 탑승항구를 숫자로 변환
        data['Initial'].replace(['Mr', 'Mrs', 'Miss', 'Master', 'Other'], [0, 1, 2, 3, 4], inplace=True)  # 호칭을 숫자로 변환
        data.drop(['Name', 'Age', 'Ticket', 'Cabin', 'PassengerId'], axis=1, inplace=True)  # 불필요한 컬럼 삭제

        return data  # 값이 변환된 데이터를 반환
