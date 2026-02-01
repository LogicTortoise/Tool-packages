"""
THSTrader 核心类
适配新版同花顺（11.46.04）
"""
import time
import uiautomator2 as u2
from PIL import Image
from .config import UI_ELEMENTS, COORDINATES, XPATHS, APP_PACKAGE, DEFAULT_WAIT, MAX_HOLDINGS, INPUT_CLEAR_COUNT

try:
    import easyocr
    HAS_OCR = True
except ImportError:
    HAS_OCR = False
    print("警告: easyocr 未安装，OCR 功能将不可用")


class THSTrader:
    """同花顺模拟炒股自动交易类"""

    def __init__(self, serial="127.0.0.1:5565"):
        """
        初始化 THSTrader

        Args:
            serial: 设备序列号，默认 127.0.0.1:5565
        """
        self.d = u2.connect(serial)
        self.serial = serial

        # 初始化 OCR（如果可用）
        if HAS_OCR:
            self.reader = easyocr.Reader(['ch_sim', 'en'])
        else:
            self.reader = None

        print(f"✓ 已连接到设备: {serial}")

    def get_balance(self):
        """
        获取账户余额

        Returns:
            dict: {'总资产': float, '可用': float, '浮动盈亏': float, '总市值': float}
        """
        print("\n获取账户余额...")
        self._back_to_moni_page()

        # 点击持仓按钮
        if self.d(resourceId=UI_ELEMENTS["menu_holdings_image"]).exists:
            self.d(resourceId=UI_ELEMENTS["menu_holdings_image"]).click()
            time.sleep(DEFAULT_WAIT)
        else:
            # 使用坐标点击
            self.d.click(*COORDINATES["holdings_button"])
            time.sleep(DEFAULT_WAIT)

        # 向下滑动查看资产信息
        self.d.swipe(340, 600, 340, 1000, duration=0.3)
        time.sleep(1)

        # 获取资产信息（新版UI）
        balance = {}
        if self.d(resourceId=UI_ELEMENTS["capital_cell_value"]).exists:
            titles = []
            values = []

            for elem in self.d(resourceId=UI_ELEMENTS["capital_cell_title"]):
                try:
                    titles.append(elem.get_text())
                except:
                    pass

            for elem in self.d(resourceId=UI_ELEMENTS["capital_cell_value"]):
                try:
                    values.append(elem.get_text())
                except:
                    pass

            for i in range(min(len(titles), len(values))):
                balance[titles[i]] = values[i]

        # 返回
        self.d.press("back")
        time.sleep(1)

        print(f"✓ 获取成功: {balance}")
        return balance

    def get_position(self):
        """
        获取持仓列表

        Returns:
            list: [{'股票名称': str, '股票余额': int, '可用余额': int}, ...]
        """
        if not self.reader:
            print("✗ OCR 未初始化，无法获取持仓")
            return []

        print("\n获取持仓列表...")
        self._back_to_moni_page()

        # 点击持仓按钮
        if self.d(resourceId=UI_ELEMENTS["menu_holdings_image"]).exists:
            self.d(resourceId=UI_ELEMENTS["menu_holdings_image"]).click()
        else:
            self.d.click(*COORDINATES["holdings_button"])
        time.sleep(DEFAULT_WAIT)

        # 滚动并截取所有持仓
        i = 0
        first = True
        while True:
            if i > MAX_HOLDINGS:
                break
            try:
                self.d.xpath(f'//*[@resource-id="{UI_ELEMENTS["recyclerview_id"]}"]/android.widget.RelativeLayout[{i+1}]').screenshot().save(f"tmp{i}.png")
                i += 1
                self.d.swipe(340, 1000, 340, 890)
            except:
                if first:
                    self.d.swipe(340, 1000, 340, 600)
                    first = False
                else:
                    break

        count = i
        holdings = []
        for i in range(count):
            holdings.append(self._ocr_parse_holding(f"tmp{i}.png"))

        # 返回
        self.d.press("back")
        time.sleep(1)

        print(f"✓ 获取成功，共 {len(holdings)} 只股票")
        return holdings

    def buy(self, stock_code, amount, price):
        """
        买入股票

        Args:
            stock_code: 股票代码，如 "002415"
            amount: 买入数量（股）
            price: 买入价格

        Returns:
            dict: {'success': bool, 'msg': str, 'stock_name': str, 'amount': int, 'price': float}
        """
        return self._trade_action(stock_code, amount, price, "buy")

    def sell(self, stock_code, amount, price):
        """
        卖出股票

        Args:
            stock_code: 股票代码，如 "002415"
            amount: 卖出数量（股）
            price: 卖出价格

        Returns:
            dict: {'success': bool, 'msg': str, 'stock_name': str, 'amount': int, 'price': float}
        """
        return self._trade_action(stock_code, amount, price, "sell")

    def get_avail_withdrawals(self):
        """
        获取可撤单列表

        Returns:
            list: [{'股票名称': str, '委托价格': float, '委托数量': int, '委托类型': str}, ...]
        """
        if not self.reader:
            print("✗ OCR 未初始化，无法获取撤单列表")
            return []

        print("\n获取可撤单列表...")
        self._back_to_moni_page()

        # 点击撤单按钮
        if self.d(resourceId=UI_ELEMENTS["menu_withdrawal_image"]).exists:
            self.d(resourceId=UI_ELEMENTS["menu_withdrawal_image"]).click()
        else:
            self.d.click(*COORDINATES["withdrawal_button"])
        time.sleep(DEFAULT_WAIT)

        # 滚动并截取所有撤单
        i = 0
        first = True
        while True:
            if i > MAX_HOLDINGS:
                break
            try:
                self.d.xpath(f'//*[@resource-id="{UI_ELEMENTS["chedan_recycler_view"]}"]/android.widget.LinearLayout[{i+1}]').screenshot().save(f"tmp{i}.png")
                i += 1
                self.d.swipe(340, 1000, 340, 890)
            except:
                if first:
                    self.d.swipe(340, 1000, 340, 600)
                    first = False
                else:
                    break

        count = i
        withdrawals = []
        for i in range(count):
            withdrawals.append(self._ocr_parse_withdrawal(f"tmp{i}.png"))

        # 返回
        self.d.press("back")
        time.sleep(1)

        print(f"✓ 获取成功，共 {len(withdrawals)} 条委托")
        return withdrawals

    def withdraw(self, stock_name, trade_type, amount, price):
        """
        撤单

        Args:
            stock_name: 股票名称，如 "海康威视"
            trade_type: 委托类型，"买入" 或 "卖出"
            amount: 委托数量
            price: 委托价格

        Returns:
            dict: {'success': bool, 'msg': str}
        """
        if not self.reader:
            return {'success': False, 'msg': 'OCR 未初始化'}

        print(f"\n撤单: {stock_name} {trade_type} {amount}股 @{price}")
        self._back_to_moni_page()

        # 点击撤单按钮
        if self.d(resourceId=UI_ELEMENTS["menu_withdrawal_image"]).exists:
            self.d(resourceId=UI_ELEMENTS["menu_withdrawal_image"]).click()
        else:
            self.d.click(*COORDINATES["withdrawal_button"])
        time.sleep(DEFAULT_WAIT)

        # 查找匹配的委托
        success = False
        i = 0
        first = True
        while True:
            if i > MAX_HOLDINGS:
                break
            try:
                self.d.xpath(f'//*[@resource-id="{UI_ELEMENTS["chedan_recycler_view"]}"]/android.widget.LinearLayout[{i+1}]').screenshot().save(f"tmp{i}.png")
                info = self._ocr_parse_withdrawal(f"tmp{i}.png")

                if (stock_name == info["股票名称"] and
                    int(amount) == int(info["委托数量"]) and
                    abs(float(price) - float(info["委托价格"])) < 0.01 and
                    trade_type == info["委托类型"]):
                    # 找到匹配的委托，点击
                    self.d.xpath(f'//*[@resource-id="{UI_ELEMENTS["chedan_recycler_view"]}"]/android.widget.LinearLayout[{i+1}]').click()
                    time.sleep(1)
                    self.d(resourceId=UI_ELEMENTS["option_chedan"]).click()
                    time.sleep(1)
                    success = True
                    print(f"✓ 撤单成功")
                    break

                i += 1
                self.d.swipe(340, 1000, 340, 890)
            except:
                if first:
                    self.d.swipe(340, 1000, 340, 600)
                    first = False
                else:
                    break

        # 返回
        self.d.press("back")
        time.sleep(1)

        if not success:
            print(f"✗ 未找到匹配的委托")

        return {'success': success, 'msg': '撤单成功' if success else '未找到匹配的委托'}

    # ==================== 私有方法 ====================

    def _back_to_moni_page(self):
        """返回到模拟炒股主页"""
        # 关闭可能的对话框
        self._close_dialogs()

        # 启动应用
        self.d.app_start(APP_PACKAGE)
        time.sleep(2)
        self._close_dialogs()

        # 点击底部"交易"标签
        if self.d(text="交易").exists:
            self.d(text="交易").click()
        else:
            self.d.click(*COORDINATES["trading_tab"])
        time.sleep(DEFAULT_WAIT)
        self._close_dialogs()

        # 点击"模拟炒股"标签
        if self.d(resourceId=UI_ELEMENTS["tab_moni"]).exists:
            self.d(resourceId=UI_ELEMENTS["tab_moni"]).click()
            time.sleep(2)
            self._close_dialogs()

    def _close_dialogs(self):
        """关闭可能的对话框"""
        try:
            if self.d(text="等待").exists(timeout=1):
                self.d(text="等待").click()
                time.sleep(0.5)
        except:
            pass

        try:
            if self.d(resourceId=UI_ELEMENTS["close_btn"]).exists(timeout=1):
                self.d(resourceId=UI_ELEMENTS["close_btn"]).click()
                time.sleep(0.5)
        except:
            pass

    def _trade_action(self, stock_code, amount, price, action="buy"):
        """
        买入/卖出通用方法

        Args:
            stock_code: 股票代码
            amount: 数量
            price: 价格
            action: "buy" 或 "sell"

        Returns:
            dict: 交易结果
        """
        stock_code = str(stock_code)
        amount = str(amount)
        price = str(price)
        action_cn = "买入" if action == "buy" else "卖出"

        print(f"\n{action_cn}股票: {stock_code} {amount}股 @{price}")

        success = False
        msg = ""
        stock_name = ""

        self._back_to_moni_page()

        # 点击买入/卖出按钮
        button_id = UI_ELEMENTS["menu_buy_image"] if action == "buy" else UI_ELEMENTS["menu_sale_image"]
        button_coord = COORDINATES["buy_button"] if action == "buy" else COORDINATES["sell_button"]

        if self.d(resourceId=button_id).exists:
            self.d(resourceId=button_id).click()
        else:
            self.d.click(*button_coord)
        time.sleep(DEFAULT_WAIT)
        self._close_dialogs()

        # 输入股票代码
        self._input_stock_code(stock_code)

        # 输入价格
        self._input_price(price)

        # 输入数量
        self._input_amount(amount)

        # 截图保存
        self.d.screenshot(f"{action}_{stock_code}_before.png")

        # 点击买入/卖出按钮
        if self.d(text=action_cn).exists:
            self.d(text=action_cn).click()
            time.sleep(DEFAULT_WAIT)

            # 检查确认对话框
            if self.d(resourceId=UI_ELEMENTS["ok_btn"]).exists:
                # 二次确认
                if self._verify_order(stock_code, amount, price):
                    try:
                        stock_name = self.d(resourceId=UI_ELEMENTS["stock_name_value"]).get_text()
                    except:
                        stock_name = stock_code

                    self.d.screenshot(f"{action}_{stock_code}_confirm.png")
                    self.d(resourceId=UI_ELEMENTS["ok_btn"]).click()
                    time.sleep(DEFAULT_WAIT)

                    # OCR 识别结果
                    if self.reader and self.d(resourceId=UI_ELEMENTS["content_scroll"]).exists:
                        self.d(resourceId=UI_ELEMENTS["content_scroll"]).screenshot().save("tmp.png")
                        msg = self._ocr_get_full_text()
                    else:
                        h = self.d.dump_hierarchy()
                        if "委托已提交" in h or "成功" in h:
                            msg = "委托已提交"
                        else:
                            msg = "已提交"

                    # 关闭结果对话框
                    if self.d(resourceId=UI_ELEMENTS["ok_btn"]).exists:
                        self.d(resourceId=UI_ELEMENTS["ok_btn"]).click()

                    success = True
                    print(f"✓ {action_cn}成功: {msg}")
                else:
                    # 确认失败，取消
                    self.d(resourceId=UI_ELEMENTS["cancel_btn"]).click()
                    msg = "订单确认失败"
                    print(f"✗ {msg}")

        # 截图保存
        time.sleep(1)
        self.d.screenshot(f"{action}_{stock_code}_after.png")

        # 返回
        self.d.press("back")
        time.sleep(1)

        return {
            'success': success,
            'msg': msg,
            'stock_name': stock_name.replace(" ", ""),
            'amount': amount,
            'price': price,
            'type': action_cn
        }

    def _input_stock_code(self, stock_code):
        """输入股票代码"""
        self._close_dialogs()

        # 尝试多个可能的输入框
        input_ids = [UI_ELEMENTS["content_stock"], UI_ELEMENTS["content_buy_stock"]]
        for rid in input_ids:
            if self.d(resourceId=rid).exists:
                self.d(resourceId=rid).click()
                time.sleep(1)
                break

        # 清空并输入
        self._input_text(stock_code)
        time.sleep(DEFAULT_WAIT)

        # 选择搜索结果
        if self.d(resourceId=UI_ELEMENTS["stockname_tv"]).exists:
            try:
                # 尝试使用 xpath 选择第一个结果
                self.d.xpath(XPATHS["stock_search_result"]).click()
            except:
                # 备选方案
                self.d(resourceId=UI_ELEMENTS["stockname_tv"]).click()
            time.sleep(DEFAULT_WAIT)

    def _input_price(self, price):
        """输入价格"""
        self._close_dialogs()
        if self.d(resourceId=UI_ELEMENTS["stockprice"]).exists:
            self.d(resourceId=UI_ELEMENTS["stockprice"]).click()
            time.sleep(1)
            self._input_text(price)

    def _input_amount(self, amount):
        """输入数量"""
        self._close_dialogs()
        if self.d(resourceId=UI_ELEMENTS["stockvolume"]).exists:
            self.d(resourceId=UI_ELEMENTS["stockvolume"]).click()
            time.sleep(1)
            self._input_text(amount)

    def _input_text(self, text):
        """文本输入工具"""
        self.d.shell("input keyevent 123")  # MOVE_END
        for _ in range(INPUT_CLEAR_COUNT):
            self.d.shell("input keyevent 67")  # DEL
        self.d.shell(f"input text {text}")

    def _verify_order(self, stock_code, amount, price):
        """验证订单信息"""
        time.sleep(1)
        try:
            code = self.d(resourceId=UI_ELEMENTS["stock_code_value"]).get_text().replace(" ", "")
            num = self.d(resourceId=UI_ELEMENTS["number_value"]).get_text().replace(" ", "").replace(",", "")
            prc = float(self.d(resourceId=UI_ELEMENTS["price_value"]).get_text())

            if code != stock_code:
                return False
            if num != amount:
                return False
            if abs(float(price) - prc) > 0.01:
                return False
            return True
        except:
            return False

    def _ocr_get_full_text(self):
        """OCR 识别全部文本"""
        if not self.reader:
            return ""
        result = self.reader.readtext("tmp.png")
        text = ""
        for line in result:
            text += line[1]
        return text

    def _ocr_parse_holding(self, path):
        """OCR 解析持仓信息"""
        if not self.reader:
            return {}

        Image.open(path).crop((11, 11, 165, 55)).save("tmp.png")
        result = self.reader.readtext("tmp.png")
        stock_name = result[0][1] if result else "未知"

        Image.open(path).crop((419, 11, 548, 55)).save("tmp.png")
        result = self.reader.readtext("tmp.png")
        stock_count = result[0][1] if result else "0"

        Image.open(path).crop((419, 60, 548, 102)).save("tmp.png")
        result = self.reader.readtext("tmp.png")
        stock_available = result[0][1] if result else "0"

        return {
            "股票名称": stock_name.replace(" ", ""),
            "股票余额": int(stock_count.replace(",", "")),
            "可用余额": int(stock_available.replace(",", ""))
        }

    def _ocr_parse_withdrawal(self, path):
        """OCR 解析撤单信息"""
        if not self.reader:
            return {}

        Image.open(path).crop((11, 11, 165, 55)).save("tmp.png")
        result = self.reader.readtext("tmp.png")
        stock_name = result[0][1] if result else "未知"

        Image.open(path).crop((219, 11, 390, 55)).save("tmp.png")
        result = self.reader.readtext("tmp.png")
        stock_price = result[0][1] if result else "0"

        Image.open(path).crop((419, 11, 548, 55)).save("tmp.png")
        result = self.reader.readtext("tmp.png")
        stock_count = result[0][1] if result else "0"

        Image.open(path).crop((589, 11, 704, 55)).save("tmp.png")
        result = self.reader.readtext("tmp.png")
        t = result[0][1] if result else "未知"

        return {
            "股票名称": stock_name.replace(" ", ""),
            "委托价格": float(stock_price.replace(",", "")),
            "委托数量": int(stock_count.replace(",", "")),
            "委托类型": t.replace(" ", "")
        }
