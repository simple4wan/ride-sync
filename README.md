# ride-sync
码表骑行轨迹多平台同步，支持 IGPSPORT 迹驰 / 行者 / Magene 迈金 顽鹿

**运行环境**
`python3`

**使用方法**
1. 克隆项目到本地
2. 执行`pip install -r requirements.txt`安装依赖
3. 复制`.env.example`为`.env`并配置好 导入平台 导出平台 以及对应平台的账号密码
- 导出平台`EXPORT_PLATFORM`支持`igpsport`, `onelap`
- 导入平台`IMPORT_PLATFORM`支持`imxingzhe`
4. 执行`python3 main.py` 如果没有异常提示表明正在同步
5. 当同步出现异常脚本会自动退出，所以需要第三方服务守护进程 linux 推荐 supervisor

**TODO**
- [ ] 支持更多平台