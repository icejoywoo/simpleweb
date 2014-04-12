#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-4-10

__author__ = 'icejoywoo'

"""
motor mongodb async version for tornado
mongoengine is like ORM for mongodb, but not update for a few months.

But maybe I should use sqlalchemy for sqlite3 or mysql.
"""

from sqlalchemy import create_engine, func, Table, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref


Base = declarative_base()


# entities defination

user_sample_association_table = Table('user_sample_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('sample_id', Integer, ForeignKey('sample.id')),
    # extra data
    Column('category_id', Integer, ForeignKey('category.id'))
)


class User(Base):
    """
    用户信息, 与Sample多对多, 方便用户认领任务, 并且做交叉判断
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(16), nullable=False)
    created_at = Column(DateTime, default=func.now())
    samples = relationship("Sample", secondary=user_sample_association_table,
                           backref="users")


class Category(Base):
    """
    对Sample数据进行分类的信息, 例如: 购物, 饮食等.
    自引用, 一对多, 树状结构
    """
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    parent_id = Column(Integer, ForeignKey('category.id'))  # 引用自身id作为外键
    children = relationship("Category")  # 建立one-to-many关系


class Sample(Base):
    """
    样本信息, 与User多对多, 方便用户认领任务, 并且做交叉判断
    """
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True)
    data = Column(String(255), nullable=False)
    # 用户标注结果经过评判后的最终结果
    labeled_result = Column("s_labeled_result", Integer, ForeignKey('category.id'))


class Result(Base):
    """
    预测结果, 和sample多对一
    """
    __tablename__ = "result"

    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    # 预测结果
    predict_result = Column(Integer, ForeignKey('category.id'))

if __name__ == "__main__":
    import sqlalchemy
    print "version:", sqlalchemy.__version__

    engine = create_engine('sqlite:///:memory:', echo=True)
    db = scoped_session(sessionmaker(bind=engine))

    Base.metadata.create_all(engine)
