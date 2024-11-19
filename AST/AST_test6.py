import functools
import time
import logging
from typing import Callable, Any

# 設置日誌配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Aspect:
    """切面基礎類"""
    def __init__(self, enable_logging=True, enable_timing=True):
        self.enable_logging = enable_logging
        self.enable_timing = enable_timing

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 前置通知(Before advice)
            if self.enable_logging:
                logger.info(f"Starting execution of {func.__name__}")
                logger.info(f"Arguments: args={args}, kwargs={kwargs}")

            start_time = time.time()

            try:
                # 執行原始函數
                result = func(*args, **kwargs)

                # 返回通知(After returning advice)
                if self.enable_logging:
                    logger.info(f"Function {func.__name__} completed successfully")
                    logger.info(f"Return value: {result}")

                return result

            except Exception as e:
                # 異常通知(After throwing advice)
                logger.error(f"Exception in {func.__name__}: {str(e)}")
                raise

            finally:
                # 後置通知(After advice)
                if self.enable_timing:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    logger.info(f"Execution time of {func.__name__}: {execution_time:.4f} seconds")

        return wrapper

class TransactionAspect:
    """事務處理切面"""
    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("Beginning transaction")
            try:
                result = func(*args, **kwargs)
                logger.info("Committing transaction")
                return result
            except Exception as e:
                logger.error("Rolling back transaction due to error")
                raise
        return wrapper

# 使用範例
class UserService:
    def __init__(self):
        self.users = {}

    @Aspect(enable_logging=True, enable_timing=True)
    def create_user(self, user_id: int, name: str) -> dict:
        """創建新用戶"""
        # 模擬一些處理時間
        time.sleep(0.1)
        user = {"id": user_id, "name": name}
        self.users[user_id] = user
        return user

    @Aspect()
    @TransactionAspect()
    def update_user(self, user_id: int, new_name: str) -> dict:
        """更新用戶信息"""
        if user_id not in self.users:
            raise ValueError(f"User {user_id} not found")
        self.users[user_id]["name"] = new_name
        return self.users[user_id]

# 測試代碼
def test_aop():
    service = UserService()

    # 測試創建用戶
    user = service.create_user(1, "Alice")
    print("\n創建用戶結果:", user)

    # 測試更新用戶
    updated_user = service.update_user(1, "Alice Smith")
    print("\n更新用戶結果:", updated_user)

    # 測試異常情況
    try:
        service.update_user(999, "Non-existent User")
    except ValueError as e:
        print("\n預期的錯誤:", str(e))

if __name__ == "__main__":
    test_aop()