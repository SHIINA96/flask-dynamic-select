from app import app
from flask import Flask, render_template, request, jsonify
from app.models import Storage, User, db
from app.forms import Form
import math

@app.route('/outbound', methods=['GET', 'POST'])
def outbound():
    form = Form()
    form.location.choices = ['---', '金星', '水星', '火星', '木星', '土星', '地球', '仓库']
 
    if request.method == 'POST':
        location = Storage.query.filter_by(location=form.location.data).first()
        size = Storage.query.filter_by(size=form.size.data).first()
        item = Storage.query.filter_by(item=form.item.data).first()
        # quantity = Storage.query.filter_by(quantity=form.quantity.data).first()
        quantity = form.quantity.data

        totalQuantity = Storage.query.filter_by(item=form.item.data, size=form.size.data, location=form.location.data).all()
        totalQuantity = totalQuantity[0].quantity
        quantity = totalQuantity - quantity

        update = Storage.query.filter_by(item=form.item.data, size=form.size.data, location=form.location.data).first()
        update.quantity = quantity
        db.session.commit()

        # return '<h1>地点 : {}, 规格: {}, 物品: {}, 数量: {}</h1>'.format(location.location, size.size, item.item, quantity)
    return render_template('outbound.html', form=form)
 
@app.route('/size/<get_size>')
def sizebylocation(get_size):
    # 从 jQuery 中获取选项 size， 并从数据库中查找数据
    # size = Storage.query.filter_by(location=get_size).all()
    # 只获取 size 中不重复的项
    size = Storage.query.with_entities(Storage.size).filter_by(location=get_size).distinct().all()
    #  创建新的 List 存储从数据库中获取的数据
    sizeArray = []
    for item in size:
        sizeObj = {}
        # sizeObj['id'] = item.id
        sizeObj['size'] = item.size
        sizeArray.append(sizeObj)
    # 将 List 转为 JSON 并添加 id
    sizeArray.insert(0,'--')
    global itemLocation
    itemLocation = get_size
    return jsonify({'sizelocation' : sizeArray})
  
@app.route('/item/<get_item>')
def item(get_item):
    size_data = Storage.query.filter_by(size=get_item, location=itemLocation).all()
    itemArray = []
    for item in size_data:
        itemObj = {}
        itemObj['size'] = item.size
        itemObj['item'] = item.item
        itemArray.append(itemObj)
    itemArray.insert(0,'--')
    global itemSize
    itemSize = get_item
    return jsonify({'itemList' : itemArray})

# @app.route('/quantity/<get_quantity>')
# def quantity(get_quantity):
#     item_data = Storage.query.filter_by(item=get_quantity, size=itemSize, location=itemLocation).all()
#     quantityArray = []
#     for quantity in item_data:
#         quantityObj = {}
#         quantityObj['item'] = quantity.item
#         quantityObj['quantity'] = quantity.quantity
#         quantityArray.append(quantityObj)
#     quantityArray.insert(0,'--')
#     return jsonify({'quantityList' : quantityArray})

    
@app.route('/quantity/<get_quantity>')
def quantity(get_quantity):
    item_data = Storage.query.filter_by(item=get_quantity, size=itemSize, location=itemLocation).all()
    quantityArray =[]
    for i in range(0, math.ceil(item_data[0].quantity)+1): # 物品数量出现小数时会向上取整
        quantityObj = {}
        quantityObj['item'] = item_data[0].item
        quantityObj['quantity'] = i
        quantityArray.append(quantityObj)
    return jsonify({'quantityList' : quantityArray})