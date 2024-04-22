import csv
import sys
from datetime import datetime

class Company:
    def __init__(self, name, occupation=None, address=None, web_page=None):
        self.name = name
        self.occupation = occupation
        self.address = address
        self.web_page = web_page

class Phone:
    def __init__(self, mobile_phone_2=None, mobile_phone_3=None, home_phone=None, office_phone=None):
        self.mobile_phone_2 = mobile_phone_2
        self.mobile_phone_3 = mobile_phone_3
        self.home_phone = home_phone
        self.office_phone = office_phone

class Email:
    def __init__(self, private_email_1=None, private_email_2=None, office_email=None):
        self.private_email_1 = private_email_1
        self.private_email_2 = private_email_2
        self.office_email = office_email

class Contact:
    def __init__(self, name, mobile_phone, company, other_phones=None, emails=None, melody=None, other=None, spouse=None, children=None):
        self.name = name
        self.mobile_phone = mobile_phone
        self.company = company
        self.other_phones = other_phones or Phone()
        self.emails = emails or Email()
        self.melody = melody
        self.other = other or Other()
        self.spouse = spouse
        self.children = children or []

    def __str__(self):
        company_info = f"Company: {self.company.name} ({self.company.occupation}), ({self.company.address}), ({self.company.web_page})" if self.company else "Company: None"
        phone_info = f"Mobile Phone: {self.mobile_phone}\nOther Phones: {self.other_phones.mobile_phone_2}, {self.other_phones.mobile_phone_3}, {self.other_phones.home_phone}, {self.other_phones.office_phone}"
        email_info = f"Private Emails: {self.emails.private_email_1}, {self.emails.private_email_2}\nOffice Email: {self.emails.office_email}"
        other_info = f"Address: {self.other.address}\nBirth Day: {self.other.birth_day}\nNotes: {self.other.notes}"
        spouse_info = f"Spouse: {self.spouse.name} (Birthday: {self.spouse.birth_day}, Notes: {self.spouse.notes})" if self.spouse else "Spouse: None"
        children_info = "\n".join(
            [f"Child: {child.name} (Birthday: {child.birth_day}, Notes: {child.notes})" for child in self.children])
        return f"Name: {self.name}\n{company_info}\n{phone_info}\n{email_info}\n{other_info}\n{spouse_info}\n{children_info}"

    def update_contact(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Other:
    def __init__(self, address=None, birth_day=None, notes=None):
        self.address = address
        self.birth_day = birth_day
        self.notes = notes

class Person:
    def __init__(self, name, birth_day=None, notes=None):
        self.name = name
        self.birth_day = birth_day
        self.notes = notes

class ContactBook:
    def __init__(self):
        self.contacts = []
        self.groups = {}

    def add_contact(self, contact):
        self.contacts.append(contact)

    def delete_contact(self, contact):
        self.contacts.remove(contact)

    def search_contact(self, query):
        results = []
        # Search by name
        results.extend([contact for contact in self.contacts if query.lower() in contact.name.lower()])
        # Search by company name
        results.extend(
            [contact for contact in self.contacts if contact.company and query.lower() in contact.company.name.lower()])
        for contact in self.contacts:
            # Check if the contact has other_phones attribute and it's not None
            if contact.other_phones:
                # Check each phone number attribute for the query
                if (contact.mobile_phone and query in contact.mobile_phone) or \
                        (contact.other_phones.mobile_phone_2 and query in contact.other_phones.mobile_phone_2) or \
                        (contact.other_phones.mobile_phone_3 and query in contact.other_phones.mobile_phone_3) or \
                        (contact.other_phones.home_phone and query in contact.other_phones.home_phone) or \
                        (contact.other_phones.office_phone and query in contact.other_phones.office_phone):
                    results.append(contact)
        # Remove duplicates
        results = list(set(results))
        return results

    def import_contacts(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                contact = Contact(
                    name=row['Name'],
                    mobile_phone=row['Mobile phone'],
                    company=Company(row['Company']),
                    other_phones=Phone(
                        mobile_phone_2=row['Mobile phone 2'],
                        mobile_phone_3=row['Mobile phone 3'],
                        home_phone=row['Home phone'],
                        office_phone=row['Office phone']
                    ),
                    emails=Email(
                        private_email_1=row['Private email 1'],
                        private_email_2=row['Private email 2'],
                        office_email=row['Office email']
                    ),
                    melody=row['Melody'],
                    other=Other(
                        address=row['Address'],
                        birth_day=row['Birth day'],
                        notes=row['Notes']
                    ),
                    spouse=Person(
                        name=row["Spouse's Name"],
                        birth_day=row["Spouse's Birthday"],
                        notes=row["Spouse's Notes"]
                    ) if row.get("Spouse's Name") else None,
                    children=[
                        Person(
                            name=row[f"Child {i}'s Name"],
                            birth_day=row[f"Child {i}'s Birthday"],
                            notes=row[f"Child {i}'s Notes"]
                        ) for i in range(1, 4) if row.get(f"Child {i}'s Name")
                    ]
                )
                self.contacts.append(contact)


    def export_contacts(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Name', 'Mobile phone', 'Company', 'Mobile phone 2', 'Mobile phone 3', 'Home phone', 'Office phone', 'Private email 1', 'Private email 2', 'Office email', 'Melody', 'Address', 'Birth day', 'Notes', "Spouse's Name", "Spouse's Birthday", "Spouse's Notes", "Child 1's Name", "Child 1's Birthday", "Child 1's Notes", "Child 2's Name", "Child 2's Birthday", "Child 2's Notes", "Child 3's Name", "Child 3's Birthday", "Child 3's Notes"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                row = {
                    'Name': contact.name,
                    'Mobile phone': contact.mobile_phone,
                    'Company': contact.company.name if contact.company else None,
                    'Mobile phone 2': contact.other_phones.mobile_phone_2,
                    'Mobile phone 3': contact.other_phones.mobile_phone_3,
                    'Home phone': contact.other_phones.home_phone,
                    'Office phone': contact.other_phones.office_phone,
                    'Private email 1': contact.emails.private_email_1,
                    'Private email 2': contact.emails.private_email_2,
                    'Office email': contact.emails.office_email,
                    'Melody': contact.melody,
                    'Address': contact.other.address,
                    'Birth day': contact.other.birth_day,
                    'Notes': contact.other.notes,
                    "Spouse's Name": contact.spouse.name if contact.spouse else None,
                    "Spouse's Birthday": contact.spouse.birth_day if contact.spouse else None,
                    "Spouse's Notes": contact.spouse.notes if contact.spouse else None
                }
                for i, child in enumerate(contact.children, start=1):
                    row[f"Child {i}'s Name"] = child.name
                    row[f"Child {i}'s Birthday"] = child.birth_day
                    row[f"Child {i}'s Notes"] = child.notes
                writer.writerow(row)

    def print_contact_details(self, contact, filename):
        with open(filename, 'w') as file:
            file.write(str(contact))

    def schedule_birthday_reminders(self):
        today = datetime.today()
        for contact in self.contacts:
            if contact.other.birth_day:
                bday = datetime.strptime(contact.other.birth_day, '%Y-%m-%d')
                if (bday - today).days == 10:
                    print(f"Reminder: {contact.name}'s birthday is coming up in 10 days!")

    def edit_contact(self, contact, **kwargs):
        contact.update_contact(**kwargs)
        print("Contact details updated successfully.")

    def create_group(self, group_name):
        self.groups[group_name] = []
        print(f"Group '{group_name}' created successfully.")

    def add_to_group(self, contact, group_name):
        if group_name in self.groups:
            self.groups[group_name].append(contact)
            print(f"Contact added to group '{group_name}' successfully.")
        else:
            print(f"Group '{group_name}' does not exist.")

    def remove_from_group(self, contact, group_name):
        if group_name in self.groups:
            if contact in self.groups[group_name]:
                self.groups[group_name].remove(contact)
                print(f"Contact removed from group '{group_name}' successfully.")
            else:
                print("Contact not found in the group.")
        else:
            print(f"Group '{group_name}' does not exist.")

    def print_contact_list(self, filename):
        with open(filename, 'w') as file:
            for contact in self.contacts:
                file.write(f"Name: {contact.name}\nMobile Phone: {contact.mobile_phone}\nCompany: {contact.company.name if contact.company else None}\n\n")
        print("Contact list printed successfully.")

def help():
    print("Available commands:")
    print("1. add_contact - Add a new contact")
    print("2. delete_contact - Delete a contact")
    print("3. search_contact - Search for a contact")
    print("4. import_contacts - Import contacts from a CSV file")
    print("5. export_contacts - Export contacts to a CSV file")
    print("6. print_contact_details - Print contact details to a text file")
    print("7. schedule_birthday_reminders - Schedule birthday reminders")
    print("8. edit_contact - Edit contact details")
    print("9. create_group - Create a contact group")
    print("10. add_to_group - Add a contact to a group")
    print("11. remove_from_group - Remove a contact from a group")
    print("12. print_contact_list - Print contact list to a text file")
    print("13. exit - exit application")
    print("14. help - Show available commands")

def main():
    contact_book = ContactBook()
    while True:
        command = input("Enter command (type 'help' for available commands): ").strip()
        if command == "add_contact":
            name = input("Enter name: ")
            mobile_phone = input("Enter mobile phone: ")
            company_name = input("Enter company name: ")
            print("If you wish to add more info use the edit contact command")
            contact = Contact(name, mobile_phone, Company(company_name))
            contact_book.add_contact(contact)
        elif command == "delete_contact":
            name = input("Enter the name of the contact you want to delete: ")
            contacts_to_delete = contact_book.search_contact(name)
            if contacts_to_delete:
                for contact in contacts_to_delete:
                    contact_book.delete_contact(contact)
                print("Contact(s) deleted successfully.")
            else:
                print("Contact not found.")
        elif command == "search_contact":
            query = input("Enter the name, phone, company name or part of them to search for: ")
            found_contacts = contact_book.search_contact(query)
            if found_contacts:
                print("Found contacts:")
                for contact in found_contacts:
                    print(f"Name: {contact.name}, Mobile Phone: {contact.mobile_phone}")
            else:
                print("No contacts found matching the query.")
        elif command == "import_contacts":
            filename = input("Enter filename to import: ")
            contact_book.import_contacts(filename)
            print("Contacts imported successfully.")
        elif command == "export_contacts":
            filename = input("Enter filename to export: ")
            contact_book.export_contacts(filename)
        elif command == "print_contact_details":
            name = input("Enter the name of the contact whose details you want to print: ")
            found_contacts = contact_book.search_contact(name)
            if found_contacts:
                filename = input("Enter filename to print contact details: ")
                contact_book.print_contact_details(found_contacts[0], filename)
                print("Contact details printed successfully.")
            else:
                print("Contact not found.")
        elif command == "schedule_birthday_reminders":
            contact_book.schedule_birthday_reminders()
        elif command == "edit_contact":
            name = input("Enter the name of the contact you want to edit: ")
            found_contacts = contact_book.search_contact(name)
            if found_contacts:
                edit_input = input("Enter a key-value pair as in this example: \'name\': \'Ivan\', \'company\': (\'ABC\', \'Manager\'): ")
                try:
                    attribute, value = edit_input.split(":")
                    attribute = attribute.strip()
                    value = value.strip()
                    if '(' in value and ')' in value:
                        value = eval(value)
                    kwargs = {attribute: value}
                    contact_book.edit_contact(found_contacts[0], **kwargs)
                except ValueError:
                    print("Invalid input format. Please provide attribute and new value separated by ':'.")
            else:
                print("Contact not found.")
        elif command == "create_group":
            group_name = input("Enter group name: ")
            contact_book.create_group(group_name)
        elif command == "add_to_group":
            name = input("Enter the name of the contact you want to add to a group: ")
            found_contacts = contact_book.search_contact(name)
            if found_contacts:
                group_name = input("Enter the group name to add the contact to: ")
                contact_book.add_to_group(found_contacts[0], group_name)
            else:
                print("Contact not found.")
        elif command == "remove_from_group":
            name = input("Enter the name of the contact you want to remove from a group: ")
            found_contacts = contact_book.search_contact(name)
            if found_contacts:
                group_name = input("Enter the group name to remove the contact from: ")
                contact_book.remove_from_group(found_contacts[0], group_name)
            else:
                print("Contact not found.")
        elif command == "print_contact_list":
            filename = input("Enter filename to print contact list: ")
            contact_book.print_contact_list(filename)
        elif command == "help":
            help()
        elif command == "exit":
            sys.exit()
        else:
            print("Invalid command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()
