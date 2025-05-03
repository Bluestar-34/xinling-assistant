from database import SessionManager, get_db
from models import Session, Message
from context_manager import ContextManager
import uuid
from datetime import datetime

def test_database_operations():
    # 创建测试会话ID
    test_session_id = str(uuid.uuid4())
    
    # 获取数据库会话
    db = next(get_db())
    session_manager = SessionManager(db)
    context_manager = ContextManager(session_manager)
    
    try:
        # 测试1：创建会话
        print("测试1：创建会话")
        session = session_manager.create_session(test_session_id)
        assert session is not None, "会话创建失败"
        print("✓ 会话创建成功")
        
        # 测试2：添加消息
        print("\n测试2：添加消息")
        message = session_manager.add_message(test_session_id, "user", "测试消息1")
        assert message is not None, "消息添加失败"
        print("✓ 消息添加成功")
        
        # 测试3：获取消息
        print("\n测试3：获取消息")
        messages = session_manager.get_messages(test_session_id)
        assert len(messages) > 0, "获取消息失败"
        print(f"✓ 成功获取 {len(messages)} 条消息")
        
        # 测试4：上下文管理
        print("\n测试4：上下文管理")
        context_manager.add_message(test_session_id, "user", "我今年14岁")
        context = context_manager.get_context(test_session_id)
        assert len(context) > 0, "获取上下文失败"
        print("✓ 上下文管理正常")
        
        # 测试5：会话统计
        print("\n测试5：会话统计")
        stats = session_manager.get_session_stats(test_session_id)
        assert stats is not None, "获取会话统计失败"
        print(f"✓ 会话统计：{stats}")
        
        # 测试6：清理会话
        print("\n测试6：清理会话")
        session_manager.clear_messages(test_session_id)
        messages = session_manager.get_messages(test_session_id)
        assert len(messages) == 0, "清理会话失败"
        print("✓ 会话清理成功")
        
        print("\n所有测试通过！数据库运行正常。")
        
    except Exception as e:
        print(f"\n测试失败：{str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_database_operations() 