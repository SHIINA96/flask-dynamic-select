from app import app
from flask import Flask, render_template, request, jsonify, json
from app.models import Storage
from app.forms import Form
from urllib.parse import unquote

@app.route('/outbound', methods=['GET', 'POST'])
def outbound():
    form = Form()
    form.location.choices = ['木星', '地球']
 
    if request.method == 'POST':
        location = Storage.query.filter_by(location=form.location.data).first()
        size = Storage.query.filter_by(size=form.size.data).first()
        item = Storage.query.filter_by(item=form.item.data).first()
        return '<h1>地点 : {}, 规格: {}, 物品: {}</h1>'.format(location.location, size.size, item.item)
    return render_template('outbound.html', form=form)
 
@app.route('/size/<get_size>')
def sizebylocation(get_size):
    # 从 jQuery 中获取选项 size， 并从数据库中查找数据
    size = Storage.query.filter_by(location=get_size).all()
    #  创建新的 List 存储从数据库中获取的数据
    sizeArray = []
    for item in size:
        sizeObj = {}
        sizeObj['id'] = item.id
        sizeObj['size'] = item.size
        sizeArray.append(sizeObj)
        sizeArray.insert(0,'--')
    # 将 List 转为 JSON 并添加 id
    return jsonify({'sizelocation' : sizeArray})
  
@app.route('/item/<get_item>')
def item(get_item):
    size_data = Storage.query.filter_by(size=get_item).all()
    itemArray = []
    for item in size_data:
        itemObj = {}
        itemObj['size'] = item.size
        itemObj['item'] = item.item
        itemArray.append(itemObj)
        itemArray.insert(0,'--')
    return jsonify({'itemList' : itemArray})

@app.route('/quantity/<get_quantity>')
def quantity(get_quantity):
    item_data = Storage.query.filter_by(item=get_quantity).all()
    quantityArray = []
    for quantity in item_data:
        quantityObj = {}
        quantityObj['item'] = quantity.item
        quantityObj['quantity'] = quantity.quantity
        quantity.append(quantityObj)
        quantityArray.insert(0,'--')
    return jsonify({'quantityList' : quantityArray})