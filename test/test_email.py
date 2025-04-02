import os
from dotenv import load_dotenv
from get_email_code import EmailVerificationHandler
import logging
import json


def test_icloud_imap():
    """测试 iCloud IMAP 方式"""
    handler = EmailVerificationHandler("test@example.com")
    print("\n=== 测试 iCloud IMAP 模式 ===")
    icloud_user = os.getenv('ICLOUD_USER', '')
    print(f"iCloud 用户: {icloud_user}")
    
    code = handler.get_verification_code()
    if code:
        print(f"成功获取验证码: {code}")
    else:
        print("未能获取验证码")

def print_config():
    """打印当前配置"""
    print("\n当前环境变量配置:")
    print(f"TEMP_MAIL: {os.getenv('TEMP_MAIL')}")
    
    # 检查是否配置了 iCloud IMAP
    icloud_user = os.getenv('ICLOUD_USER')
    icloud_pass = os.getenv('ICLOUD_APP_PASSWORD')
    
    print(f"ICLOUD_USER: {icloud_user}")
    print("ICLOUD_APP_PASSWORD: [已配置]")
    print(f"ICLOUD_FOLDER: {os.getenv('ICLOUD_FOLDER', 'INBOX')}")

    

def main():
    # 加载环境变量
    load_dotenv()
    
    # 打印初始配置
    print_config()
    
    try:
        # 首先检查是否配置了 iCloud IMAP
        icloud_user = os.getenv('ICLOUD_USER')
        icloud_pass = os.getenv('ICLOUD_APP_PASSWORD')
        
        if icloud_user and icloud_pass:
            text = test_icloud_imap()
            print("text", text)
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main() 