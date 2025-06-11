# weapon-vpn

웨펀마스터 포트폴리오 운영 중 사용되는 WireGuard VPN 도구입니다.  
Python 기반 GUI로, macOS 또는 Linux 환경에서 사용됩니다.  
(WireGuard VPN 구성이 완료된 상태에서 실행 가능합니다)

---

## 주요 기능

- VPN 연결 (`wg-quick up client.conf`)
- VPN 연결 종료 (`wg-quick down client.conf`)
- 현재 VPN 상태 확인 (`wg show`)
- 버튼 클릭으로 명령 실행 및 결과 메시지 표시
- 상태 표시 영역에 연결 상태 색상으로 구분

---

## 사용법

1. `.env` 파일 생성 및 비밀번호 설정

   ```env
   PASSWORD=your_password
   ```

2. `client.conf` 파일이 실행 디렉토리에 위치해야 합니다.

3. 원하는 폴더에서 Python 가상환경 생성 및 활성화

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. 필요한 패키지 설치
   
   ```bash
   pip install python-dotenv
   ```
   
5. 스크립트 실행
   ```bash
   python main.py
   ```
