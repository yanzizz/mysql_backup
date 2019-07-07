**Mysql/MariaDB数据备份脚本**  
- 使用python2编写。
- 依赖xtrabackup工具。
- 仅在linux下测试通过。
- 备份策略为周日全备一次，依次每天做增备，7天为一周期。
- 可备份到其它机器，使用rsync工具。
- 其它说明见配制文件。
- 安装说明见INSTALL文件。
