from datetime import datetime, timedelta  # 날짜 및 시간을 다루기 위한 datetime 모듈 임포트

from airflow import DAG  # DAG 정의를 위한 Airflow 모듈 임포트
from airflow.operators.bash import BashOperator  # Bash 명령어를 실행하기 위한 BashOperator 임포트
from airflow.operators.dummy import DummyOperator  # 더미 연산자를 위한 DummyOperator 임포트
from airflow.operators.python import BranchPythonOperator  # 분기 처리를 위한 BranchPythonOperator 임포트
from airflow.operators.python_operator import PythonOperator  # Python 함수를 실행하기 위한 PythonOperator 임포트
from airflow.utils.trigger_rule import TriggerRule  # 트리거 규칙을 위한 TriggerRule 임포트

import sys, os  # 시스템 및 운영체제 관련 모듈 임포트
sys.path.append(os.getcwd())  # 현재 작업 디렉토리를 시스템 경로에 추가

from MLproject.titanic import *  # 사용자 정의 TitanicMain 클래스를 임포트
from utils.slack_alert import SlackAlert  # Slack 알림을 위한 SlackAlert 클래스 임포트

titanic = TitanicMain()  # TitanicMain 클래스의 인스턴스 생성
slack = SlackAlert("#일반", "your Token")  # SlackAlert 클래스의 인스턴스 생성

# Airflow에서 PythonOperator를 사용할 때, kwargs를 통해 태스크 인스턴스(task_instance)와 같은 컨텍스트 정보를 전달. 
# Airflow는 기본적으로 여러 메타데이터와 태스크의 실행 정보를 kwargs로 전달
def print_result(**kwargs):  # 결과를 출력하는 함수 정의
    r = kwargs["task_instance"].xcom_pull(key='result_msg')  # xcom에서 결과 메시지를 가져옴
    print("message : ", r)  # 결과 메시지를 출력

default_args = {
    'owner': 'owner-name',  # 소유자 이름
    'depends_on_past': False,  # 이전 DAG 실행에 의존하지 않음
    'email': ['your-email@g.com'],  # 알림 이메일 주소
    'email_on_failure': False,  # 실패 시 이메일 알림 사용 안 함
    'email_on_retry': False,  # 재시도 시 이메일 알림 사용 안 함
    'retries': 1,  # 재시도 횟수
    'retry_delay': timedelta(minutes=30),  # 재시도 사이의 지연 시간
}

dag_args = dict(
    dag_id="tutorial-slack-ml-op",  # DAG ID
    default_args=default_args,  # 기본 인수 설정
    description='tutorial DAG ml with slack',  # DAG 설명
    schedule_interval=None,  # DAG 실행 간격
    start_date=datetime(2022, 2, 1),  # DAG 시작 날짜
    tags=['example-sj'],  # DAG 태그
    on_success_callback=slack.success_msg,  # 성공 시 호출할 콜백 함수
    on_failure_callback=slack.fail_msg  # 실패 시 호출할 콜백 함수

)

with DAG( **dag_args ) as dag:  # DAG 정의 시작
    start = BashOperator(
        task_id='start',  # 태스크 ID
        bash_command='echo "start!"',  # 실행할 Bash 명령어
    )

    prepro_task = PythonOperator(
        task_id='preprocessing',  # 태스크 ID
        python_callable=titanic.prepro_data,  # 실행할 Python 함수
        op_kwargs={'f_name': "train"}  # 함수에 전달할 인수
    )
    
    modeling_task = PythonOperator(
        task_id='modeling',  # 태스크 ID
        python_callable=titanic.run_modeling,  # 실행할 Python 함수
        op_kwargs={'n_estimator': 100, 'flag' : True}  # 함수에 전달할 인수
    )

    msg = PythonOperator(
        task_id='msg',  # 태스크 ID
        python_callable=print_result  # 실행할 Python 함수
    )

    complete = BashOperator(
        task_id='complete_bash',  # 태스크 ID
        bash_command='echo "complete~!"',  # 실행할 Bash 명령어
    )

    # 태스크 의존성 설정
    start >> prepro_task >> modeling_task >> msg >> complete
