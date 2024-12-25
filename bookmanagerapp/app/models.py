from config import app, db
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum, SmallInteger
from sqlalchemy_utils import EmailType
from flask_login import UserMixin
from enum import Enum as RoleEnum
from flask_login import current_user
from datetime import datetime as dt
from sqlalchemy import text
from datetime import datetime, timedelta

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2
class MethodRecevie(RoleEnum):
    AITHECOUNTER = 1
    DELIVERY = 2
class MethodBank(RoleEnum):
    MOMO = 1
    BANKWHENGET = 2

class StateOrder(RoleEnum):
    PENDINGPAYMENT = 1
    PENDINGPROCESSING = 2
    DELIVERING = 3
    CONFIRM = 4
    CANCEL = 5
class CategoryBook(db.Model):
    __tablename__ = 'category_book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id',ondelete='CASCADE'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id',ondelete='CASCADE'), nullable=False)

    def __str__(self):
        return str(self.id)

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dt.now())
    updated_at = Column(DateTime, default=dt.now(), onupdate=dt.now())

class Client(db.Model, UserMixin):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(EmailType, unique=True, nullable=True)
    password = Column(String(512), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    info_user_order = relationship('InfoUserOrder', backref='client', lazy=True)
    reviews = relationship('Review', backref='client', lazy=True)

    def __str__(self):
        return self.name
    def to_dict(self):
            return {
                'id': self.id,
                'fullname': self.name,
                'username': self.username,
            }




class Category(BaseModel):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False,unique=True)
    books = relationship('Book', secondary='category_book', back_populates='categories')

    def __str__(self):
        return self.name
    def to_dict(self):
            return {
                'id': self.id,
                'name': self.name
            }
class Book(BaseModel):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False,unique=True)
    author = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    prices = relationship('Price', backref='book', lazy=True)
    image = Column(String(100), nullable=True)
    quantity = Column(Integer, default=1, nullable=False)    
    categories = relationship(Category, secondary='category_book', back_populates='books')
    order_details = relationship('OrderDetail', backref='book', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'image': self.image,
            'quantity': self.quantity,
            'categories': [category.name for category in self.categories],
            'prices': [{'name_price': price.name_price, 'price': price.price} for price in self.prices]
        }
    def __str__(self):
        return self.title

class Price(db.Model):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_price = Column(String(100), nullable=False)
    price = Column(Float, default=0, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    
    def __str__(self):
        return self.name_price


class TakedBook(BaseModel):
    __tablename__ = 'taked_books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    details = relationship('TakedBookDetail', backref='taked_book', lazy=True, cascade="all, delete-orphan")

    def __str__(self):
        return str(self.id)


class TakedBookDetail(db.Model): 
    __tablename__ = 'taked_book_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    taked_book_id = Column(Integer, ForeignKey(TakedBook.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    price = Column(Float, default=0, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    def __str__(self):
        return str(self.id)
    

class Receipt(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)
    is_pay = Column(Boolean, default=False)


class ReceiptDetails(BaseModel):
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    

class InfoUserOrder(BaseModel):
    __tablename__ = 'info_user_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False,unique=True)
    address = Column(String(255), nullable=False)
    email = Column(EmailType, nullable=False)
    user_id = Column(Integer, ForeignKey(Client.id), nullable=True)
    orders = relationship('Order', backref='client', lazy=True)
    def __str__(self):
        return self.name
    

class Coupon(BaseModel):
    __tablename__ = 'coupons'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False, unique=True)
    discount = Column(Float, nullable=False)

    def __str__(self):
        return self.code
    

# class BookAttention(BaseModel):
#     __tablename__ = 'book_attentions'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
#     client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
#     def __str__(self):
#         return str(self.id)

class Order(BaseModel):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    info_user_order_id = Column(Integer, ForeignKey(InfoUserOrder.id), nullable=False)
    details = relationship('OrderDetail', backref='order', lazy=True, cascade="all, delete-orphan")
    methodReceive = Column(Enum(MethodRecevie), default=MethodRecevie.AITHECOUNTER)
    methodBank = Column(Enum(MethodBank), default=MethodBank.MOMO)
    coupon_id  = Column(Integer, ForeignKey(Coupon.id), nullable=True)
    delivery_address = Column(String(255), nullable=False)
    state =  Column(Enum(StateOrder), default=StateOrder.PENDINGPAYMENT)
    def __str__(self):
        return str(self.id)
    @staticmethod
    def update_order_status():
        with app.app_context():
            now = datetime.now()
            cutoff_time = now - timedelta(hours=48)
            orders_to_update = Order.query.filter(Order.state != StateOrder.CONFIRM, Order.created_at <= cutoff_time).all()
            for order in orders_to_update:
                order.state = StateOrder.CANCEL
                db.session.commit()


class OrderDetail(BaseModel):
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    price = Column(Float, default=0, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    def __str__(self):
        return str(self.id)
    

class Review(BaseModel):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    content = Column(String(255), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    rate = Column(SmallInteger, default=5)
    def __str__(self):
        return self.content
    
class CancelOrder(BaseModel):
    __tablename__ = 'cancel_orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    reason = Column(String(255), nullable=False)

    def __str__(self):
        return self.reason



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # with db.engine.connect() as connection:
        #     connection.execute(text('DROP TABLE IF EXISTS taked_book_details'))
        # db.session.commit()
        # info_user_order = InfoUserOrder(name='user3', phone='user3', address='use3',email="user3@gmail.com")
        # db.session.add(info_user_order)
        # db.session.commit()
        # order = Order(info_user_order_id=info_user_order.id, delivery_address='user3')
        # db.session.add(order)
        # db.session.commit()

        # u = Client(name='user', username='user', email='user2k4@gmail.com',password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), user_role=UserRole.USER)
        # programming = get_or_create_category('Programming')
        # python = get_or_create_category('Python')
        # java_cat = get_or_create_category('Java')

        # # Thêm sách với các category
        # book = Book(
        #     title='Python2', 
        #     author='Guido van Rossum', 
        #     description='Python programming language', 
        #     image='python.jpg',
        #     prices=[
        #         Price(name_price='Giá Gốc', price=1000), 
        #         Price(name_price='Giá giảm', price=200)
        #     ],
        #     categories=[programming, python]
        # )
        
        # java = Book(
        #     title='Java', 
        #     author='James Gosling', 
        #     description='Java programming language', 
        #     image='java.jpg',
        #     prices=[
        #         Price(name_price='Giá Gốc', price=2000), 
        #         Price(name_price='Giá giảm', price=400)
        #     ],
        #     categories=[programming, java_cat]
        # )
        # c = Book(
        #     title='C', 
        #     author='James Gosling', 
        #     description='Java programming language', 
        #     image='java.jpg',
        #     prices=[
        #         Price(name_price='Giá Gốc', price=2000), 
        #         Price(name_price='Giá giảm', price=400)
        #     ],
        #     categories=[programming]
        # )

        # db.session.add(book)
        # db.session.add(java)
        # db.session.add(u)
        db.session.commit()
