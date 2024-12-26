from flask import redirect, url_for, render_template_string, request
from markupsafe import Markup
from flask_admin import Admin,BaseView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func
from config import app, db
from flask_admin.actions import action
from models import Order, CancelOrder, Book, InfoUserOrder, CancelReasonState,OrderDetail, Receipt, ReceiptDetail, Client, StateOrder


em_admin = Admin(app,'Employee Site',template_mode='bootstrap4', url='/em', endpoint='em',base_template='employee/em_base.html')


class EmployeeAuthenticatedView(ModelView):
    pass


class OrderAttachedUserModelView(EmployeeAuthenticatedView):
    column_list=['id','state','name','phone','delivery_adr','email',
                 'method_bank','method_receive']
    
    def get_query(self):
        return db.session.query(Order.id,
                                Order.state,
                                InfoUserOrder.name.label('name'), 
                                InfoUserOrder.phone.label('phone'), 
                                Order.delivery_address.label('delivery_adr'), 
                                Order.methodReceive,
                                InfoUserOrder.email.label('email'), 
                                Order.methodBank.label('method_bank'),
                                Order.methodReceive.label('method_receive'))\
                                .join(InfoUserOrder,InfoUserOrder.id==Order.info_user_order_id)
    

# @app.route('/user_action/<int:user_id>')
# def user_action(user_id):
#     print(f"User ID: {user_id}")
#     print(request.url_rule)
#     args = request.args.get('search')
#     print(args)
#     return redirect('/em/em_users/?search=user')  # Quay lại trang danh sách


class CancelPendingOrderModelView(EmployeeAuthenticatedView):
    column_list=['id','order_id','reason','reason_state',
                 'order_state','phone','name','email',
                 'method_bank','method_receive','test']
    column_details_list=['id','order_id','reason','reason_state',
                 'order_state','phone','name','email',
                 'method_bank','method_receive','detail_quantity']
    can_view_details = True
    details_modal=True
    edit_modal=True
    list_template='employee/em_list.html'

    column_formatters = {
        'test': lambda v, c, m, p: Markup(f'<a onclick="confirmPendingCancel({m.id})" class="btn btn-primary btn-sm">X</a>')
    }
    # <a onclick="confirmPendingCancel({{ cancel_order_id }})" class="btn btn-primary btn-sm">X</a>
    # column_formatters = {
    #     'test': lambda v, c, m, p: Markup(f'<a href="/user_action/{m.id}" class="btn btn-primary btn-sm">Action</a>')
    # }


    
    def get_query(self):
        return db.session.query(CancelOrder.id,
                                Order.id.label('order_id'),
                                CancelOrder.reason,
                                CancelOrder.reason_state,
                                Order.state.label('order_state'),
                                InfoUserOrder.phone.label('phone'),
                                InfoUserOrder.name.label('name'),
                                InfoUserOrder.email.label('email'),
                                Order.methodBank.label('method_bank'),
                                Order.methodReceive.label('method_receive'),
                                OrderDetail.quantity.label('detail_quantity')
                                )\
                                .join(Order,CancelOrder.order_id==Order.id)\
                                .join(InfoUserOrder,InfoUserOrder.id==Order.info_user_order_id)\
                                .filter(CancelOrder.reason_state==CancelReasonState.PENDINGCANCEL)
    # db.session.query(CancelOrder)
        #not execute show details
    

class CancelOrderModelView(EmployeeAuthenticatedView):
    column_list = ['id','order_id','reason','reason_state']
    column_editable_list = ['reason']


class UserModelView(EmployeeAuthenticatedView):
    column_list=['id','name','username','email','user_role']
    column_editable_list=['user_role']
    can_create=False
    column_filters = ['id','name']
    column_searchable_list = ['name','id']
    # list_template = 'employee/test_list.html'

    # column_formatters = {
    #     'test': lambda v, c, m, p: render_template_string(
    #         '<a href="{{ url_for("user_action", user_id=m.id) }}" class="btn btn-primary btn-sm">Action</a>',
    #         m=m  # Truyền đối tượng m vào template
    #     )
    # }
    

    # Định nghĩa hành động
    @action('custom_action', 'Custom Action', 'Are you sure?')
    def custom_action(self, ids):
        for user_id in ids:
            print(f"Custom action for user ID: {user_id}")
        # Thực hiện hành động nào đó




class ReceiptModelView(EmployeeAuthenticatedView):
    column_list = ['id','client_id','receipts_detail','is_pay']

    # column_select_related_list = ['client_id']
    

    #issue now: detail custom, and how to custom for field & button for bar

class ReceiptDetailModelView(EmployeeAuthenticatedView):
    column_list = ['id','quantity','price','receipt_id','book_id']



em_admin.add_view(OrderAttachedUserModelView(Order,db.session,name="Orders",endpoint='em_orders'))
em_admin.add_view(CancelPendingOrderModelView(CancelOrder,db.session,name='CancelPendingOrder',endpoint='em_pending_cancels'))
em_admin.add_view(CancelOrderModelView(CancelOrder,db.session,name='CancelOrder',endpoint='em_cancels'))
em_admin.add_view(UserModelView(Client,db.session,endpoint='em_users'))
em_admin.add_view(ReceiptModelView(Receipt,db.session,endpoint='em_receipts'))
em_admin.add_view(ReceiptDetailModelView(ReceiptDetail,db.session,endpoint='em_receipt_detail'))