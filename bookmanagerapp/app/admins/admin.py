from flask_admin.contrib.sqla import ModelView
from flask import redirect,url_for,request
from flask_admin import expose ,BaseView
from flask_login import current_user
from config import app,db,admin
import dao
from models import CancelOrder,Review,Category, Book,Price,TakedBookDetail,Order,OrderDetail,Client
import utils

class AdminAuthenticatedView(ModelView):
    pass
    # def is_accessible(self):
    #     return current_user.is_authenticated

class BaseModelView(AdminAuthenticatedView):
    # column_display_pk = False
    can_create = True
    can_edit = True
    can_export = True
    can_delete = True
class CategoryModelView(BaseModelView):
    column_list = ['id', 'name', 'books']
    column_labels = {
        'id': 'ID',
        'name': 'Category Name',
        'books': 'Books'
    }


class BookModelView(BaseModelView):
    column_list = ['id', 'title', 'author','image', 'description', 'quantity', 'prices', 'categories']
    column_searchable_list = ['title']
    column_filters = ['title', 'prices']
    column_editable_list = ['title', 'prices']
    edit_modal = True

from flask_login import logout_user

class PriceModelView(BaseModelView):
    column_list = ['id', 'name_price', 'price', 'book_id']
    column_editable_list = ['name_price', 'price']
    form_excluded_columns = ['book_id']
class OrderModelView(BaseModelView):
    column_list = ['id', 'info_user_order_id','created_at','state', 'details']

class OrderDetailView(BaseModelView):
    column_list = ['id']


class CancelOrderView(BaseModelView):
    column_list = ['id','order_id','reason']
    column_editable_list = ['reason']

class ReviewView(BaseModelView):
    column_list = ['id']

class TakedBookModelView(BaseModelView):
    column_list = ['id','client_id','taked_book_details']
class TakedBookDetailModelView(BaseModelView):
    column_list = ['id','taked_book_id','book_id','quantity']

class AboutUsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/about-us.html')
class CartView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/cart.html')


class LogoutView(BaseView): 
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('/admin'))
    def is_accessible(self):
        return current_user.is_authenticated
    
    
class StatsView(BaseView):
    @expose("/")
    def index(self):
        # kw = request.args.get('kw')
        month = request.args.get('month')
        stats,months = dao.revenue_stats_by_time(month=int(month) if month else None)
        stats_book_sold = dao.book_sales_frequency(month=int(month) if month else None)
        print(months)
        return self.render('admin/stats.html', stats=stats,selected_month=month,months=months,stats_book_sold=stats_book_sold)
    

class UserModelView(AdminAuthenticatedView):
    column_list=['id','name','username','email','user_role']
    column_editable_list=['user_role']
    can_create=False


admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(BookModelView(Book, db.session))
admin.add_view(UserModelView(Client,db.session))
admin.add_view(OrderModelView(Order, db.session))
admin.add_view(CancelOrderView(CancelOrder, db.session))
admin.add_view(OrderDetailView(OrderDetail, db.session))
admin.add_view(ReviewView(Review, db.session))
admin.add_view(PriceModelView(Price, db.session))
admin.add_view(TakedBookDetailModelView(TakedBookDetail, db.session))
admin.add_view(AboutUsView(name="Nhập Sách"))
admin.add_view(LogoutView(name="Đăng Xuất"))
admin.add_view(StatsView(name="Báo Cáo"))
admin.add_view(CartView(name="Giỏ Hàng"))