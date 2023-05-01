from main import ma

class ItemSchema(ma.Schema):
    class Meta:
        fields=('id','name','price','description','type','photo','stock','cartegory','vat','photo_2','photo_3')

itemSchema=ItemSchema()
itemsSchema=ItemSchema(many=True)

class BusinessSchema(ma.Schema):
    items=ma.Nested(ItemSchema, many=True)
    class Meta:
        fields=('id','name','username','address','cartegory','phone','photo','pdf_menu','site','active','subscription_type','items_cartegories','items')

businessSchema=BusinessSchema()
businessesSchema=BusinessSchema(many=True)

class CartegorySchema(ma.Schema):
    class Meta:
        fields=('id','name','address_name')
cartegorySchema=CartegorySchema()
cartegoriesSchema=CartegorySchema(many=True)