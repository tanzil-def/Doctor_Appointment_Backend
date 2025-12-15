from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '91cbbd3afab4'
down_revision = '77fd0f57940d'
branch_labels = None
depends_on = None


def upgrade():
  
    userrole_enum = postgresql.ENUM(
        'USER', 'DOCTOR', 'ADMIN',
        name='userrole'
    )
    userrole_enum.create(op.get_bind(), checkfirst=True)

     
    op.alter_column(
        'users',
        'role',
        type_=userrole_enum,
        postgresql_using="role::userrole"
    )


def downgrade():
    op.alter_column(
        'users',
        'role',
        type_=sa.String(length=20)
    )

    userrole_enum = postgresql.ENUM(
        'USER', 'DOCTOR', 'ADMIN',
        name='userrole'
    )
    userrole_enum.drop(op.get_bind(), checkfirst=True)
