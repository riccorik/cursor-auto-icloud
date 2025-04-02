# Cursor Pro (iCloud) 自动化工具

⭐️ 在 GitHub 上给我们 Star — 这对我们是很大的鼓励！
[English README](README-en.md)

## 目录

- [准备工作](#准备工作)
- [下载](#下载)
- [设置](#设置)
- [运行工具](#运行工具)
- [免责声明](#免责声明)
- [致谢](#致谢)
- [贡献](#贡献)
- [许可证](#许可证)

## 准备工作

在使用此工具之前，您应该准备以下内容：

- 一个拥有 **iCloud Plus** 的苹果账号

## 下载

1. 从 GitHub Releases 下载最新版本
2. 根据你的系统选择对应的版本：

> Windows：直接下载 CursorKeepAlive.exe
> Mac（Intel）：选择 x64 版本
> Mac（M系列）：选择 ARM64(aarch64) 版本

### Mac 用户额外步骤

> 打开终端，进入应用所在目录
> 执行以下命令使文件可执行：
> ```chmod +x ./CursorKeepAlive```

按照下文设置，然后运行

## 设置

### 设置环境变量

> Mac 用户：如果您无法重命名文件，可以使用 `touch .env` 在同一目录中创建该文件。

1. 下载 `.env.example` 文件并将其重命名为 `.env`
2. 填写 `.env` 文件

```env
ICLOUD_USER=您的苹果ID（!!! 不包括 @icloud.com）
ICLOUD_APP_PASSWORD=您的苹果ID应用专用密码（解释如下）
ICLOUD_COOKIES=您的iCloud cookies（解释如下）
```

### 获取 iCloud cookie 字符串

1. 下载 [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) Chrome 扩展
2. 在浏览器中到 [iCloud 设置](https://www.icloud.com/settings/) 并登录
3. 点击 Cookie-Editor 扩展并以 `Header String` 格式导出 cookies
4. 将导出的 cookies 粘贴到名为 `.env` 的文件中作为 `ICLOUD_COOKIES`

### 获取 Apple ID 应用专用密码

1. 在 [account.apple.com](https://account.apple.com) 登录您的 Apple 账户
2. 在登录和安全部分，选择应用专用密码
3. 选择生成应用专用密码，然后按照屏幕上的步骤操作
4. 复制生成的密码并将其粘贴到名为 `.env` 的文件中作为 `ICLOUD_APP_PASSWORD`

## 运行工具

### Windows 用户

双击可执行文件运行工具。

### Mac 用户

1. 打开终端
2. 导航到可执行文件所在的目录
3. `./CursorKeepAlive`

### 请按 `4` 开始自动化流程

## 免责声明

本项目仅为教育目的而创建。作者不对以下情况承担任何责任或义务：

- 对代码或相关材料的任何滥用
- 使用本项目产生的任何损害或法律后果
- 所提供内容的准确性、完整性或实用性

使用本项目，即表示您同意风险自负。本项目不适用于生产环境，且不提供任何保证或担保。
如果您有任何法律或道德顾虑，请不要使用此存储库。

## 致谢

没有这些出色项目的帮助，本项目无法完成：

- [cursor-auto-free](https://github.com/chengazhen/cursor-auto-free)
- [go-cursor-help](https://github.com/yuaotian/go-cursor-help)

## 贡献

如果您想为本项目做出贡献，请随时提交拉取请求。

## 许可证

本产品根据专有许可证分发。您可以在以下链接查看完整的许可协议：[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)。
