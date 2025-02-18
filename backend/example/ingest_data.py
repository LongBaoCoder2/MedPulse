from enum import Enum
from uuid import uuid4

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

# Assuming models have been imported
from qllm.models.base import Base
from qllm.models.model import (
    Conversation,
    Document,
    MedicalRecord,
    Message,
    MessageRoleEnum,
    MessageStatusEnum,
    User,
)

# Initialize Faker
fake = Faker()


# Enum helper
class MockEnum(Enum):
    @classmethod
    def random(cls):
        return fake.random_element(cls)


# Mock Data Functions
def create_mock_user(dev: bool = False):
    id = "ea7aaab2-ca20-4a95-a190-df99c4c5d72a" if dev else uuid4()

    return User(
        id=id,
        name=fake.name(),
        email=fake.unique.email(),
        password_hash=fake.sha256(),
        age=fake.random_int(min=18, max=80),
        gender=fake.random_element(["Male", "Female", "Other"]),
    )


def create_mock_conversation(user_id):
    return Conversation(
        id=uuid4(),
        title=fake.sentence(nb_words=5),
        user_id=user_id,
        document_id=uuid4(),
    )


def create_mock_message(conversation_id):
    return Message(
        id=uuid4(),
        conversation_id=conversation_id,
        content=fake.text(max_nb_chars=200),
        role=fake.random_element(MessageRoleEnum),
        status=fake.random_element(MessageStatusEnum),
    )


def create_mock_document():
    return Document(
        id=uuid4(),
        url=fake.url(),
        metadata_map={"key": fake.word()},
    )


def create_mock_medical_record(user_id):
    return MedicalRecord(
        id=uuid4(),
        user_id=user_id,
        file_name=fake.file_name(extension="pdf"),
        file_path=fake.file_path(depth=3, category=None),
        description=fake.sentence(nb_words=10),
    )


# Bulk Data Generator
def generate_mock_data(session: Session, num_users=10):  # type: ignore
    is_dev = True
    try:
        for _ in range(num_users):
            user = create_mock_user(is_dev)
            if is_dev:
                is_dev = False

            session.add(user)
            session.flush()

            for _ in range(fake.random_int(min=1, max=3)):
                conversation = create_mock_conversation(user_id=user.id)
                session.add(conversation)
                session.flush()

                for _ in range(fake.random_int(min=1, max=5)):
                    message = create_mock_message(conversation_id=conversation.id)
                    session.add(message)

            for _ in range(fake.random_int(min=1, max=2)):
                medical_record = create_mock_medical_record(user_id=user.id)
                session.add(medical_record)

        session.commit()
        print("Mock data generated successfully.")
    except IntegrityError as e:
        session.rollback()
        print(f"Error generating mock data: {e}")


# Create a new database connection (PostgreSQL in this case)
engine = create_engine("postgresql://qllm:qllm@127.0.0.1/qllm")
Session = sessionmaker(bind=engine)
session = Session()


generate_mock_data(session=session, num_users=10)
