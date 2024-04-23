from datetime import datetime, timedelta
from sqlalchemy import cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from src.dto.contact import ContactSchema, ContactUpdateSchema
from src.models.model import Contact, User


async def create_contact(data: ContactSchema, db: AsyncSession, user: User):
    contact = Contact(**data.model_dump(exclude_unset=True),user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def get_contact_by_name(name: str, db: AsyncSession):
    """
    The get_contact_by_name function returns a contact object from the database.
    
    :param name: str: Filter the database for a contact with that name
    :param db: AsyncSession: Pass in the database session to the function
    :return: A single contact
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(name=name)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user

async def get_contact_by_last_name(last_name: str, db: AsyncSession):
    """
    The get_contact_by_last_name function returns a contact object from the database based on the last name of that contact.
        Args:
            last_name (str): The last name of the user to be retrieved.
            db (AsyncSession): An async session for interacting with an SQLAlchemy database.
        Returns:
            Contact: A single Contact object matching the provided first and last names, or None if no such user exists.
    
    :param last_name: str: Filter the query by last name
    :param db: AsyncSession: Pass in the database session
    :return: A contact object
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(last_name=last_name)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def get_contact_by_email(email: str, db: AsyncSession):
    """
    The get_contact_by_email function returns a contact object from the database based on the email address provided.
        Args:
            email (str): The email address of the contact to be retrieved.
            db (AsyncSession): An async session for interacting with an SQLAlchemy database.
    
    :param email: str: Filter the database query
    :param db: AsyncSession: Pass the database session to the function
    :return: A single contact by email
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def get_contact(id: int, db:AsyncSession):
    """
    The get_contact function returns a contact object from the database.
        Args:
            id (int): The ID of the contact to be retrieved.
            db (AsyncSession): An async session for interacting with the database.
        Returns:
            Contact: A single Contact object matching the provided ID.
    
    :param id: int: Specify the id of the contact to be returned
    :param db:AsyncSession: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=id)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def get_contacts(db: AsyncSession):
    """
    The get_contacts function returns a list of all contacts in the database.
        :return: A list of dictionaries containing contact information.
    
    
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of contact objects
    :doc-author: Trelent
    """
    stmt = select(Contact)
    users = await db.execute(stmt)
    return users.scalars().all()


async def update_contact(id: int, data: ContactUpdateSchema, db: AsyncSession, user: User):
    """
    The update_contact function updates a contact in the database.
    
    :param id: int: Identify the contact to be updated
    :param data: ContactUpdateSchema: Pass the data that is being updated
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user from the request
    :return: The contact object
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = data.name
        contact.last_name = data.last_name
        contact.email = data.email
        contact.phone = data.phone
        contact.birthday = data.birthday
        await db.commit()
        await db.refresh(contact)
    return contact

async def delete_contact(id: int, db: AsyncSession, user: User):
    """
    The delete_contact function deletes a contact from the database.
    
    :param id: int: Specify the id of the contact to be deleted
    :param db: AsyncSession: Pass in the database session
    :param user: User: Check if the user is authorized to delete the contact
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(id=id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact

async def birthday_seven(db: AsyncSession):
    """
    The birthday_seven function returns a list of users with birthdays in the next 7 days.
    
    :param db: AsyncSession: Pass the database session into the function
    :return: A list of users with birthdays in the next 7 days
    :doc-author: Trelent
    """
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    users = await db.execute(
        select(Contact).filter(
            cast(Contact.birthday, Date) >= today,
            cast(Contact.birthday, Date) <= next_week
        )
    )
    users = users.scalars().all()
    if not users:
        return {"message": "No users with birthdays in the next 7 days"}
    return users

