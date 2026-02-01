"""
THSTrader 配置文件
新版同花顺（11.46.04）UI 元素定位配置
设备分辨率: 720x1280, 240dpi
"""

# UI 元素 Resource IDs
UI_ELEMENTS = {
    # 导航相关
    "tab_moni": "com.hexin.plat.android:id/tab_mn",  # 模拟炒股标签
    "title_bar_img": "com.hexin.plat.android:id/title_bar_img",  # 返回按钮

    # 功能按钮
    "menu_buy_image": "com.hexin.plat.android:id/menu_buy_image",  # 买入按钮
    "menu_sale_image": "com.hexin.plat.android:id/menu_sale_image",  # 卖出按钮
    "menu_holdings_image": "com.hexin.plat.android:id/menu_holdings_image",  # 持仓按钮
    "menu_withdrawal_image": "com.hexin.plat.android:id/menu_withdrawal_image",  # 撤单按钮

    # 输入框
    "content_stock": "com.hexin.plat.android:id/content_stock",  # 股票代码输入框
    "content_buy_stock": "com.hexin.plat.android:id/content_buy_stock",  # 买入股票代码输入框
    "stockprice": "com.hexin.plat.android:id/stockprice",  # 价格输入框
    "stockvolume": "com.hexin.plat.android:id/stockvolume",  # 数量输入框

    # 搜索结果
    "recyclerView": "com.hexin.plat.android:id/recyclerView",  # 搜索结果列表
    "stockname_tv": "com.hexin.plat.android:id/stockname_tv",  # 股票名称

    # 确认对话框
    "ok_btn": "com.hexin.plat.android:id/ok_btn",  # 确定按钮
    "cancel_btn": "com.hexin.plat.android:id/cancel_btn",  # 取消按钮
    "close_btn": "com.hexin.plat.android:id/close_btn",  # 关闭按钮
    "stock_name_value": "com.hexin.plat.android:id/stock_name_value",  # 股票名称值
    "stock_code_value": "com.hexin.plat.android:id/stock_code_value",  # 股票代码值
    "number_value": "com.hexin.plat.android:id/number_value",  # 数量值
    "price_value": "com.hexin.plat.android:id/price_value",  # 价格值

    # 账户信息（新版UI）
    "capital_cell_title": "com.hexin.plat.android:id/capital_cell_title",  # 资产标题
    "capital_cell_value": "com.hexin.plat.android:id/capital_cell_value",  # 资产值

    # 持仓列表
    "recyclerview_id": "com.hexin.plat.android:id/recyclerview_id",  # 持仓列表

    # 撤单列表
    "chedan_recycler_view": "com.hexin.plat.android:id/chedan_recycler_view",  # 撤单列表
    "option_chedan": "com.hexin.plat.android:id/option_chedan",  # 撤单选项

    # 结果展示
    "content_scroll": "com.hexin.plat.android:id/content_scroll",  # 结果滚动区域

    # 自选股相关
    "tab_optional": "com.hexin.plat.android:id/tab_optional",  # 自选标签
    "add_optional": "com.hexin.plat.android:id/add_optional",  # 添加自选按钮
    "optional_list": "com.hexin.plat.android:id/optional_list",  # 自选列表
    "stock_item": "com.hexin.plat.android:id/stock_item",  # 股票项
    "stock_code": "com.hexin.plat.android:id/stock_code",  # 股票代码
}

# 坐标位置（720x1280分辨率）
COORDINATES = {
    "trading_tab": (420, 1210),  # 底部"交易"标签位置
    "buy_button": (72, 610),  # 买入按钮位置（左侧圆形按钮）
    "sell_button": (216, 610),  # 卖出按钮位置
    "holdings_button": (360, 610),  # 持仓按钮位置
    "withdrawal_button": (504, 610),  # 撤单按钮位置
}

# XPath 路径
XPATHS = {
    "trading_tab": '//*[@content-desc="交易"]/android.widget.ImageView[1]',
    "transaction_layout": '//*[@resource-id="com.hexin.plat.android:id/transaction_layout"]/android.widget.LinearLayout[1]',
    "stock_search_result": '//*[@resource-id="com.hexin.plat.android:id/recyclerView"]/android.widget.RelativeLayout[1]',
}

# 应用包名
APP_PACKAGE = "com.hexin.plat.android"
APP_ACTIVITY = "com.hexin.plat.android.LogoEmptyActivity"

# OCR 裁剪区域（用于持仓和撤单列表的信息提取）
OCR_CROP_AREAS = {
    "holding": {
        "stock_name": (11, 11, 165, 55),
        "stock_count": (419, 11, 548, 55),
        "stock_available": (419, 60, 548, 102),
    },
    "withdrawal": {
        "stock_name": (11, 11, 165, 55),
        "stock_price": (219, 11, 390, 55),
        "stock_count": (419, 11, 548, 55),
        "type": (589, 11, 704, 55),
    }
}

# 默认参数
DEFAULT_WAIT = 2  # 默认等待时间（秒）
MAX_RETRY = 3  # 最大重试次数
MAX_HOLDINGS = 1000  # 最大持仓数量
INPUT_CLEAR_COUNT = 20  # 输入框清空按键次数
