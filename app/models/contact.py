from app.settings.database import Database
from datetime import datetime

class Contact:
    COLLECTION = 'contacts'

    @staticmethod
    def create_contact(user_id, mobile_phone, email, address, registration_number):
        contacts = Database.get_collection(Contact.COLLECTION)

        # Check if registration number already exists
        if contacts.find_one({'registration_number': registration_number}):
            return None

        contact = {
            'user_id': user_id,
            'mobile_phone': mobile_phone,
            'email': email,
            'address': address,
            'registration_number': registration_number,
            'created_at': datetime.utcnow()
        }

        result = contacts.insert_one(contact)
        return result.inserted_id

    @staticmethod
    def find_by_registration_number(registration_number):
        contacts = Database.get_collection(Contact.COLLECTION)
        return contacts.find_one({'registration_number': registration_number})

    @staticmethod
    def find_all_by_user(user_id):
        contacts = Database.get_collection(Contact.COLLECTION)
        return list(contacts.find({'user_id': user_id}))

    @staticmethod
    def update_contact(registration_number, updates):
        contacts = Database.get_collection(Contact.COLLECTION)
        result = contacts.update_one(
            {'registration_number': registration_number},
            {'$set': updates}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_contact(registration_number):
        contacts = Database.get_collection(Contact.COLLECTION)
        result = contacts.delete_one({'registration_number': registration_number})
        return result.deleted_count > 0
