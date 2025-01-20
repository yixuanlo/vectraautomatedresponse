這是一個Vectra Python腳本，旨在簡化與第三方安全廠商的整合。

根據多種輸入參數（詳情如下），此腳本返回需要被阻止/解除阻止的主機、帳戶或檢測項列表。

程式碼中定義了一個抽象類，第三方客戶端需要繼承此類，以便輕鬆整合基礎腳本的工作流程。

由於新增整合僅需擴展該抽象類，建議對所有新的整合需求使用此框架。

支援的第三方整合

目前已實現的第三方整合包括：
	1.	Bitdefender
	2.	External Program
	3.	Cisco AMP
	4.	Cisco FMC
	5.	Cisco ISE
	6.	Cisco Meraki
	7.	Cisco PxGrid
	8.	ClearPass
	9.	Endgame
	10.	Fortinet (FortiOS)
	11.	Harmony
	12.	McAfee EPO
	13.	Palo Alto (Panorama 或單機)
	14.	PAN Cortex
	15.	Pulse Secure NAC
	16.	Sophos 
	17.	Static destination IP blocking
	18.	Trendmicro ApexOne
	19.	Trendmicro CloudOne
	20.	Trendmicro VisionOne
	21.	VMware vSphere
	22.	WatchGuard
	23.	Windows（直接執行 PowerShell 關閉主機）
	24.	WithSecure Elements

整合的特定文檔可以在相關目錄中找到。

需求
	1.	使用以下指令安裝必要的 Python 模組：

pip3 install -r requirements.txt


	2.	必須使用 Vectra API Tools 2.4 版或更高版本，以支援基於帳戶的群組功能。

工作流程

腳本支援基於以下方式的阻止操作：
	•	主機（Host-based）
	•	帳戶（Account-based）
	•	檢測項（Detection-based）

阻止條件定義於 config.py 文件中。

安全憑證存儲

此腳本使用 Python Keyring 套件安全地存儲憑證。
腳本會檢查預設的 Keyring 是否包含必要的憑證，若未找到會提示用戶輸入。
預設配置會在輸入後存儲憑證；如不希望存儲，請使用 --no_store_secrets 選項。

獲取 Vectra API Token（v2）

Vectra Detect API v2 使用基於 Token 的身份驗證。
	1.	登入 Vectra，進入「My Profile」並創建 API Token。
	2.	僅本地帳戶可生成 API Token。
	3.	建議創建單獨的 API 整合用戶，並分配精細的 RBAC 權限。

API Token 所需權限：
	•	讀取主機（Hosts）
	•	讀取帳戶（Accounts）
	•	讀取檢測項（Detections）
	•	讀取「管理 - 群組」
	•	標籤的讀/寫權限
	•	備註與其他用戶備註的讀/寫權限

獲取 Vectra API 客戶端 ID 和密鑰（v3）
	1.	登入 Detect 入口網站，進入「Manage > API Clients」，選擇「Add API Client」新增客戶端。
	2.	記錄客戶端 ID 和密鑰，這兩個信息將用於獲取 API Token。
	3.	建議為整合創建單獨角色，並分配精細的 RBAC 權限。

主機阻止

根據以下條件阻止內部主機的通訊：
	1.	BLOCK_HOST_TAG：當主機被標記此標籤時觸發阻止。
	2.	NO_BLOCK_HOST_GROUP_NAME：此群組中的成員不會被阻止。
	3.	BLOCK_HOST_GROUP_NAME：此群組中的成員將被阻止。
	4.	BLOCK_HOST_THREAT_CERTAINTY：威脅與確定性分數門檻。
	5.	BLOCK_HOST_URGENCY：僅對 V3 API，緊急性分數門檻。
	6.	BLOCK_HOST_DETECTION_TYPES：特定檢測類型觸發阻止。
	7.	BLOCK_HOST_DETECTION_TYPES_MIN_TC_SCORE：指定檢測類型的最低分數。

帳戶阻止

目前僅 external_call 模組支援帳戶阻止。
阻止條件類似於主機阻止，需配置 config.py 文件中的相關參數。

檢測項阻止

目標為阻止包含外部元件（如 IP 或域名）的檢測項。
主要應用於防火牆類第三方客戶端。
請謹慎使用，因為錯誤的阻止可能對網路造成嚴重影響。

配置第三方客戶端
	•	修改 config.py 文件以添加所需的第三方客戶端。
	•	可使用輔助腳本進行交互式配置：

python3 var_config_helper.py

選擇阻止類型

可設定執行主機、帳戶或檢測項的阻止操作，或同時執行：

# 主機阻止
hosts_to_block, hosts_to_unblock = var.get_hosts_to_block_unblock()
var.block_hosts(hosts_to_block)
var.unblock_hosts(hosts_to_unblock)

# 檢測項阻止
detections_to_block, detections_to_unblock = var.get_detections_to_block_unblock()
var.block_detections(detections_to_block)
var.unblock_detections(detections_to_unblock)

運行腳本
	1.	手動運行：

python3 vectra_automated_response.py

	2.	設定為服務模式（迴圈執行）：

python3 vectra_automated_response.py --loop

重點整理
	1.	靈活性：支援主機、帳戶與檢測項阻止，並整合多家安全系統。
	2.	安全性：使用 Keyring 存儲敏感信息，並提供精細的 RBAC 控制。
	3.	自動化：支援定時運行與持續監控，減少手動操作。
	4.	高擴展性：只需擴展抽象類，即可快速整合新廠商工具。
	5.	注意事項：謹慎設定檢測項阻止條件，以避免對網路運行造成影響。
