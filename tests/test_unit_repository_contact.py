import unittest
from unittest.mock import MagicMock, AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.model import Contact, User
from src.dto.contact import ContactSchema, ContactUpdateSchema
from src.repository.contact import get_contact, get_contacts, create_contact, update_contact, delete_contact


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        contacts = [Contact(id=1, name='test_name_1', last_name='test_l_name_1',email='test_email_1',phone='test_phone_1',birthday='test_birthday_1')]
        mocked_contact = Mock()
        mocked_contact.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contact
        result = await get_contacts(self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = [Contact(id=1, name='test_name_1', last_name='test_l_name_1',email='test_email_1',phone='test_phone_1',birthday='test_birthday_1', user=self.user)]
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(1, self.session)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        contact = ContactSchema(name='test_name_1', last_name='test_l_name_1',email='bot@gmail.com',phone=1234567890,birthday='test_birthday_1')
        result = await create_contact(contact, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, contact.name)
        self.assertEqual(result.last_name, contact.last_name)
        self.assertEqual(result.email, contact.email)
        self.assertEqual(result.phone, contact.phone)
        self.assertEqual(result.birthday, contact.birthday)



    async def test_update_contact(self):
        contact = ContactUpdateSchema(name='test_name', last_name='test_l_name', email='bot@gmail.com', phone=1234567890, birthday='test_birthday')
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, name='test_name', last_name='test_l_name', email='bot@gmail.com', phone=1234567890, birthday='test_birthday',
                                                                  user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, contact, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.name, contact.name)
        self.assertEqual(result.last_name, contact.last_name)
        self.assertEqual(result.email, contact.email)
        self.assertEqual(result.phone, contact.phone)
        self.assertEqual(result.birthday, contact.birthday)

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, name='test_name', last_name='test_l_name', email='bot@gmail.com', phone=1234567890, birthday='test_birthday',
                                                                  user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Contact)
