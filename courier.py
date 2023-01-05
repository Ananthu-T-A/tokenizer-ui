from flask import *
from database import *

courier=Blueprint('courier',__name__)

@courier.route('/chome')
def chome():

    return render_template("courier_home.html")

@courier.route('/viewdelivery')
def viewdelivery():
    data={}
    q="SELECT * FROM delivery d,bid b,`user` u WHERE d.bid_id=b.bid_id AND b.bidder_id=u.user_id AND courier_id='%s'"%(session['cid'])
    data['delivery']=select(q)

    if 'id' in request.args:
        id=request.args['id']
        q="update delivery set delivery_status='Delivered' where delivery_id='%s'"%(id)
        update(q)
        flash("Product Delivered successfully...")
        return redirect(url_for('courier.viewdelivery'))
    return render_template('courier_view_assign_orders.html',data=data)