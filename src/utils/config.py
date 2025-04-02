from dotenv import load_dotenv
import os
import sys
from src.utils.logger import logging
import json


class Config:
    def __init__(self):
        # 获取应用程序的根目录路径
        if getattr(sys, "frozen", False):
            # 如果是打包后的可执行文件
            application_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            # Look for .env in the project root, not in src/utils
            application_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # 指定 .env 文件的路径
        dotenv_path = os.path.join(application_path, ".env")

        if not os.path.exists(dotenv_path):
            raise FileNotFoundError(f"文件 {dotenv_path} 不存在")

        # 加载 .env 文件
        load_dotenv(dotenv_path)

        self.icloud_user = os.getenv('ICLOUD_USER', '').strip()
        if '@icloud.com' in self.icloud_user:
            self.icloud_user = self.icloud_user.replace('@icloud.com', '')
        self.icloud_pass = os.getenv('ICLOUD_APP_PASSWORD', '').strip()

        # 检查配置
        self.check_config()


    def get_icloud_imap(self):
        """获取 iCloud IMAP 配置
        
        Returns:
            dict or False: iCloud IMAP 配置信息，若未配置则返回 False
        """
        # 检查必要的 iCloud IMAP 配置是否存在
        icloud_user = os.getenv('ICLOUD_USER', '').strip()

        if '@icloud.com' in icloud_user:
            icloud_user = icloud_user.replace('@icloud.com', '')

        icloud_pass = os.getenv('ICLOUD_APP_PASSWORD', '').strip()
        
        if not icloud_user or not icloud_pass:
            return False
        
        return {
            "imap_server": "imap.mail.me.com",  # iCloud Mail 固定服务器
            "imap_port": 993,                    # iCloud Mail 固定端口
            "imap_user": icloud_user,            # 用户名通常是邮箱前缀
            "imap_pass": icloud_pass,            # 应用专用密码
            "imap_dir": os.getenv('ICLOUD_FOLDER', 'INBOX').strip(),
        }

    def check_config(self):
        """检查配置项是否有效

        检查规则：
        1. Validate if icloud user and pass is not null
        """

        required_configs = {
            "icloud_user": "iCloud 邮箱",
            "icloud_pass": "iCloud 应用专用密码",
        }

        # 检查基础配置
        for key, name in required_configs.items():
            if not self.check_is_valid(getattr(self, key)):
                raise ValueError(f"{name}未配置，请在 .env 文件中设置 {key.upper()}")



    def check_is_valid(self, value):
        """检查配置项是否有效

        Args:
            value: 配置项的值

        Returns:
            bool: 配置项是否有效
        """
        return isinstance(value, str) and len(str(value).strip()) > 0

    def print_config(self):
        logging.info(f"iCloud 邮箱: {self.icloud_user}@icloud.com")
        logging.info(f"iCloud 应用专用密码: {self.icloud_pass}")


# 使用示例
if __name__ == "__main__":
    try:
        config = Config()
        print("环境变量加载成功！")
        config.print_config()
    except ValueError as e:
        print(f"错误: {e}")
