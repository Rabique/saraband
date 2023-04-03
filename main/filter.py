
from main import app, datetime, time


@app.template_filter('formatdatetime')
def format_datetime(value):
    if value is None:
        return ""

    # 현재 시간 타임스탬프를 구합니다.
    now_timestamp = time.time()
    
    # 현재 시간 타임스탬프를 현재 시간객체, UTC 시간 기준 시간객체로 변환하여
    # 현재 시간에서 UTC 시간을 빼 시간차를 구합니다.
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    
    # 구해진 시간차만큼 저장된 시간정보에 더해줍니다.
    value = datetime.fromtimestamp((int(value) / 1000)) + offset
    
    # 원하는 형태의 시간 포맷으로 변경합니다.
    return value.strftime('%Y-%m-%d %H:%M:%S')
