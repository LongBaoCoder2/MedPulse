"""init

Revision ID: 79f302b81b89
Revises: 
Create Date: 2025-02-19 23:19:00.035761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '79f302b81b89'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('metadata_map', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_index(op.f('ix_document_id'), 'document', ['id'], unique=False)
    op.create_table('user',
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('conversation',
    sa.Column('document_id', sa.UUID(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversation_id'), 'conversation', ['id'], unique=False)
    op.create_table('medicalrecord',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.Column('file_path', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medicalrecord_id'), 'medicalrecord', ['id'], unique=False)
    op.create_table('memory',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('type', postgresql.ENUM('EPISODIC', 'SEMANTIC', 'PROCEDURAL', name='MemoryType'), nullable=False),
    sa.Column('content', sa.JSON(), nullable=False),
    sa.Column('meta_data', sa.JSON(), nullable=True),
    sa.Column('embedding', sa.JSON(), nullable=True),
    sa.Column('importance_score', sa.Float(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_memory_id'), 'memory', ['id'], unique=False)
    op.create_table('memoryindex',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('memory_type', postgresql.ENUM('EPISODIC', 'SEMANTIC', 'PROCEDURAL', name='MemoryType'), nullable=False),
    sa.Column('index_data', sa.JSON(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_memoryindex_id'), 'memoryindex', ['id'], unique=False)
    op.create_table('conversationdocument',
    sa.Column('conversation_id', sa.UUID(), nullable=True),
    sa.Column('document_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
    sa.ForeignKeyConstraint(['document_id'], ['document.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversationdocument_conversation_id'), 'conversationdocument', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_conversationdocument_document_id'), 'conversationdocument', ['document_id'], unique=False)
    op.create_index(op.f('ix_conversationdocument_id'), 'conversationdocument', ['id'], unique=False)
    op.create_table('message',
    sa.Column('conversation_id', sa.UUID(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('role', postgresql.ENUM('USER', 'ASSISTANT', name='MessageRoleEnum'), nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'SUCCESS', 'ERROR', name='MessageStatusEnum'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_message_conversation_id'), 'message', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_message_id'), 'message', ['id'], unique=False)
    op.create_table('messagesubprocess',
    sa.Column('message_id', sa.UUID(), nullable=True),
    sa.Column('status', postgresql.ENUM('PENDING', 'FINISHED', name='MessageSubProcessStatusEnum'), nullable=False),
    sa.Column('metadata_map', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messagesubprocess_id'), 'messagesubprocess', ['id'], unique=False)
    op.create_index(op.f('ix_messagesubprocess_message_id'), 'messagesubprocess', ['message_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_messagesubprocess_message_id'), table_name='messagesubprocess')
    op.drop_index(op.f('ix_messagesubprocess_id'), table_name='messagesubprocess')
    op.drop_table('messagesubprocess')
    op.drop_index(op.f('ix_message_id'), table_name='message')
    op.drop_index(op.f('ix_message_conversation_id'), table_name='message')
    op.drop_table('message')
    op.drop_index(op.f('ix_conversationdocument_id'), table_name='conversationdocument')
    op.drop_index(op.f('ix_conversationdocument_document_id'), table_name='conversationdocument')
    op.drop_index(op.f('ix_conversationdocument_conversation_id'), table_name='conversationdocument')
    op.drop_table('conversationdocument')
    op.drop_index(op.f('ix_memoryindex_id'), table_name='memoryindex')
    op.drop_table('memoryindex')
    op.drop_index(op.f('ix_memory_id'), table_name='memory')
    op.drop_table('memory')
    op.drop_index(op.f('ix_medicalrecord_id'), table_name='medicalrecord')
    op.drop_table('medicalrecord')
    op.drop_index(op.f('ix_conversation_id'), table_name='conversation')
    op.drop_table('conversation')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_document_id'), table_name='document')
    op.drop_table('document')
    # ### end Alembic commands ###
