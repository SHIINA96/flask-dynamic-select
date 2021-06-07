from app import app
from flask import Flask, render_template, request, jsonify
from app.models import Storage
from app.forms import Form


@app.route('/outbound', methods=['GET', 'POST'])
def outbound():
    form = Form()
    form.location.choices = ['---', '木星', '地球']
 
    if request.method == 'POST':
        location = Storage.query.filter_by(location=form.location.data).first()
        size = Storage.query.filter_by(size=form.size.data).first()
        item = Storage.query.filter_by(item=form.item.data).first()
        quantity = Storage.query.filter_by(quantity=form.quantity.data).first()
        return '<h1>地点 : {}, 规格: {}, 物品: {}, 数量: {}</h1>'.format(location.location, size.size, item.item, quantity.quantity)
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
    # 将 List 转为 JSON 并添加 id
    sizeArray.insert(0,'--')
    global itemLocation
    itemLocation = get_size
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
    maxQuantity = item_data[0].quantity
    
    maxQuantityArray =[]
    for i in range(0, maxQuantity+1):
        maxQuantityArray.append(i)

    quantityArray =[]
    for i in maxQuantityArray:
        quantityObj = {}
        quantityObj['item'] = item_data[0].item
        quantityObj['quantity'] = maxQuantityArray.index(i)
        quantityArray.append(quantityObj)
    return jsonify({'quantityList' : quantityArray})