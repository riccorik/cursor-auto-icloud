import asyncio
import aiohttp
import ssl
import certifi
import os
import sys

# Add parent directory to path to import logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import logging


class HideMyEmail:
    base_url_v1 = "https://p68-maildomainws.icloud.com/v1/hme"
    base_url_v2 = "https://p68-maildomainws.icloud.com/v2/hme"
    params = {
        "clientBuildNumber": "2413Project28",
        "clientMasteringNumber": "2413B20",
        "clientId": "",
        "dsid": "", # Directory Services Identifier (DSID) is a method of identifying AppleID accounts
    }

    def __init__(self, label: str = "Cursor-Auto-iCloud", cookies: str = ""):
        """Initializes the HideMyEmail class.

        Args:
            label (str)     Label that will be set for all emails generated, defaults to `Cursor-Auto-iCloud`
            cookies (str)   Cookie string to be used with requests. Required for authorization.
        """
        self.label = label

        # Cookie string to be used with requests. Required for authorization.
        self.cookies = cookies

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl_context=ssl.create_default_context(cafile=certifi.where())) 
        self.s = aiohttp.ClientSession(
            headers={
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Content-Type": "text/plain",
                "Accept": "*/*",
                "Sec-GPC": "1",
                "Origin": "https://www.icloud.com",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.icloud.com/",
                "Accept-Language": "en-US,en-GB;q=0.9,en;q=0.8,cs;q=0.7",
                "Cookie": self.__cookies.strip(),
            },
            timeout=aiohttp.ClientTimeout(total=10),
            connector=connector,
        )

        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self.s.close()

    @property
    def cookies(self) -> str:
        return self.__cookies

    @cookies.setter
    def cookies(self, cookies: str):
        # remove new lines/whitespace for security reasons
        self.__cookies = cookies.strip()

    async def generate_email(self) -> dict:
        """Generates an email"""
        try:
            logging.debug("正在生成 iCloud 隐藏邮箱...")
            async with self.s.post(
                f"{self.base_url_v1}/generate", params=self.params, json={"langCode": "en-us"}
            ) as resp:
                res = await resp.json()
                return res
        except asyncio.TimeoutError:
            logging.error("生成邮箱超时")
            return {"error": 1, "reason": "Request timed out"}
        except Exception as e:
            logging.error(f"生成邮箱失败: {str(e)}")
            return {"error": 1, "reason": str(e)}

    async def reserve_email(self, email: str) -> dict:
        """Reserves an email and registers it for forwarding"""
        try:
            logging.debug(f"正在保留邮箱 {email}...")
            payload = {
                "hme": email,
                "label": self.label,
                "note": "Cursor-Auto-iCloud",
            }
            async with self.s.post(
                f"{self.base_url_v1}/reserve", params=self.params, json=payload
            ) as resp:
                res = await resp.json()
            return res
        except asyncio.TimeoutError:
            logging.error("保留邮箱超时")
            return {"error": 1, "reason": "Request timed out"}
        except Exception as e:
            logging.error(f"保留邮箱失败: {str(e)}")
            return {"error": 1, "reason": str(e)}

    async def list_email(self) -> dict:
        """List all HME"""
        logging.info("正在获取邮箱列表...")
        try:
            async with self.s.get(f"{self.base_url_v2}/list", params=self.params) as resp:
                res = await resp.json()
                return res
        except asyncio.TimeoutError:
            logging.error("获取邮箱列表超时")
            return {"error": 1, "reason": "Request timed out"}
        except Exception as e:
            logging.error(f"获取邮箱列表失败: {str(e)}")
            return {"error": 1, "reason": str(e)}


    async def delete_email(self, email: str) -> dict:
        """Deletes an email"""
        logging.info(f"正在删除邮箱 {email}...")
        try: 
            async with self.s.post(f"{self.base_url_v1}/delete", params=self.params, json={"hme": email}) as resp:
                res = await resp.json()
                return res
        except asyncio.TimeoutError:
            logging.error("删除邮箱超时")
            return {"error": 1, "reason": "Request timed out"}
        except Exception as e:
            logging.error(f"删除邮箱失败: {str(e)}")
            return {"error": 1, "reason": str(e)}
        