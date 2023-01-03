from flask import *
from database import *
import uuid
user=Blueprint('user',__name__)

@user.route('/uhome')
def uhome():

    return render_template('user_home.html')



   



@user.route('/manageproduct',methods=['get','post'])
def manageproduct():
    data={}
    q="select * from item,category,subcategory where item.cat_id=category.cat_id and item.subcat_id=subcategory.subcat_id and user_id='%s'"%(session['uid'])
    print(q)
    data['proview']=select(q)

    q="select * from category"
    data['cate']=select(q)

    q="select * from subcategory"
    data['subcate']=select(q)
   

    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']

    else:
        action=None

    # if  action=='active':
    #     q="update item set item_status='active' where item_id='%s'"%(id)
    #     update(q)
    #     flash("Item active")
    #     return redirect(url_for('user.manageproduct'))

    # if  action=='inactive':
    #     q="update item set item_status='inactive' where item_id='%s'"%(id)
    #     update(q)
    #     flash("Item inactive")
    #     return redirect(url_for('user.manageproduct'))
    
    if action=='upd':
        q="select * from item,category,subcategory where item.cat_id=category.cat_id and item.subcat_id=subcategory.subcat_id and item_id='%s'"%(id)
        data['upd']=select(q)

    if action=='delete':
        q="delete from item where item_id='%s'"%(id)
        delete(q)
       
        flash("item Deleted")
        return redirect(url_for('user.manageproduct'))

    if 'update' in request.form:
        cat_id=request.form['cat']
        subcat_id=request.form['subcat']
        iname=request.form['iname']
        desc=request.form['desc']
        i=request.files['image']
        img="static/"+str(uuid.uuid4())+i.filename
        i.save(img)
        amt=request.form['amt']
        if i.filename=="":
            q="update item set cat_id='%s',subcat_id='%s',item_name='%s',item_desc='%s',item_amount='%s' where item_id='%s'"%(cat_id,subcat_id,iname,desc,amt,id)
            update(q)
        else:
            q="update item set cat_id='%s',subcat_id='%s',item_name='%s',item_desc='%s',item_amount='%s',item_image='%s' where item_id='%s'"%(cat_id,subcat_id,iname,desc,amt,img,id)
            update(q)
        flash("Item Updated")
        return redirect(url_for('user.manageproduct'))

    if 'add' in request.form:
        cat_id=request.form['cat']
        subcat_id=request.form['subcat']
        iname=request.form['iname']
        desc=request.form['desc']
        i=request.files['image']
        img="static/"+str(uuid.uuid4())+i.filename
        i.save(img)
        amt=request.form['amt']
        
        q="select * from item where item_name='%s'"%(iname)
        res=select(q)
        if res:
           flash("Item Already added")
        else:
            
            q="insert into item values(null,'%s','%s','%s','%s','%s','%s','%s','active')"%(cat_id,subcat_id,session['uid'],iname,desc,img,amt)
            insert(q)
            flash("Item added..")
            return redirect(url_for("user.manageproduct"))

    return render_template('user_manage_product.html',data=data)


@user.route('/manageauction',methods=['get','post'])
def manageauction():
    data={}
    id=request.args['proid']
    data['proid']=id
    data['dummy']=request.args['dummyid']
    # if 'proid' in request.args:
    #     id=request.args['proid']
    #     q="select * from auction where item_id='%s'"%(id)
    #     res=select(q)
    #     if res:
    #         data['res']=1
    #         flash("Item Already Added To Auction")
          



    if 'add' in request.form:
        
        
        stime=request.form['stime']
        sdate=request.form['sdate']
        samount=request.form['samt']
        q="insert into auction values(null,'%s','%s','%s','%s','pending')"%(id,stime,sdate,samount)
        insert(q)
        q="update item set item_status='Added to auction' where item_id='%s'"%(id)
        update(q)
        flash("Item Added To auction")
        return redirect(url_for('user.manageproduct'))


    if 'action' in request.args:
        id=request.args['proid']
        dummy=request.args['dummyid']
        amount=request.args['amount']
        action=request.args['action']
        aid=request.args['aid']
    else:
        action=None

    if action=="start":
        q="update auction set auction_status='start' where auction_id='%s'"%(aid)
        update(q)
        q="insert into bid values(null,'%s','%s',now(),'%s','bid')"%(aid,session['uid'],amount)
        insert(q)
        flash("Auction Started")
        return redirect(url_for('user.manageauction',proid=id,dummyid=dummy)) 

    if action=="stop":
        q="update auction set auction_status='stop' where auction_id='%s'"%(aid)
        update(q)
        q="UPDATE bid SET bid_status='winner' WHERE auction_id='%s' ORDER BY bid_amount DESC LIMIT 1"%(aid)
        update(q)
        flash("Auction Stoped, Winner Selected")
        return redirect(url_for('user.manageauction',proid=id,dummyid=dummy)) 

          
    q="SELECT * FROM `auction`,item,category,subcategory WHERE auction.item_id=item.item_id and item.cat_id=category.cat_id and item.subcat_id=subcategory.subcat_id AND auction.item_id='%s'"%(id)
    data['view']=select(q)
    return render_template('user_manage_auction.html',data=data)


@user.route('/viewbid')
def viewbid():
    data={}
    id=request.args['aid']
    q="SELECT * FROM `bid`,`auction`,`user`,item WHERE bid.auction_id=`auction`.auction_id AND bid.bidder_id=user.user_id AND auction.item_id=item.item_id and bid.auction_id='%s' order by bid_amount desc "%(id)

    data['viewbid']=select(q)
    return render_template('user_view_bid.html',data=data)



@user.route('/viewwinners')
def viewwinners():
    data={}
    id=request.args['bid']
    q="SELECT * FROM `bid`,`auction`,`user`,item WHERE bid.auction_id=`auction`.auction_id AND bid.bidder_id=user.user_id AND auction.item_id=item.item_id and bid.bid_id='%s' order by bid_amount desc   limit 1"%(id)

    data['vieweinner']=select(q)

    return render_template('user_view_winner_details.html',data=data)




@user.route('/viewpayments')
def viewpayments():
    data={}
    id=request.args['bid']
    q="SELECT * FROM payment,card,`user`,bid WHERE payment.card_id=card.card_id AND card.user_id=user.user_id AND payment.bid_id=bid.bid_id AND payment.bid_id='%s'"%(id)
    print(q)
    print(q)
    data['viewpay']=select(q)

    return render_template('user_view_payments.html',data=data)


@user.route('/assignorder',methods=['get','post'])
def assignorder():
    data={}
    id=request.args['bid']
    q="select * from courier"
    data['cour']=select(q)
    q="SELECT * FROM delivery,bid,`user`,courier WHERE `delivery`.`bid_id`=`bid`.bid_id AND bid.bidder_id=user.user_id AND delivery.courier_id=courier.courier_id and bid.bid_id='%s'"%(id)
    data['delivery']=select(q)
    
    if 'add' in request.form:
        q="select * from delivery where bid_id='%s'"%(id)
        res=select(q)
        if res:
            flash('Delivery already Assigned ')
            return redirect(url_for('user.assignorder',bid=id))
        else:

            id=request.args['bid']
            cour=request.form['cour']
            ddate=request.form['ddate']
            dtime=request.form['dtime']
            q="insert into delivery values(null,'%s','%s','%s','%s','shipped')"%(id,cour,ddate,dtime)
            insert(q)
            flash('Delivery Assigned successfully')
            return redirect(url_for('user.assignorder',bid=id))
    return render_template('user_assign_order.html',data=data)


@user.route('/otherauction')
def otherauction():
    data={}

    q="SELECT * FROM `auction`,item,category,subcategory WHERE auction.item_id=item.item_id and item.cat_id=category.cat_id and item.subcat_id=subcategory.subcat_id AND auction_status='start'"
    print(q)
    data['viewother']=select(q)
    return render_template('user_view_other_auctions.html',data=data)



@user.route('/makebids',methods=['get','post'])
def makebids():
    data={}
    id=request.args['aid']
    q="SELECT * FROM `bid`,`auction`,`user`,item WHERE bid.auction_id=`auction`.auction_id AND bid.bidder_id=user.user_id AND auction.item_id=item.item_id and bid.auction_id='%s' order by bid_amount desc "%(id)
    res=select(q)
    data['makebid']=res
    data['amount']=res[0]['bid_amount']

    if 'bid' in request.form:
        bamt=request.form['bamt']
        q="insert into bid values(null,'%s','%s',now(),'%s','bid')"%(id,session['uid'],bamt)
        insert(q)
        flash("Bid Added Successfully..")
        return redirect(url_for("user.makebids",aid=id))
    
    return render_template('user_make_bid.html',data=data)

@user.route('/makepayment',methods=['get','post'])
def makepayment():
    data={}
    bid=request.args['bid']
    amount=request.args['amount']
    username=request.args['username']
    data['total']=amount
    data['username']=username

    if 'pay' in request.form:
        username=request.form['username']
        total=request.form['total']
        cno=request.form['cno']
        exp=request.form['exp']
        cvv=request.form['cvv']
        q="insert into card values(null,'%s','%s','visa,'%s')"%(session['uid'],cno,exp,)
        id=insert(q)
        q="insert into payment values (null,'%s','%s',curdate(),'paid')"%(id,bid)
        insert(q)
        flash("payment succesfull")
        return redirect(url_for('user.uhome'))

    return render_template('user_make_payment.html',data=data)