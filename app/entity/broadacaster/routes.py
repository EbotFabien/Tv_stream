from flask import render_template, url_for,flash,redirect,request,abort,Blueprint
from app.Models import User,subscription,live_ession
from app.entity.broadacaster.forms import sessionForm
from app import db,login_manager
from flask_login import login_user,current_user,logout_user,login_required
from sqlalchemy import or_, and_, distinct, func




broadacast =Blueprint('broadacast',__name__)

@broadacast.route('/broadacast/subscribe/<id>/',methods=['GET','POST'])
def subscribe(id):
    
    jo=subscription.query.filter(and_(subscription.broadcaster_id==id,subscription.client_id==current_user.id)).first()
    if jo:
        flash(f'User  already exists','success')
        return redirect(url_for('users.dashboard'))
    else:
        sub=subscription(broadcaster_id=id,client_id=current_user.id)
        db.session.add(sub)
        db.session.commit()

    flash(f'You have suceesfully Subscribed ','success')
    return redirect(url_for('users.dashboard'))

@broadacast.route('/broadacast/create/<id>',methods=['GET','POST'])
def create(id):
    form=sessionForm()
    if form.validate_on_submit():
        sub=live_ession(broadcaster_id=id,Title=form.title.data,key=form.key.data)
        db.session.add(sub)
        db.session.commit()
        return redirect(url_for('broadacast.singlelives',id=id))
    return render_template('create_session.html',legend="single",form=form)

@broadacast.route('/broadacast/single/lives/<id>',methods=['GET','POST'])
def singlelives(id):
    
    lives=live_ession.query.filter_by(broadcaster_id=id).all()

    return render_template('single_session.html',legend="single",lives=lives,ide=id)

@broadacast.route('/broadacast/lives',methods=['GET','POST'])
def alllives():
    
    lives=live_ession.query.all()

    return render_template('all_session.html',legend="single",lives=lives)

@broadacast.route('/broadacast/session/<id>',methods=['GET','POST'])
def session(id):
    sess=live_ession.query.filter_by(id=id).first()
    lives=live_ession.query.filter_by(status=True).all()
    url='http://104.238.191.159:8088/hls/'+sess.key+'.m3u8'

    return render_template('live.html',lives=lives,session=sess,url=url)


@broadacast.route('/broadacast/stop/<id>',methods=['GET','POST'])
def stop(id):
    sess=live_ession.query.filter_by(id=id).first()
    sess.status=False
    db.session.commit()

   

    return redirect(url_for('broadacast.singlelives',id=id))