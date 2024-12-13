import pandas as pd  # pandas 라이브러리를 임포트하여 데이터 분석 기능을 사용

class DataIOSteam:
    
    def get_data(self, path, f_name, flag=False):  # 데이터 로드 메서드 정의
        if flag:
            # flag가 True이면 xcom을 통해 path를 받기 때문에 전체 경로 값이 f_name에 존재함
            return pd.read_csv(f'{f_name}.csv')  # 파일 이름에 .csv를 붙여 전체 경로에서 파일을 읽음
        return pd.read_csv(f'{path}/{f_name}.csv')  # path와 f_name을 결합하여 파일을 읽음
    
    def get_X_y(self, data):  # 입력 변수(X)와 타겟 변수(y)를 분리하는 메서드 정의
        X = data[data.columns[1:]]  # 첫 번째 열을 제외한 모든 열을 X로 설정
        X = X[['Sex', 'Age_band', 'Pclass']]  # 필요한 열만 선택하여 X에 저장
        y = data['Survived']  # 'Survived' 열을 y로 설정

        return X, y  # X와 y를 반환
