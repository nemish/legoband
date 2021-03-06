"""empty message

Revision ID: 2ea8c6d340d0
Revises: None
Create Date: 2016-04-06 00:44:39.329398

"""

# revision identifiers, used by Alembic.
revision = '2ea8c6d340d0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('page', sa.Column('instagram_link', sa.String(length=128), nullable=True))
    op.add_column('page', sa.Column('youtube_link', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('page', 'youtube_link')
    op.drop_column('page', 'instagram_link')
    ### end Alembic commands ###
