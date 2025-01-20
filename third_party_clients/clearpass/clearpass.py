import json
import logging
from requests import HTTPError
import requests

from third_party_clients.clearpass.clearpass_config import (
    CHECK_SSL,
    HOSTNAME,
)
from third_party_clients.third_party_interface import (
    ThirdPartyInterface,
    VectraAccount,
    VectraDetection,
    VectraHost,
    VectraStaticIP,
)
from common import _get_password


class Client(ThirdPartyInterface):
    """
    ClearPass 客戶端實現，用於與 ClearPass API 進行交互操作。
    """
    def __init__(self, **kwargs):
        self.name = "ClearPass Client"
        self.logger = logging.getLogger()
        self.url = f"https://{HOSTNAME}/api"
        self.verify = CHECK_SSL
        
        try:
            # 建立 OAuth 認證 URL
            url_oauth = f"{self.url}/oauth"
            params_oauth = {
                "grant_type": "password",
                "client_id": _get_password("Clearpass", "Client_ID", modify=kwargs.get("modify", False)),
                "client_secret": _get_password("Clearpass", "Client_Secret", modify=kwargs.get("modify", False)),
                "username": _get_password("Clearpass", "Username", modify=kwargs.get("modify", False)),
                "password": _get_password("Clearpass", "Password", modify=kwargs.get("modify", False)),
            }

            # 發送 POST 請求以獲取 OAuth Token
            post_oauth = requests.post(url=url_oauth, json=params_oauth, verify=self.verify)
            post_oauth.raise_for_status()
            
            # 獲取認證 Token
            self.bearer = {
                "Authorization": f"Bearer {post_oauth.json()['access_token']}"
            }
            self.logger.info("成功連線至 ClearPass，獲取 OAuth Token。")
        except HTTPError as http_err:
            self.logger.error(f"ClearPass OAuth 認證失敗: {http_err.response.text}")
            raise http_err
        except Exception as err:
            self.logger.error(f"ClearPass 連線發生未知錯誤: {str(err)}")
            raise err

        # 初始化父類
        ThirdPartyInterface.__init__(self)

    def block_host(self, host):
        """
        將指定的主機進行隔離。
        Args:
            host (VectraHost): 需要隔離的主機物件
        Returns:
            list: 成功隔離的 MAC 地址清單
        """
        mac_addresses = host.mac_addresses or self._get_macs(host.ip)

        if not mac_addresses:
            self.logger.warning("未提供 MAC 地址，且無法通過 IP 查找對應的 MAC 地址。")
            return []

        for mac_address in mac_addresses:
            self._patch_endpoint(mac_address, isolated=True)
            self._disconnect_session(mac_address)
        
        return mac_addresses

    def unblock_host(self, host):
        """
        解除主機隔離狀態。
        Args:
            host (VectraHost): 需要解除隔離的主機物件
        Returns:
            list: 成功解除隔離的 MAC 地址清單
        """
        mac_addresses = host.blocked_elements.get(self.name, [])

        for mac_address in mac_addresses:
            self._patch_endpoint(mac_address, isolated=False)
            self._disconnect_session(mac_address)
        
        return mac_addresses

    def _get_macs(self, ip):
        """
        根據 IP 查找對應的 MAC 地址。
        Args:
            ip (str): 主機的 IP 地址
        Returns:
            list: MAC 地址清單
        """
        mac_list = []
        try:
            sessions = requests.get(
                url=f"{self.url}/session?filter=%7B%22framedipaddress%22%3A%20%22{ip}%22%7D",
                headers=self.bearer,
                verify=self.verify,
            )
            sessions.raise_for_status()
            
            items = sessions.json().get("_embedded", {}).get("items", [])
            for session in items:
                mac_list.append(session.get("mac_address", "").replace("-", ":"))
            
            return list(set(mac_list))
        except Exception as e:
            self.logger.error(f"無法根據 IP 獲取 MAC 地址: {str(e)}")
            return mac_list

    def _patch_endpoint(self, mac_address, isolated=False):
        """
        更新指定 MAC 地址的隔離狀態。
        Args:
            mac_address (str): 主機的 MAC 地址
            isolated (bool): 是否啟用隔離
        """
        try:
            patch_endpoint_url = f"{self.url}/endpoint/mac-address/{mac_address}"
            params_patch_endpoint = {
                "mac_address": mac_address,
                "attributes": {"isolated": isolated},
            }
            r = requests.patch(
                url=patch_endpoint_url,
                headers=self.bearer,
                verify=self.verify,
                json=params_patch_endpoint,
            )
            r.raise_for_status()
            self.logger.info(f"成功更新 MAC 地址 {mac_address} 的隔離狀態為 {isolated}")
        except Exception as e:
            self.logger.error(f"更新 MAC 地址 {mac_address} 隔離狀態失敗: {str(e)}")

    def _disconnect_session(self, mac_address):
        """
        斷開指定 MAC 地址的會話。
        Args:
            mac_address (str): 主機的 MAC 地址
        """
        try:
            disconnect_url = f"{self.url}/session-action/disconnect/mac/{mac_address}?async=false"
            disconnect = requests.post(
                url=disconnect_url,
                headers=self.bearer,
                verify=self.verify,
            )
            disconnect.raise_for_status()
            self.logger.info(f"成功斷開 MAC 地址 {mac_address} 的會話")
        except Exception as e:
            self.logger.error(f"斷開 MAC 地址 {mac_address} 的會話失敗: {str(e)}")
