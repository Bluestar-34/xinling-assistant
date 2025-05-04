from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import os
from datetime import datetime, timedelta
from typing import Generator

# 创建数据库引擎
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 会话管理
class SessionManager:
    def __init__(self, db: Session):
        self.db = db
        self.max_history = 20  # 增加最大历史消息数
        self.max_age = timedelta(hours=24)  # 会话最大保存时间

    def create_session(self, session_id: str) -> None:
        """创建新的会话"""
        from models import Session
        session = Session(id=session_id)
        self.db.add(session)
        self.db.commit()

    def get_session(self, session_id: str):
        """获取会话"""
        from models import Session
        return self.db.query(Session).filter(Session.id == session_id).first()

    def delete_session(self, session_id: str) -> None:
        """删除会话"""
        from models import Session
        session = self.db.query(Session).filter(Session.id == session_id).first()
        if session:
            self.db.delete(session)
            self.db.commit()

    @contextmanager
    def session_scope(self):
        """会话作用域管理器"""
        try:
            yield self.db
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def add_message(self, session_id, role, content):
        """添加消息到会话"""
        from models import Session, Message
        session = self.get_session(session_id)
        if not session:
            session = self.create_session(session_id)
        
        message = Message(
            session_id=session_id,
            role=role,
            content=content
        )
        self.db.add(message)
        self.db.commit()
        return message

    def get_messages(self, session_id, limit=None):
        """获取会话消息历史"""
        from models import Message
        query = self.db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.created_at.asc())  # 改为按时间正序排列
        
        if limit:
            query = query.limit(limit)
        
        return query.all()

    def clear_messages(self, session_id):
        """清空会话的所有消息"""
        from models import Message
        self.db.query(Message).filter(
            Message.session_id == session_id
        ).delete()
        self.db.commit()

    def cleanup_old_sessions(self):
        """清理过期会话"""
        from models import Session
        cutoff_time = datetime.utcnow() - self.max_age
        self.db.query(Session).filter(
            Session.updated_at < cutoff_time
        ).delete()
        self.db.commit()

    def get_session_stats(self, session_id):
        """获取会话统计信息"""
        from models import Message
        from sqlalchemy import func
        
        stats = self.db.query(
            func.count(Message.id).label('total_messages'),
            func.min(Message.created_at).label('first_message'),
            func.max(Message.created_at).label('last_message')
        ).filter(
            Message.session_id == session_id
        ).first()
        
        return {
            'total_messages': stats.total_messages,
            'first_message': stats.first_message,
            'last_message': stats.last_message,
            'duration': (stats.last_message - stats.first_message) if stats.first_message and stats.last_message else None
        } 