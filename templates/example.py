#!/usr/bin/env python3
"""
PyTools 示例脚本
展示 Python 代码格式化、检查和执行
"""

import sys
import numpy as np
import pandas as pd
from typing import List, Dict, Optional


class DataProcessor:
    """数据处理类示例"""
    
    def __init__(self, data: List[float]):
        self.data = data
        self.processed = False
        
    def process(self) -> List[float]:
        """处理数据"""
        if not self.data:
            raise ValueError("数据不能为空")
            
        # 计算均值和标准差
        mean_val = np.mean(self.data)
        std_val = np.std(self.data)
        
        # 标准化数据
        normalized = [(x - mean_val) / std_val for x in self.data]
        self.processed = True
        
        return normalized
    
    def summary(self) -> Dict[str, float]:
        """生成数据摘要"""
        if not self.processed:
            self.process()
            
        return {
            'mean': np.mean(self.data),
            'std': np.std(self.data),
            'min': np.min(self.data),
            'max': np.max(self.data),
            'count': len(self.data)
        }


def calculate_fibonacci(n: int) -> List[int]:
    """计算斐波那契数列"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib


def main():
    """主函数"""
    print("PyTools 示例脚本")
    print("=" * 40)
    
    # 示例数据
    sample_data = [1.2, 2.3, 3.4, 4.5, 5.6]
    
    # 创建处理器
    processor = DataProcessor(sample_data)
    
    # 处理数据
    normalized = processor.process()
    print(f"原始数据: {sample_data}")
    print(f"标准化后: {normalized}")
    
    # 显示摘要
    summary = processor.summary()
    print(f"\n数据摘要:")
    for key, value in summary.items():
        print(f"  {key}: {value:.4f}")
    
    # 计算斐波那契数列
    fib_sequence = calculate_fibonacci(10)
    print(f"\n斐波那契数列(前10个): {fib_sequence}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())