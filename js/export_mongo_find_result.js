//db.auth('dev', '123456')
db.auth('featrage','feat46660N')  //佰付美2.0
// var c = db.apply_base.find({apply_id: /^APPLY20171106/});
//var c = db.apply_base.find({apply_id: "APPLY20171116104258422656765"});
var c = db.apply_base.find({"data.card_id" : "622628198909150450"})
while(c.hasNext()){
        printjson(c.next());
}