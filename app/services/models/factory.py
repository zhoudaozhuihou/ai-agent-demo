from typing import Type, Dict
from .base import SQLOptimizer
from .default_optimizer import DefaultOptimizer
from .copilot_optimizer import CopilotOptimizer
from app.core.config import settings

class OptimizerFactory:
    """优化器工厂类"""
    
    _optimizers: Dict[str, Type[SQLOptimizer]] = {
        "default": DefaultOptimizer,
        "copilot": CopilotOptimizer
    }

    @classmethod
    def register(cls, name: str, optimizer_class: Type[SQLOptimizer]):
        """注册新的优化器"""
        cls._optimizers[name] = optimizer_class

    @classmethod
    def create(cls, name: str = None) -> SQLOptimizer:
        """创建优化器实例"""
        # 如果没有指定名称，使用配置中的活动优化器
        name = name or settings.ACTIVE_OPTIMIZER

        # 检查优化器是否启用
        if not settings.is_optimizer_enabled(name):
            raise ValueError(f"Optimizer '{name}' is not enabled")

        # 获取优化器类
        optimizer_class = cls._optimizers.get(name)
        if not optimizer_class:
            raise ValueError(f"Unknown optimizer: {name}")

        # 获取优化器配置
        config = settings.get_optimizer_config(name)
        
        # 创建并返回优化器实例
        return optimizer_class(config=config.config)

    @classmethod
    def list_available(cls) -> Dict[str, str]:
        """列出所有可用的优化器"""
        return {
            name: settings.get_optimizer_config(name).description
            for name in cls._optimizers.keys()
            if settings.is_optimizer_enabled(name)
        }
