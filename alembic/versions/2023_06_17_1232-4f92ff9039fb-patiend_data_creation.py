"""patiend data creation

Revision ID: 4f92ff9039fb
Revises: 
Create Date: 2023-06-17 12:32:44.157751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f92ff9039fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business',
    sa.Column('business_id', sa.Integer(), nullable=False),
    sa.Column('business_name', sa.String(length=100), nullable=True),
    sa.Column('symptom_code', sa.String(length=100), nullable=True),
    sa.Column('symptom_name', sa.String(length=100), nullable=True),
    sa.Column('symptom_diagnostic', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('business_id')
    )
    # ### end Alembic commands ###
    


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('business')
    # ### end Alembic commands ###