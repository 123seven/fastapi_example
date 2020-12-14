# @Time    : 2020/12/2 6:48 下午
# @Author  : Seven
# @File    : apollo_client
# @Desc    : ApolloClient

import json
import logging
import threading
import time
from typing import Any, Callable

import requests


class ApolloClient(object):
    def __init__(self, app_id: str, cluster_name: str, config_server_url: str, flush_time: int = 70, ip: Any = None,
                 call_back: Callable = None):
        """
        初始化 ApolloClient
        :param app_id:应用的appId
        :param cluster_name:集群名
        :param config_server_url:服务器地址
        :param flush_time:更新时间
        :param ip:本机ip(用来实现灰度发布)
        :param call_back:更新回调函数
        """
        self.appId = app_id
        self.cluster = cluster_name
        self.config_server_url = config_server_url
        self.flush_time = flush_time
        self.ip = ip
        self.call_back = call_back

        self.init_ip(ip)
        self.stopped = False
        self._stopping = False
        self._cache = {}
        self._notification_map = {'application': -1, "common": -1, "app": -1}
        self.thread = None

    def init_ip(self, ip: Any):
        """
        获取本机ip
        :param ip: ip地址
        """
        if ip:
            self.ip = ip
        else:
            import socket
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            finally:
                s.close()
            self.ip = ip

    def get_value_default_namespace(self, key, default_val=None):
        return self.get_value(key, default_val=default_val, namespace="application")

    def get_value(self, key: str, default_val: Any = None, namespace: str = None) -> Any:
        """
        获取配置参数
        :param key: 参数key
        :param default_val: 默认值
        :param namespace: 命名空间
        :return:
        """
        try:
            v = self._get_value(key, namespace)
            if v:
                return v
            if namespace:
                v = self._cached_http_get(key, None, namespace)
                if v:
                    return v
            else:
                for namespace in self._notification_map:
                    v = self._cached_http_get(key, None, namespace)
                    if v:
                        return v
            return default_val
        except Exception as e:
            logging.error(e)
            return default_val

    def _get_value(self, key: str, namespace: str = 'application') -> Any:
        """
        从缓存中获取配置参数
        :param key: 参数key
        :param namespace: 命名空间
        :return:
        """
        if not namespace:
            if namespace in self._cache:
                if self._cache[namespace].get(key):
                    return self._cache[namespace][key]
            return None
        if namespace not in self._notification_map:
            self._notification_map[namespace] = -1
            logging.info("Add namespace '%s' to local notification map", namespace)

        if namespace not in self._cache:
            self._cache[namespace] = {}
            logging.info("Add namespace '%s' to local cache", namespace)
            # self._long_poll()

        if key in self._cache[namespace]:
            return self._cache[namespace][key]
        return None

    def start(self, catch_signals: bool = True):
        """
        启动配置客户端
        :param catch_signals:
        """
        # if len(self._cache) == 0:
        #     self._long_poll()
        if catch_signals:
            import signal
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            signal.signal(signal.SIGABRT, self._signal_handler)
        self.thread = threading.Thread(target=self._listener)
        self.thread.setDaemon(self)
        self.thread.start()

    def stop(self):
        """
        停止监听
        :return:
        """
        self._stopping = True
        logging.info("Stopping listener..")

    def _cached_http_get(self, key: str, default_val: Any = None, namespace: str = 'application') -> Any:
        """
        远程获取参数
        :param key:
        :param default_val:
        :param namespace:
        :return:
        """
        if not namespace:
            return default_val
        url = '{}/configfiles/json/{}/{}/{}?ip={}'.format(self.config_server_url, self.appId, self.cluster, namespace,
                                                          self.ip)
        r = requests.get(url, timeout=5)
        if r.ok:
            data = r.json()
            self._cache[namespace] = data
            logging.info('Updated local cache for namespace %s', namespace)
        else:
            data = self._cache[namespace]

        if key in data:
            return data[key]
        else:
            return default_val

    def _signal_handler(self, *args, **xx):
        """
        注册监听
        :return:
        """
        logging.info('You pressed Ctrl+C!')
        self._stopping = True

    def _long_poll(self):
        """
        长轮询获取配置
        :return:
        """
        try:
            url = '{0}/notifications/v2'.format(self.config_server_url)
            notifications = []
            for key in self._notification_map:
                notification_id = self._notification_map[key]
                notifications.append({
                    'namespaceName': key,
                    'notificationId': notification_id
                })

            r = requests.get(url=url, params={
                'appId': self.appId,
                'cluster': self.cluster,
                'notifications': json.dumps(notifications, ensure_ascii=False)
            }, timeout=self.flush_time)  # 必须保持60秒以上

            logging.debug('Long polling returns %d: url=%s', r.status_code, r.request.url)

            if r.status_code == 304:
                # no change, loop
                logging.debug('No change, loop..')
                time.sleep(self.flush_time)
                return

            if r.status_code == 200:
                data = r.json()
                for entry in data:
                    ns = entry['namespaceName']
                    nid = entry['notificationId']
                    logging.info("%s has changes: notificationId=%d", ns, nid)
                    self._cached_http_get('test', namespace=ns)
                    self._notification_map[ns] = nid
                if self.call_back:
                    self.call_back()
            else:
                logging.warning('Sleep..')
                time.sleep(self.flush_time)
        except Exception as e:
            logging.error(e)

    def _listener(self):
        """
        监听事件
        :return:
        """
        logging.info('Entering listener loop..')
        while not self._stopping:
            self._long_poll()

        logging.info("Listener stopped!")
        self.stopped = True
