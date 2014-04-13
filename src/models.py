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
class Category(Base):
    """
    对Sample数据进行分类的信息, 例如: 购物, 饮食等.
    自引用, 一对多, 树状结构
    """
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey('category.id'))  # 引用自身id作为外键
    children = relationship("Category")  # 建立one-to-many关系

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category: %(name)r>" % self.__dict__

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UserSampleAssociation(Base):
    """
    user和sample多对多中间表
    """
    __tablename__ = 'user_sample_association'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    sample_id = Column(Integer, ForeignKey('sample.id'), primary_key=True)
    sample = relationship("Sample")
    user = relationship("User")
    # extra data: user对sample的标注结果
    category_id = Column('category_id', Integer, ForeignKey('category.id'))
    category = relationship("Category")

    def __repr__(self):
        return "<UserSampleAssociation: %r, %r>" % (self.user, self.sample)


class User(Base):
    """
    用户信息, 与Sample多对多, 方便用户认领任务, 并且做交叉判断
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    nickname = Column(String(50), nullable=False)
    password = Column(String(16), nullable=False)
    created_at = Column(DateTime, default=func.now())
    samples = relationship("UserSampleAssociation")

    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password

    def __repr__(self):
        return "<User: %(name)r>" % self.__dict__


class SampleType(Base):
    """
    预测方法
    """
    __tablename__ = "sample_type"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<SampleType: %(name)r>" % self.__dict__


class Sample(Base):
    """
    样本信息, 与User多对多, 方便用户认领任务, 并且做交叉判断
    """
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True)
    sample_type_id = Column(Integer, ForeignKey('sample_type.id'))
    sample_type = relationship("SampleType")
    # 需要标注的样本数据
    data = Column(String(255), nullable=False)
    users = relationship("UserSampleAssociation")
    # 用户标注结果经过评判后的最终结果
    labeled_result = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category")

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return "<User: %(data)r>" % self.__dict__


class Result(Base):
    """
    预测结果, 和sample多对一
    """
    __tablename__ = "result"

    id = Column(Integer, primary_key=True)
    sample_id = Column(Integer, ForeignKey("sample.id"), nullable=False)
    sample = relationship("Sample", backref=backref("result", uselist=False))

    # 预测结果的category_id
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category")

    method_id = Column(Integer, ForeignKey('method.id'))
    method = relationship("Method", backref=backref("result", uselist=False))

    evaluate_id = Column(Integer, ForeignKey('evaluate.id'))
    evaluate = relationship("Evaluate", backref=backref("result", uselist=False))

    def __init__(self, sample, method, category):
        self.sample = sample
        self.method = method
        self.category = category

    def __repr__(self):
        return "<Result: %r, %r, %r>" % (self.sample, self.method, self.category)


class Method(Base):
    """
    预测方法
    """
    __tablename__ = "method"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<Method: %(name)r>" % self.__dict__

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Evaluate(Base):
    """
    算法的结果进行评估, 例如好, 中, 差
    """
    __tablename__ = "evaluate"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Evaluate: %(name)r>" % self.__dict__


if __name__ == "__main__":
    import sqlalchemy
    print "version:", sqlalchemy.__version__

    engine = create_engine('sqlite:///sqlite3.db', echo=True)
    db = scoped_session(sessionmaker(bind=engine))

    Base.metadata.create_all(engine)

    # 分类名称树, 可以无线递归下去
    category = Category(u"影视")
    category.children.append(Category(u"电影"))
    category.children.append(Category(u"电视"))
    print category, category.children
    db.add(category)
    db.commit()

    # user和sample
    user = User("admin", "admin", "123456")
    print user
    a = UserSampleAssociation()
    sample = Sample("test")
    a.sample = sample
    a.sample.category = category
    user.samples.append(a)
    print user.samples
    print user.samples[0].sample.users
    db.add(a)
    db.add(user)
    db.commit()
    print a.sample.users

    # result
    method = Method("dnn", "Deep Netron Network")
    result = Result(sample, method, category)
    db.add(method)
    db.add(result)
    db.commit()
    print result
