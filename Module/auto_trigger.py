# Module/auto_trigger.py
import ctypes
import time
from math import sqrt

class AutoTrigger:
    def __init__(self):
        self.enabled = True          # True=开, False=关
        self.precision_px = 10       # 偏差阈值
        self.cooldown_ms = 150       # 冷却毫秒
        self._last_shot_ms = 0
    
    def check_and_shoot(self, target_center_x, target_center_y, screen_center_x, screen_center_y):
        """检查是否瞄准到目标，是则开枪"""
        if not self.enabled:
            return False
        
        dx = target_center_x - screen_center_x
        dy = target_center_y - screen_center_y
        distance = sqrt(dx*dx + dy*dy)
        
        if distance <= self.precision_px:
            now_ms = time.time() * 1000
            if now_ms >= self._last_shot_ms:
                # 开枪
                ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
                time.sleep(0.01)
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
                self._last_shot_ms = now_ms + self.cooldown_ms
                return True
        return False