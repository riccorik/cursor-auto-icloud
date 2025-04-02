from datetime import datetime
import logging
import time
import re
from config import Config
import requests
import email
import imaplib
import poplib
from email.parser import Parser
import json
import socket


class EmailVerificationHandler:
    def __init__(self,account):
        self.session = requests.Session()
        self.account = account

    def get_verification_code(self, max_retries=5, retry_interval=60):
        """
        获取验证码，带有重试机制。

        Args:
            max_retries: 最大重试次数。
            retry_interval: 重试间隔时间（秒）。

        Returns:
            验证码 (字符串或 None)。
        """

        for attempt in range(max_retries):
            try:
                logging.info(f"尝试获取验证码 (第 {attempt + 1}/{max_retries} 次)...")

                verify_code = self._get_latest_mail_code()
                if attempt < max_retries - 1 and not verify_code:  # 除了最后一次尝试，都等待
                    logging.warning(f"未获取到验证码，{retry_interval} 秒后重试...")
                    time.sleep(retry_interval)
                else: 
                    return verify_code

            except Exception as e:
                logging.error(f"获取验证码失败: {e}")  # 记录更一般的异常
                if attempt < max_retries - 1:
                    logging.error(f"发生错误，{retry_interval} 秒后重试...")
                    time.sleep(retry_interval)
                else:
                    raise Exception(f"获取验证码失败且已达最大重试次数: {e}") from e

        raise Exception(f"经过 {max_retries} 次尝试后仍未获取到验证码。")

    # 手动输入验证码
    def _get_latest_mail_code(self):
        """
        获取最新邮件中的验证码:
        1. iCloud IMAP
        
        Returns:
            str or tuple: 验证码或 (验证码, 邮件ID) 元组
        """
        # 首先尝试 iCloud IMAP
        icloud_imap = Config().get_icloud_imap()
        if icloud_imap:
            logging.info("使用 iCloud IMAP 获取邮件...")
            verify_code = self._get_mail_code_by_icloud_imap(icloud_imap)
            if verify_code:
                return verify_code
        
        return None
    

    def _get_mail_code_by_icloud_imap(self, icloud_config, retry=0):
        """使用 iCloud IMAP 获取邮件验证码
        
        Args:
            icloud_config: iCloud IMAP 配置信息
            retry: 重试次数
            
        Returns:
            str or None: 验证码
        """
        if retry > 0:
            time.sleep(3)
        if retry >= 20:
            raise Exception("获取验证码超时")
        
        try:
            # 连接到 iCloud IMAP 服务器
            mail = imaplib.IMAP4_SSL(icloud_config['imap_server'], icloud_config['imap_port'])
            
            # 用户名可能需要包含完整邮箱地址
            username = icloud_config['imap_user']
            if '@' not in username and '@icloud.com' not in username:
                # 尝试检查是否已经是完整的邮箱地址
                if not username.endswith(('@icloud.com', '@me.com', '@mac.com')):
                    # 默认添加 @icloud.com
                    logging.info(f"使用完整邮箱地址 {username}@icloud.com 登录 iCloud IMAP")
                    username = f"{username}@icloud.com"
            
            mail.login(username, icloud_config['imap_pass'])
            mail.select(icloud_config['imap_dir'] or 'INBOX')
            
            # 获取最近的邮件
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                logging.error(f"获取 iCloud 邮件列表失败: {status}")
                return None
            
            mail_ids = messages[0].split()
            print(mail_ids)
            if not mail_ids:
                # 没有获取到邮件
                logging.info("iCloud 邮箱中没有找到邮件")
                return self._get_mail_code_by_icloud_imap(icloud_config, retry=retry + 1)
            
            # 检查最新的10封邮件
            for i in range(min(10, len(mail_ids))):
                mail_id = mail_ids[len(mail_ids) - 1 - i]  
                try:
                    status, msg_data = mail.fetch(mail_id, '(BODY[])')
                except (EOFError, ConnectionError, socket.error) as e:
                    logging.error(f"iCloud IMAP fetch failed: {e}")
                    mail.logout()
                    return None
                if status != 'OK':
                    logging.error(f"iCloud IMAP fetch failed with status: {status}")
                    continue
                raw_email = msg_data[0][1]

                email_message = email.message_from_bytes(raw_email)
                sender = email_message.get('from', '')
                recipient = email_message.get('to', '')

                if self.account not in recipient:
                    continue
                if 'no-reply_at_cursor_sh' not in sender:
                    continue
                

                body = self._extract_imap_body(email_message)
                if body:
                    # 查找 6 位数验证码
                    code_match = re.search(r"(?<![a-zA-Z@.])\b\d{6}\b", body)
                    if code_match:
                        code = code_match.group()
                        logging.info(f"从 iCloud 邮件中找到验证码: {code}")
                        
                        mail.store(mail_id, '+FLAGS', '\\Deleted')
                        mail.expunge()
                        
                        mail.logout()
                        return code
            
            logging.info("在 iCloud 邮件中未找到验证码")
            mail.logout()
            return None
            
        except Exception as e:
            logging.error(f"iCloud IMAP 操作失败: {e}")
            return None

    def _extract_imap_body(self, email_message):
        # 提取邮件正文
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    charset = part.get_content_charset() or 'utf-8'
                    try:
                        body = part.get_payload(decode=True).decode(charset, errors='ignore')
                        return body
                    except Exception as e:
                        logging.error(f"解码邮件正文失败: {e}")
        else:
            content_type = email_message.get_content_type()
            if content_type == "text/plain":
                charset = email_message.get_content_charset() or 'utf-8'
                try:
                    body = email_message.get_payload(decode=True).decode(charset, errors='ignore')
                    return body
                except Exception as e:
                    logging.error(f"解码邮件正文失败: {e}")
        return ""

if __name__ == "__main__":
    email_handler = EmailVerificationHandler()
    code = email_handler.get_verification_code()
    print(code)
