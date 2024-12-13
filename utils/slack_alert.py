from slack_sdk import WebClient  # Slack API 클라이언트를 사용하기 위해 WebClient 임포트
from datetime import datetime  # 날짜 및 시간을 다루기 위한 datetime 모듈 임포트

class SlackAlert:
    def __init__(self, channel, token):  # 초기화 메서드
        self.channel = channel  # Slack 채널 설정
        self.client = WebClient(token=token)  # Slack API 클라이언트 생성 및 인증 토큰 설정

    def success_msg(self, msg):  # 작업 성공 시 호출되는 메서드
        text = f"""
            date : {datetime.today().strftime('%Y-%m-%d')}
            alert : 
                Success! 
                    task id : {msg.get('task_instance').task_id}, 
                    dag id : {msg.get('task_instance').dag_id}, 
                    log url : {msg.get('task_instance').log_url},
                    result : {msg.get('task_instance').xcom_pull(key='result_msg')}
                    
            """  # 성공 메시지 텍스트 생성
        self.client.chat_postMessage(channel=self.channel, text=text)  # Slack 채널에 메시지 전송

    def fail_msg(self, msg):  # 작업 실패 시 호출되는 메서드
        text = f"""
            date : {datetime.today().strftime('%Y-%m-%d')}  
            alert : 
                Fail! 
                    task id : {msg.get('task_instance').task_id}, 
                    dag id : {msg.get('task_instance').dag_id}, 
                    log url : {msg.get('task_instance').log_url}
        """  # 실패 메시지 텍스트 생성
        self.client.chat_postMessage(channel=self.channel, text=text)  # Slack 채널에 메시지 전송
