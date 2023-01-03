from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adhome')
def adhome():

    return render_template("admin_home.html")

@admin.route('/managecat',methods=['get','post'])
def managecat():
    data={}
    q="select * from category"
    data['catview']=select(q)

    if 'add' in request.form:
        cat=request.form['cat']
        desc=request.form['desc']
        q="insert into category values(null,'%s','%s','active')"%(cat,desc)
        insert(q)
        flash("Category added..")
        return redirect(url_for("admin.managecat"))

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']

    else:
        action=None

    if  action=='active':
        q="update category set cat_status='active' where cat_id='%s'"%(id)
        update(q)
        flash("Category active")
        return redirect(url_for('admin.managecat'))

    if  action=='inactive':
        q="update category set cat_status='inactive' where cat_id='%s'"%(id)
        update(q)
        flash("Category inactive")
        return redirect(url_for('admin.managecat'))
    
    if action=='upd':
        q="select * from category where cat_id='%s'"%(id)
        data['upd']=select(q)

    if action=='delete':
        q="delete from category where cat_id='%s'"%(id)
        delete(q)
        flash("Category Deleted")
        return redirect(url_for('admin.managecat'))

    if 'update' in request.form:
        cat=request.form['cat']
        desc=request.form['desc']
        q="update category set cat_name='%s',cat_desc='%s' where cat_id='%s'"%(cat,desc,id)
        update(q)
        flash("Category Updated")
        return redirect(url_for('admin.managecat'))
    return render_template('admin_manage_category.html',data=data)



@admin.route('/managesubcat',methods=['get','post'])
def managesubcat():
    data={}
    q="select * from subcategory"
    data['subcat']=select(q)

    if 'add' in request.form:
        cat=request.form['subcat']
        desc=request.form['desc']
        q="insert into subcategory values(null,'%s','%s','active')"%(cat,desc)
        insert(q)
        flash("SubCategory added..")
        return redirect(url_for("admin.managesubcat"))

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']

    else:
        action=None

    if  action=='active':
        q="update subcategory set subcat_status='active' where subcat_id='%s'"%(id)
        update(q)
        flash("SubCategory active")
        return redirect(url_for('admin.managesubcat'))

    if  action=='inactive':
        q="update subcategory set subcat_status='inactive' where subcat_id='%s'"%(id)
        update(q)
        flash("SuubCategory inactive")
        return redirect(url_for('admin.managesubcat'))
    
    if action=='upd':
        q="select * from subcategory where subcat_id='%s'"%(id)
        data['upd']=select(q)

    if action=='delete':
        q="delete from subcategory where subcat_id='%s'"%(id)
        delete(q)
        flash("SuubCategory Deleted")
        return redirect(url_for('admin.managesubcat'))

    if 'update' in request.form:
        cat=request.form['subcat']
        desc=request.form['desc']
        q="update subcategory set subcat_name='%s',subcat_desc='%s' where subcat_id='%s'"%(cat,desc,id)
        update(q)
        flash("SuubCategory Updated")
        return redirect(url_for('admin.managesubcat'))
    return render_template('admin_manage_subcat.html',data=data)



@admin.route('/viewuser')
def viewuser():
    data={}
    q="select * from user"
    data['users']=select(q)
    return render_template('admin_view_user.html',data=data)



@admin.route('/managecour',methods=['get','post'])
def managecour():
    data={}
    q="select * from courier"
    data['catview']=select(q)

   

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']

    else:
        action=None

    if  action=='active':
        q="update courier set cour_status='active' where courier_id='%s'"%(id)
        update(q)
        flash("courier active")
        return redirect(url_for('admin.managecour'))

    if  action=='inactive':
        q="update courier set cour_status='inactive' where courier_id='%s'"%(id)
        update(q)
        flash("Courier inactive")
        return redirect(url_for('admin.managecour'))
    
    if action=='upd':
        q="select * from courier where courier_id='%s'"%(id)
        data['upd']=select(q)

    if action=='delete':
        q="delete from courier where courier_id='%s'"%(id)
        delete(q)
        q="delete from login where username=(select username from user where user_id='%s')"%(id)
        delete(q)
        flash("Courier Deleted")
        return redirect(url_for('admin.managecour'))

    if 'update' in request.form:
        cname=request.form['cname']
        phone=request.form['phone']
        add=request.form['add']
        dist=request.form['dist']
        state=request.form['state']
        pin=request.form['pin']
        q="update courier set cour_name='%s',cour_phone='%s',cour_address='%s',cour_district='%s',cour_state='%s',cour_pin='%s' where courier_id='%s'"%(cname,phone,add,dist,state,pin,id)
        update(q)
        flash("Courier Updated")
        return redirect(url_for('admin.managecour'))

    if 'add' in request.form:
        cname=request.form['cname']
        phone=request.form['phone']
        add=request.form['add']
        dist=request.form['dist']
        state=request.form['state']
        pin=request.form['pin']
        uname=request.form['uname']
        pwd=request.form['pwd']
        q="select * from login where username='%s'"%(uname)
        res=select(q)
        if res:
           data['warning']="Username Already Exist"
        else:
            q="insert into login values('%s','%s','courier','active')"%(uname,pwd)
            id=insert(q)
            q="insert into courier values(null,'%s','%s','%s','%s','%s','%s','%s','active')"%(uname,cname,phone,add,dist,state,pin)
            insert(q)
            flash("Courier added..")
            return redirect(url_for("admin.managecour"))

    return render_template('admin_manage_courier.html',data=data)



@admin.route('/viewauction')
def viewauction():
    data={}

    q="SELECT * FROM `auction`,item,category,subcategory WHERE auction.item_id=item.item_id and item.cat_id=category.cat_id and item.subcat_id=subcategory.subcat_id AND auction_status='start'"

    data['view']=select(q)
    return render_template('admin_view_auction.html',data=data)

@admin.route('/viewwinner')
def viewwinner():
    data={}
    id=request.args['aid']
    q="SELECT * FROM `bid`,`auction`,`user`,item WHERE bid.auction_id=`auction`.auction_id AND bid.bidder_id=user.user_id AND auction.item_id=item.item_id and bid.auction_id='%s' order by bid_amount desc   limit 1"%(id)

    data['vieweinner']=select(q)

    return render_template('admin_view_winner.html',data=data)



@admin.route('/viewpayment')
def viewpayment():
    data={}
    id=request.args['bid']
    q="SELECT * FROM payment,card,`user`,bid WHERE payment.card_id=card.card_id AND card.user_id=user.user_id AND payment.bid_id=bid.bid_id AND payment.bid_id='%s'"%(id)
    print(q)
    print(q)
    data['viewpay']=select(q)

    return render_template('admin_view_payment.html',data=data)



@admin.route('/viewbids')
def viewbids():
    data={}
    id=request.args['aid']
    q="SELECT * FROM `bid`,`auction`,`user`,item WHERE bid.auction_id=`auction`.auction_id AND bid.bidder_id=user.user_id AND auction.item_id=item.item_id and bid.auction_id='%s' order by bid_amount desc "%(id)

    data['viewbid']=select(q)
    return render_template('admin_view_bid.html',data=data)