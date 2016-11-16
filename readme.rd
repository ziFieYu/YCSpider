spider

core # 核心
    console # 控制
    downloader # 下载器
    parser # 解析器
    save # 数据存储


# ############################################
# spider start
# 初始化10个线程/进程 读取URL队列 加入 任务列表中
# 初始化10个线程/进程 downloader 开始下载URL列表
# 初始化10个线程/进程 parser 开始解析HTML
# 初始化10个线程/进程 save 保存数据