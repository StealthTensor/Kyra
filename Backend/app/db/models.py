from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text, Float, func, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    accounts = relationship("Account", back_populates="user")
    memories = relationship("AgentMemory", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    email_address = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True))
    last_sync_id = Column(String)
    provider = Column(String, default='gmail')
    
    user = relationship("User", back_populates="accounts")
    emails = relationship("Email", back_populates="account")

class Email(Base):
    __tablename__ = "emails"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    gmail_id = Column(String, unique=True, nullable=False)
    thread_id = Column(String, nullable=False)
    sender = Column(String, nullable=False)
    subject = Column(String)
    body_plain = Column(Text)
    received_at = Column(DateTime(timezone=True))
    importance_score = Column(Integer, default=0)
    category = Column(String)
    explanation = Column(Text)
    confidence = Column(Float)
    embedding = Column(Vector(768)) # pgvector
    
    account = relationship("Account", back_populates="emails")
    interactions = relationship("Interaction", back_populates="email")
    attachments = relationship("Attachment", back_populates="email")

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"))
    filename = Column(String, nullable=False)
    content_type = Column(String)
    size = Column(Integer)
    extracted_text = Column(Text)
    
    email = relationship("Email", back_populates="attachments")

class ThreadSummary(Base):
    __tablename__ = "thread_summaries"
    thread_id = Column(String, primary_key=True) # Gmail Thread ID
    summary = Column(Text)
    message_count = Column(Integer)
    last_updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class DailyDigest(Base):
    __tablename__ = "daily_digests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="digests")

# Update User relationship
User.digests = relationship("DailyDigest", back_populates="user")

class AgentMemory(Base):
    __tablename__ = "agent_memory"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    key = Column(String, nullable=False)
    value = Column(JSONB, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="memories")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"))
    action = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    email = relationship("Email", back_populates="interactions")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    conversation = relationship("Conversation", back_populates="messages")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"), nullable=True)
    description = Column(Text, nullable=False)
    due_date = Column(DateTime(timezone=True))
    status = Column(String, default='pending')
    priority = Column(String, default='medium')
    task_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="tasks")
    email = relationship("Email")

User.tasks = relationship("Task", back_populates="user")
