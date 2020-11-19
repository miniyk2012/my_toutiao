"""empty message

Revision ID: b852825edd3c
Revises: c49320a82209
Create Date: 2020-11-17 19:56:58.227165

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b852825edd3c'
down_revision = 'c49320a82209'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('bio', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('github_id', sa.String(length=191), nullable=True))
    op.drop_column('users', 'github_url')
    op.drop_column('users', 'intro')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('intro', mysql.VARCHAR(collation='utf8mb4_general_ci', length=128), nullable=True))
    op.add_column('users', sa.Column('github_url', mysql.VARCHAR(collation='utf8mb4_general_ci', length=191), nullable=True))
    op.drop_column('users', 'github_id')
    op.drop_column('users', 'bio')
    # ### end Alembic commands ###
