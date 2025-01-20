"""
Vectra Automated Response 設定範例
本腳本用於配置主機、帳戶及檢測項的自動化阻止邏輯，並支援與第三方安全系統整合。
"""

### 一般設定 (GENERAL SETUP)

# 定義 Vectra Detect "Brain" 的 API 存取網址 (REST API 基本 URL)
COGNITO_URL = ["https://example.vectra.local"]  # 修改為您的 Vectra Detect 伺服器 URL

# 是否將日誌輸出至檔案
LOG_TO_FILE = True  # 設為 True 可將日誌寫入檔案
LOG_FILE = "var.log"  # 日誌檔案名稱

# 腳本執行的間隔時間（分鐘）
SLEEP_MINUTES = 5  # 若腳本設定為迴圈模式，此為迴圈間隔

# 是否使用 Vectra API v3
V3 = False  # 若使用 v3 API，設為 True

# 第三方安全系統客戶端的支援列表
# 可用的選項包括多個設備廠牌（'bitdefender', 'cisco_amp', 'cisco_fmc', 'cisco_ise',
# 'cisco_nxos', 'cisco_pxgrid', 'clearpass', 'cortex', 'endgame', 'external_call', 'fortinet', 'forti_edr',
# 'harmony', 'meraki', 'pan', 'pulse_nac', 'sophos', 'test_client', 'trendmicro_apexone',
# 'trendmicro_cloudone', 'trendmicro_visionone', 'vmware', 'windows_shutdown', 'withsecure_elements',
# 'xtreme_networks_nbi'）
THIRD_PARTY_CLIENTS = ["clearpass"]  # 修改為您的整合需求


### 自動阻止的允許時間窗 (ALLOWED BLOCKING WINDOW)

# 定義允許自動阻止的天數（0 = 星期日, 6 = 星期六）
BLOCK_DAYS = [0, 1, 2, 3, 4, 5, 6]  # 設定為整週都允許執行

# 定義允許阻止的時間範圍（24 小時制）
# BLOCK_START_TIME = 0  # 開始時間，預設為午夜 0 點
BLOCK_START_TIME = 0  # 開始時間，午夜 0 點
# BLOCK_END_TIME = 0    # 結束時間，預設為午夜 0 點（無限制）
BLOCK_END_TIME = 23   # 結束時間，晚上 11 點


### 內部 IP 阻止 (INTERNAL IP BLOCKING)

# 當主機被標記為以下標籤時，執行阻止動作
BLOCK_HOST_TAG = "vectra_host_block"

# 不會被阻止的主機群組名稱
NO_BLOCK_HOST_GROUP_NAME = "NoBlock"

# 將會被阻止的主機群組名稱
BLOCK_HOST_GROUP_NAME = "Block"

# 主機的威脅與確定性分數門檻，符合條件將觸發阻止
BLOCK_HOST_THREAT_CERTAINTY = (100, "and", 100)  # 使用 "and" 或 "or" 決定條件邏輯

# 針對 V3 API 的主機緊急性分數門檻
BLOCK_HOST_URGENCY = None  # 若使用 V3 API，啟用此參數

# 特定檢測類型出現時會觸發阻止動作
BLOCK_HOST_DETECTION_TYPES = ["External Remote Access", "Hidden DNS Tunnel"]
BLOCK_HOST_DETECTION_TYPES_MIN_TC_SCORE = (100, "and", 100)


### 外部 IP 阻止 (EXTERNAL IP BLOCKING)

# 主機的威脅與確定性分數門檻，若符合則阻止所有檢測中的外部 IP
EXTERNAL_BLOCK_HOST_TC = (100, "and", 100)

# 當檢測項被標記為以下標籤時，阻止外部 IP
EXTERNAL_BLOCK_DETECTION_TAG = "block"

# 指定會觸發外部 IP 阻止的檢測類型
EXTERNAL_BLOCK_DETECTION_TYPES = ["Command&Control", "Data Smuggler"]

# 定義靜態目的地 IP 檔案路徑
STATIC_BLOCK_DESTINATION_IPS = "static_dst_ips_to_block.txt"


### 帳戶阻止 (ACCOUNT BLOCKING)

# 當帳戶被標記為以下標籤時，執行阻止動作
BLOCK_ACCOUNT_TAG = "vectra_account_block"

# 不會被阻止的帳戶群組名稱
NO_BLOCK_ACCOUNT_GROUP_NAME = "NoBlock"

# 將會被阻止的帳戶群組名稱
BLOCK_ACCOUNT_GROUP_NAME = "Block"

# 帳戶的威脅與確定性分數門檻
BLOCK_ACCOUNT_THREAT_CERTAINTY = (100, "and", 100)

# 針對 V3 API 的帳戶緊急性分數門檻
BLOCK_ACCOUNT_URGENCY = None  # 若使用 V3 API，啟用此參數

# 特定檢測類型出現時會觸發阻止動作
BLOCK_ACCOUNT_DETECTION_TYPES = ["Credential Stuffing", "Unauthorized Access"]
BLOCK_ACCOUNT_DETECTION_TYPES_MIN_TC_SCORE = (100, "and", 100)


### 通知設定 (NOTIFICATION SETUP)

# 電子郵件通知
SEND_EMAIL = True  # 啟用電子郵件通知
SMTP_SERVER = "smtp.example.com"  # SMTP 伺服器位址
SMTP_PORT = 587  # SMTP 埠
SRC_EMAIL = "alert@example.com"  # 發件人地址
DST_EMAIL = "admin@example.com"  # 收件人地址
SMTP_AUTH = True  # 是否需要 SMTP 身份驗證
SMTP_USER = "smtp_user"
SMTP_PASSWORD = "smtp_password"  # 建議使用環境變數存儲密碼以提高安全性

# Syslog 通知
SEND_SYSLOG = True  # 啟用 Syslog 通知
SYSLOG_SERVER = "syslog.example.com"  # Syslog 伺服器位址
SYSLOG_PORT = 514  # Syslog 埠
SYSLOG_PROTO = "TCP"  # Syslog 協議，TCP 或 UDP
SYSLOG_FORMAT = "CEF"  # 格式：標準或 CEF 格式


### 使用提示
"""
1. 根據需求修改以上配置，確保正確的 Vectra URL、標籤與阻止條件已設定。
2. 若需執行腳本，可在命令行中執行：python3 vectra_automated_response.py --loop
3. 若使用外部工具執行阻止（如防火牆），請檢查 `STATIC_BLOCK_DESTINATION_IPS` 文件內容。
4. 啟用通知功能，便於監控腳本運行狀態與阻止行為。
"""
