import random


class ProxyPool(object):
    def __init__(self,proxy_list):
        self.proxies = proxy_list  # 初始化代理列表

    # def load_proxies(self):
    #     # 这里只是一个示例，你需要替换为实际的代理获取逻辑
    #     self.proxies =

    def get_proxy(self):
        return random.choice(self.proxies)  # 随机选择一个代理

    def validate_proxy(self, proxy,browser):
        # 验证代理的有效性，这里只是一个示例，你需要替换为实际的验证逻辑
        try:
            response = browser.get("http://product.dangdang.com/27878108.html", proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                return True
        except:
            return False

    def update_proxies(self):
        # 更新代理列表，移除无效的代理
        self.proxies = [proxy for proxy in self.proxies if self.validate_proxy(proxy)]
