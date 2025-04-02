#!/usr/bin/env python3
"""
iCloud Email Generator
This module generates Hide My Email addresses for iCloud accounts.
"""

import os
import sys
import asyncio
from typing import List, Optional

# Add parent directory to path to import logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import logging
from utils.config import Config
from icloud.hidemyemail import HideMyEmail

async def _generate_single_email(cookies: str, label: str = "Cursor-Auto-iCloud") -> Optional[str]:
    """
    Generate a single iCloud Hide My Email address
    
    Args:
        cookies: iCloud cookies for authentication
        label: Label for the email
        
    Returns:
        str: The generated email address or None if failed
    """
    try:
        async with HideMyEmail(label, cookies) as hme:
            # Generate email
            gen_result = await hme.generate_email()
            
            # Debug print the result
            logging.debug(f"API Response: {gen_result}")
            
            if not gen_result.get("success", False):
                logging.error(f"生成邮箱失败: {gen_result.get('reason', '未知错误')}")
                return None
                
            # Correctly access the email address from the nested structure
            email = gen_result.get("result", {}).get("hme")
            if not email:
                logging.error("生成邮箱失败: 无法获取邮箱地址")
                return None
                
            # Reserve email
            reserve_result = await hme.reserve_email(email)
            if not reserve_result.get("success", False):
                logging.error(f"保留邮箱失败: {reserve_result.get('reason', '未知错误')}")
                return None
                
            logging.info(f"邮箱 {email} 生成成功")
            return email
    except Exception as e:
        logging.error(f"生成邮箱过程中发生错误: {str(e)}")
        return None

async def _generate_multiple_emails(count: int, cookies: str, label: str = "Cursor-Auto-iCloud") -> List[str]:
    """
    Generate multiple iCloud Hide My Email addresses
    
    Args:
        count: Number of emails to generate
        cookies: iCloud cookies for authentication
        label: Label for the emails
        
    Returns:
        List[str]: List of generated email addresses
    """
    tasks = []
    for _ in range(count):
        tasks.append(_generate_single_email(cookies, label))
    
    results = await asyncio.gather(*tasks)
    # Filter out None values
    return [email for email in results if email]

def generateIcloudEmail(count: int = 1, save_to_file: bool = True) -> List[str]:
    """
    Generate a specified number of iCloud Hide My Email addresses
    
    Args:
        count: Number of emails to generate
        save_to_file: Whether to save emails to data/emails.txt
        
    Returns:
        List[str]: List of generated email addresses
    """
    # Get iCloud cookies from config
    try:
        # Get cookies from .env file
        cookies = os.getenv('ICLOUD_COOKIES', '').strip()
        if not cookies:
            logging.error("iCloud Cookies 未配置，请在 .env 文件中设置 ICLOUD_COOKIES")
            return []
            
        # Generate emails
        logging.info(f"开始生成 {count} 个 iCloud 隐藏邮箱...")
        emails = asyncio.run(_generate_multiple_emails(count, cookies))
        
        if not emails:
            logging.error("未能生成任何邮箱地址")
            return []
            
        logging.info(f"成功生成 {len(emails)} 个邮箱地址")
        
        # Save to file if requested
        if save_to_file:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                
            emails_file = os.path.join(data_dir, "emails.txt")
            
            # If file exists, read existing emails
            existing_emails = []
            if os.path.exists(emails_file):
                with open(emails_file, "r") as f:
                    existing_emails = [line.strip() for line in f.readlines() if line.strip()]
            
            # Add new emails
            all_emails = existing_emails + emails
            
            # Write back to file
            with open(emails_file, "w") as f:
                f.write("\n".join(all_emails))
                
            logging.info(f"邮箱地址已保存到 {emails_file}")
                
        return emails
        
    except Exception as e:
        logging.error(f"生成邮箱过程中发生错误: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
        return []

if __name__ == "__main__":
    # If run directly, generate 5 emails
    count = 5
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            logging.error(f"无效的数量参数: {sys.argv[1]}")
            sys.exit(1)
    
    emails = generateIcloudEmail(count)
    if emails:
        print(f"成功生成 {len(emails)} 个邮箱地址:")
        for email in emails:
            print(email)
    else:
        print("未生成任何邮箱地址")
