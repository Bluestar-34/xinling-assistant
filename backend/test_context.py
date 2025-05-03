from database import SessionManager, get_db
from context_manager import ContextManager
import uuid

def test_context_management():
    # 创建测试会话ID
    test_session_id = str(uuid.uuid4())
    
    # 获取数据库会话
    db = next(get_db())
    session_manager = SessionManager(db)
    context_manager = ContextManager(session_manager)
    
    try:
        # 测试1：添加用户信息
        print("测试1：添加用户信息")
        context_manager.add_message(test_session_id, "user", "我今年14岁")
        context = context_manager.get_context(test_session_id)
        assert any("age" in msg["content"] for msg in context), "用户信息未正确存储"
        print("✓ 用户信息存储成功")
        
        # 测试2：添加多条消息
        print("\n测试2：添加多条消息")
        for i in range(25):  # 添加25条消息以触发压缩
            context_manager.add_message(test_session_id, "user", f"测试消息{i}")
            context_manager.add_message(test_session_id, "assistant", f"回复{i}")
        
        # 测试3：验证上下文压缩
        print("\n测试3：验证上下文压缩")
        messages = session_manager.get_messages(test_session_id)
        assert len(messages) <= 25, "上下文压缩失败"
        print(f"✓ 消息数量：{len(messages)}")
        
        # 测试4：验证上下文总结
        print("\n测试4：验证上下文总结")
        context = context_manager.get_context(test_session_id)
        assert any("之前的对话要点" in msg["content"] for msg in context), "上下文总结未生成"
        print("✓ 上下文总结生成成功")
        
        # 测试5：验证会话总结
        print("\n测试5：验证会话总结")
        summary = context_manager.get_session_summary(test_session_id)
        assert "message_count" in summary, "会话总结不完整"
        assert "user_info" in summary, "用户信息未包含在总结中"
        print("✓ 会话总结生成成功")
        
        print("\n所有测试通过！上下文管理功能正常。")
        
    except Exception as e:
        print(f"\n测试失败：{str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_context_management() 