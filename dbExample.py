from models import *

engine = create_engine('sqlite:///this.db')
Base.metadata.create_all(engine)



person = Person(name='maon', age=19, phoneNumber='123456789', birthday='1992-05-15', country='USA', address='123 Main St')
whatsapp1 = WhatsApp(ProfilePic='john_doe1.jpg', aboutStatus='I am on WhatsApp!', phoneNumber='123456789')
person.whastappEntries = [whatsapp1, whatsapp2]


session = Session()
session.add(person)
session.commit()



# Adding profile pictures to a WhatsApp entity
profile_pic1 = ProfilePic(path='pic1.jpg', entity_type='WhatsApp', entity_id=whatsapp_entity.id)
profile_pic2 = ProfilePic(path='pic2.jpg', entity_type='WhatsApp', entity_id=whatsapp_entity.id)
