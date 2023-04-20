from main import ma

class ItemSchema(ma.Schema):
    class Meta:
        fields=('id','name','price','description','type','photo','stock','cartegory','photo_2','photo_3')

itemSchema=ItemSchema()
itemsSchema=ItemSchema(many=True)

class BusinessSchema(ma.Schema):
    items=ma.Nested(ItemSchema, many=True)
    class Meta:
        fields=('id','name','username','address','cartegory','phone','photo','pdf_menu','site','subsription','active','items_cartegories','created_at','items')

businessSchema=BusinessSchema()
businessesSchema=BusinessSchema(many=True)